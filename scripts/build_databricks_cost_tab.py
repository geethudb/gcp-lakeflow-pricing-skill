#!/usr/bin/env python3
"""Add a "Databricks cost" tab to a Databricks POC workload-selection report.

The new tab is an **exact replica of the existing Cost tab** (every table, control and
collapsible section) with **Databricks columns appended**, for two variants on GCP
Enterprise: **Jobs Compute (classic)** and **Jobs Compute Photon**.

How it works: at runtime the script deep-clones the live Cost-tab DOM into the new tab,
makes every `id` and the selection-control classes unique (so the clone is fully
independent and never corrupts the original Cost tab), appends the Databricks columns,
and wires a scoped copy of the report's own cost model to the clone's own controls
(days, headroom, rate inputs, workload checkboxes, selection buttons, CSV export).

Databricks columns:
  * Workloads table: comparable Databricks instance, DBU/hour, Rate/hour, daily DBU
    cost and all-in daily cost (GCP + DBU), for classic and Photon.
  * Instance types table: comparable instance + DBU/hour + Rate/hour per variant.
  * Compare the selections: DBU cost + an all-in Total (compute + storage + DBU).
  * Compute cost / Total cost: DBU rows and an all-in total, per variant.

Instance mapping: if the GCP machine type is in the Databricks GCP list it is kept as-is;
otherwise a same-vCPU instance is chosen (same shape, closest memory, nearest family) as
primary with a second as fallback ("≈" marks an approximate match). Photon runs on any
instance and its DBU is a constant multiple of the classic DBU, so the Photon column
keeps the same instance and derives the rate ("†" marks a derived Photon rate for an
instance the calculator doesn't list individually).

Usage:
  python3 build_databricks_cost_tab.py INPUT.html [-o OUTPUT.html] [--pricing PATH]
"""
import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PRICING = os.path.join(HERE, "..", "references", "gcp-enterprise-pricing.json")


def norm(name):
    s = str(name).lower()
    s = re.sub(r"\s*\(-lssd\)\s*", "", s)
    s = re.sub(r"\s*\(photon\)\s*", "", s)
    return s.replace("_", "-").strip()


def compact_pricing(pricing_path):
    with open(pricing_path) as f:
        d = json.load(f)

    def rows(product):
        return [{"name": i["instance"], "norm": norm(i["instance"]), "v": i["vcpu"],
                 "m": i["memory_gb"], "dbu": i["dbu_per_hour"]}
                for i in d["products"][product]["instances"]]

    classic, photon = rows("Jobs Compute"), rows("Jobs Compute Photon")
    cmap = {r["norm"]: r["dbu"] for r in classic if r["dbu"]}
    ratios = [r["dbu"] / cmap[r["norm"]] for r in photon if r["norm"] in cmap]
    mult = round(statistics.median(ratios), 3) if ratios else 2.5
    return {
        "rate_classic": d["products"]["Jobs Compute"]["usd_per_dbu"],
        "rate_photon": d["products"]["Jobs Compute Photon"]["usd_per_dbu"],
        "photon_mult": mult,
        "classic": classic,
        "photon": photon,
        "scraped_on": d.get("scraped_on", ""),
    }


TAB_BUTTON = ('<button type="button" role="tab" data-tab="databricks" '
              'aria-controls="databricks">Databricks cost</button>')

# Empty panel; populated at runtime by cloning the Cost tab.
SECTION = '<section class="tab" id="databricks" role="tabpanel"></section>'

RENDER_JS = r"""<script>
(function(){
  if(typeof cd==='undefined'||!cd) return;
  var PRICE=JSON.parse(document.getElementById('dbx-pricing').textContent);
  var RC=PRICE.rate_classic, RP=PRICE.rate_photon;
  function nz(s){s=String(s).toLowerCase().replace(/\s*\(-lssd\)\s*/g,'').replace(/\s*\(photon\)\s*/g,'').replace(/_/g,'-').trim();return s;}
  function shapeOf(s){s=nz(s);return /highmem/.test(s)?'highmem':/highcpu/.test(s)?'highcpu':/standard/.test(s)?'standard':/highgpu|ultragpu/.test(s)?'gpu':'';}
  function famOf(n){var m=/^([a-z]+[0-9]+[a-z]*)/.exec(nz(n));return m?m[1]:'';}
  function famBase(f){return f.replace(/d$/,'');}
  function famScore(src,cand){
    if(!src||!cand) return 9;
    if(src===cand) return 0;
    if(famBase(src)===famBase(cand)) return 1;
    var ls=(/^[a-z]+/.exec(src)||[''])[0], lc=(/^[a-z]+/.exec(cand)||[''])[0];
    var gs=parseInt((/[0-9]+/.exec(src)||['0'])[0],10), gc=parseInt((/[0-9]+/.exec(cand)||['0'])[0],10);
    if(ls===lc) return 2+Math.abs(gs-gc);
    return 9;
  }
  function near(list,vcpu,mem,shape,srcFam){
    return list.slice().sort(function(a,b){
      var sa=(shape&&a.norm.indexOf(shape)>=0)?0:1, sb=(shape&&b.norm.indexOf(shape)>=0)?0:1;
      return (Math.abs(a.v-vcpu)-Math.abs(b.v-vcpu)) || (sa-sb)
        || (Math.abs(a.m-mem)-Math.abs(b.m-mem))
        || (famScore(srcFam,famOf(a.norm))-famScore(srcFam,famOf(b.norm)))
        || a.norm.localeCompare(b.norm);});
  }
  // Map a GCP type to a supported instance in `list`: {primary,fallback,exact}.
  // Classic and Photon are matched independently against their own lists; a Photon rate
  // is NEVER derived from classic — if the type isn't Photon-listed, a real
  // Photon-supported same-spec instance is substituted.
  function mapIn(list,typeStr,vcpu,mem){
    var names=String(typeStr).toLowerCase().split(/\s+or\s+|,/).map(nz).filter(Boolean);
    var shape=shapeOf(names[0]||typeStr), srcFam=famOf(names[0]||typeStr);
    for(var i=0;i<names.length;i++){
      var ex=list.filter(function(r){return r.norm===names[i];});
      if(ex.length){
        var fb=near(list,ex[0].v,ex[0].m,shape,srcFam).filter(function(r){return r.norm!==ex[0].norm;})[0]||null;
        return {primary:ex[0],fallback:fb,exact:true};
      }
    }
    var p=near(list,vcpu,mem,shape,srcFam);
    return {primary:p[0]||null,fallback:p[1]||null,exact:false};
  }
  function mapC(t,v,m){return mapIn(PRICE.classic,t,v,m);}
  function mapP(t,v,m){return mapIn(PRICE.photon,t,v,m);}
  function disp(m){ if(!m.primary) return 'n/a';
    return m.primary.name+(m.exact?'':' ≈')+(m.fallback?' / '+m.fallback.name:''); }

  // Cluster DBU/hr for a workload, matched against the given list (classic or Photon).
  function cluster(w,list){var t=0,ok=false;(w.instances||[]).forEach(function(e){
    var m=mapIn(list,e.instance_type,cnum(e.vcpus_each),cnum(e.memory_gb_each));
    if(m.primary){t+=e.count*m.primary.dbu;ok=true;}});return ok?t:null;}
  function wlDaily(w,photon){var c=cluster(w,photon?PRICE.photon:PRICE.classic),rt=cnum(w.plan.runtime_p50_min),rn=cnum(w.plan.runs_per_day);
    if(c===null||rt===null||rn===null) return null;
    return c*(photon?RP:RC)*(rt/60)*rn;}
  function setDaily(rows,photon){var t=0;rows.forEach(function(i){var v=wlDaily(cd.workloads[i],photon);if(v!==null)t+=v;});return t;}

  // ---------- clone the Cost tab into the Databricks tab ----------
  var src=document.getElementById('cost'), host=document.getElementById('databricks');
  if(!src||!host) return;
  var clone=src.cloneNode(true);
  clone.querySelectorAll('script,style').forEach(function(e){e.remove();});
  var idmap={};
  clone.querySelectorAll('[id]').forEach(function(el){var o=el.id,n=o+'_dbx';idmap[o]=n;el.id=n;});
  ['for','aria-controls','aria-labelledby','aria-describedby','headers','list'].forEach(function(a){
    clone.querySelectorAll('['+a+']').forEach(function(el){var v=el.getAttribute(a);if(idmap[v])el.setAttribute(a,idmap[v]);});});
  clone.querySelectorAll('a[href^="#"]').forEach(function(a){var t=a.getAttribute('href').slice(1);if(idmap[t])a.setAttribute('href','#'+idmap[t]);});
  // Unique control classes so the original Cost-tab JS never sees these elements.
  [['cpick','dbxpick'],['cpickall','dbxpickall'],['csetpick','dbxsetpick']].forEach(function(p){
    clone.querySelectorAll('.'+p[0]).forEach(function(e){e.classList.remove(p[0]);e.classList.add(p[1]);});});

  var note=document.createElement('div');note.className='note';
  note.innerHTML=
    '<p><b>What this tab shows.</b> The same workloads as the <b>Cost</b> tab, re-priced for '
    +'<b>Databricks (Lakeflow Jobs) on Google Cloud — Enterprise tier</b>, for two engines: '
    +'<b>Jobs Compute (classic)</b> and <b>Jobs Compute Photon</b> (both $'+RC+'/DBU, scraped '+PRICE.scraped_on+'). '
    +'Every Cost-tab table and control is mirrored here, with Databricks columns added.</p>'
    +'<p><b>How the Databricks cost is calculated.</b> Databricks bills by <b>DBUs</b> (its compute unit), '
    +'not by VM. Each GCP machine type is matched to a comparable Databricks-supported instance — classic '
    +'and Photon are matched <i>independently</i> against their own instance lists; "≈" marks a nearest '
    +'same-spec substitute used when the exact type isn\'t offered (a Photon rate is never derived — it '
    +'always maps to a real Photon-listed instance). Then, per workload:</p>'
    +'<p style="margin-left:1.2em"><code>cluster DBU/hr = Σ ( nodes × instance DBU/hr )</code><br>'
    +'<code>Rate/hr&nbsp;&nbsp;&nbsp;&nbsp;= cluster DBU/hr × $'+RC+' per DBU</code><br>'
    +'<code>DBU/day&nbsp;&nbsp;&nbsp;&nbsp;= Rate/hr × ( median run minutes ÷ 60 ) × runs per day</code></p>'
    +'<p><b>How it differs from the Cost tab.</b> The <b>Cost</b> tab is the <b>Google Cloud infrastructure</b> '
    +'cost of the current Dataproc setup (VMs, local SSDs, boot disks, storage and egress). This tab adds the '
    +'<b>Databricks DBU software charge</b> for running those same clusters on Databricks instead; the '
    +'<b>All-in</b> figures = the Cost-tab GCP infrastructure cost <b>+</b> the DBU cost. A DBU figure on its '
    +'own is the Databricks charge only and does <i>not</i> include the underlying GCE VM cost.</p>';
  host.textContent=''; host.appendChild(note);
  while(clone.firstChild) host.appendChild(clone.firstChild);

  // ---------- append Databricks column headers ----------
  function addTh(table,specs){ if(!table||!table.tHead||!table.tHead.rows[0]) return;
    var tr=table.tHead.rows[0];
    specs.forEach(function(sp){var th=document.createElement('th');if(sp.n)th.className='n';
      if(sp.sort){var b=document.createElement('button');b.type='button';b.textContent=sp.t;th.appendChild(b);}
      else th.textContent=sp.t; tr.appendChild(th);});}
  function tableOf(id){var tb=document.getElementById(id);return tb?tb.closest('table'):null;}
  // Workloads: find the static table whose header has a "Workload" column.
  var wlTable=null, wlCol=-1;
  host.querySelectorAll('table').forEach(function(t){
    if(wlTable||!t.tHead) return;
    var hs=[].slice.call(t.tHead.rows[0].cells).map(function(c){return c.textContent.trim();});
    var i=hs.indexOf('Workload'); if(i>=0 && hs.indexOf('Daily')>=0){wlTable=t;wlCol=i;}});
  var instH=[{t:'Classic: Databricks instance'},{t:'DBU/hr',n:1,sort:1},{t:'Rate/hr',n:1,sort:1},
             {t:'DBU daily',n:1,sort:1},{t:'All-in daily',n:1,sort:1},
             {t:'Photon: Databricks instance'},{t:'DBU/hr',n:1,sort:1},{t:'Rate/hr',n:1,sort:1},
             {t:'DBU daily',n:1,sort:1},{t:'All-in daily',n:1,sort:1}];
  addTh(wlTable,instH);
  addTh(tableOf('cinst_dbx'),[{t:'Classic instance'},{t:'DBU/hr',n:1},{t:'Rate/hr',n:1},
                              {t:'Photon instance'},{t:'DBU/hr',n:1},{t:'Rate/hr',n:1}]);
  addTh(tableOf('csets_dbx'),[{t:'DBU (classic)',n:1},{t:'Total+DBU (classic)',n:1},
                              {t:'DBU (Photon)',n:1},{t:'Total+DBU (Photon)',n:1}]);

  // ---------- append Databricks cells to the static Workloads rows ----------
  var byName={}; cd.workloads.forEach(function(w){byName[w.workload]=w;});
  function td(tr,text,n,v){var c=document.createElement('td');c.textContent=text;if(n)c.className='n';
    if(v!==undefined&&v!==null)c.dataset.v=v;tr.appendChild(c);}
  if(wlTable){ [].slice.call(wlTable.tBodies[0].rows).forEach(function(tr){
    var w=byName[(tr.cells[wlCol]||{}).textContent ? tr.cells[wlCol].textContent.trim():''];
    if(!w){instH.forEach(function(){td(tr,'');});return;}
    var p=w.plan, gcp=cnum(p.daily_cost_usd), cc=cluster(w,PRICE.classic), pc=cluster(w,PRICE.photon);
    var dC=wlDaily(w,false), dP=wlDaily(w,true);
    var mc=mapC(p.worker_machine_types,cnum(p.vcpus_per_worker),cnum(p.memory_gb_per_worker));
    var mp=mapP(p.worker_machine_types,cnum(p.vcpus_per_worker),cnum(p.memory_gb_per_worker));
    td(tr,disp(mc));
    td(tr,cc===null?'n/a':cfmt(cc,2),1,cc);
    td(tr,cc===null?'n/a':money(cc*RC),1,cc===null?null:cc*RC);
    td(tr,money(dC),1,dC);
    td(tr,money(gcp===null||dC===null?null:gcp+dC),1,(gcp===null||dC===null)?null:gcp+dC);
    td(tr,disp(mp));
    td(tr,pc===null?'n/a':cfmt(pc,2),1,pc);
    td(tr,pc===null?'n/a':money(pc*RP),1,pc===null?null:pc*RP);
    td(tr,money(dP),1,dP);
    td(tr,money(gcp===null||dP===null?null:gcp+dP),1,(gcp===null||dP===null)?null:gcp+dP);
  }); }

  // ---------- scoped cost model (own controls) ----------
  function el(id){return document.getElementById(id);}
  function settingsD(){var h=el('headroom_dbx'),d=el('days_dbx');
    return {h:Math.max(0,parseFloat(h&&h.value)||0),days:Math.max(0,parseFloat(d&&d.value)||0)};}
  function rateD(id,dflt){var e=el(id+'_dbx'),v=e?parseFloat(e.value):NaN;return isNaN(v)||v<0?(dflt||0):v;}
  function pickedD(){var on=[];host.querySelectorAll('input.dbxpick').forEach(function(b){if(b.checked)on.push(+b.dataset.i);});return on;}
  // storage() re-scoped to the Databricks rate inputs.
  function storageD(on,a,days,inputs){var t=rateD('rtransfer',cd.rates.transfer),st=rateD('rstorage',cd.rates.storage),op=rateD('rclassa',cd.rates.class_a);
    var G=1073741824,has={},cov={},bb=0,db=0,bo=0,dob=0,est=0,made=0,n=0;on.forEach(function(i){has[i]=1;});
    var any=function(l){return l.some(function(i){return has[i];});};
    (inputs||cd.inputs||[]).forEach(function(e){if(!any(e.r))return;n++;e.r.forEach(function(i){cov[i]=1;});
      bb+=e.bb||0;bo+=e.bo||0;if(any(e.p))made++;else{db+=e.db||0;dob+=e.do||0;}});
    bb/=G;db/=G;
    on.forEach(function(i){if(cov[i])return;var w=cd.workloads[i].plan,v=cnum(w.daily_copy_gib),o=cnum(w.daily_objects);
      if(v!==null){db+=v;dob+=o||0;est++;}});
    var copied=bb+db*days;
    return {backfill:bb,copy:db,copied:copied,transfer:copied*t,rest:(bb*days+db*days*(days+1)/2)/30*st,
            ops:(bo+dob*days)/1000*op,est:est,inputs:n,made:made};}

  function compareD(){var tb=el('csets_dbx');if(!tb||!cd.sets)return;var s=settingsD(),f=1+s.h/100,base=null;
    var t=function(v){return cfmt(v/1024,1)+' TiB';};
    fill('csets_dbx',cd.sets.map(function(x){var a=agg(x.rows),g=storageD(x.rows,a,s.days,x.inputs||cd.inputs),
      c=a.daily*s.days*f,st=(g.transfer+g.rest+g.ops)*f,tot=c+st;
      var dc=setDaily(x.rows,false)*s.days*f, dp=setDaily(x.rows,true)*s.days*f;
      if(base===null)base=tot;
      return [[x.label],[cfmt(x.rows.length,0),1],[cfmt(cup(a.tot.vms,s.h,0),0),1],[money(c),1],[t(g.backfill),1],[t(g.copy),1],[money(st),1],[money(tot),1],
              [base?(tot===base?'':cfmt((tot/base-1)*100,0)+'%'):'',1],
              [money(dc),1],[money(tot+dc),1],[money(dp),1],[money(tot+dp),1]];}));}

  function planD(){var on=pickedD(),s=settingsD(),h=s.h,f=1+h/100,a=agg(on);
    var pc=el('cpicked_dbx');if(pc)pc.textContent=on.length+' of '+cd.workloads.length+' selected';
    fill('cinst_dbx',Object.keys(a.inst).sort(function(x,y){return a.inst[y].count-a.inst[x].count;}).map(function(k){
      var e=a.inst[k],n=cup(e.count,h,0),mc=mapC(e.t,e.v,e.m),mp=mapP(e.t,e.v,e.m);
      var c0=mc.primary?mc.primary.dbu:null, p0=mp.primary?mp.primary.dbu:null;
      return [[e.t],[Object.keys(e.roles).sort().join(', ')],[cfmt(e.v,0),1],[cfmt(e.m,0),1],[cfmt(e.count,0),1],[cfmt(n,0),1],
              [cfmt(e.v===null?null:e.v*n,0),1],[cfmt(e.m===null?null:e.m*n,0),1],
              [disp(mc)],[c0===null?'n/a':cfmt(c0,2),1],[c0===null?'n/a':money(c0*RC),1],
              [disp(mp)],[p0===null?'n/a':cfmt(p0,2),1],[p0===null?'n/a':money(p0*RP),1]];}));
    fill('cdisk_dbx',Object.keys(a.disk).sort(function(x,y){return a.disk[y].count-a.disk[x].count;}).map(function(k){var e=a.disk[k],n=cup(e.count,h,0);
      return [[e.d],[e.ty],[cfmt(e.s,0),1],[cfmt(e.count,0),1],[cfmt(n,0),1],[cfmt(e.s===null?null:e.s*n,0),1]];}));
    fill('ctot_dbx',cd.totals.map(function(t){var v=a.tot[t[1]],m=a.miss[t[1]];
      return [[t[0]+(m?' ('+m+' without data)':'')],[cfmt(v,t[2]),1],[cfmt(cup(v,h,t[2]),t[2]),1]];}));
    var note2=function(m){return m?' ('+m+' without a price)':'';};
    var dC=setDaily(on,false), dP=setDaily(on,true);
    fill('ccost_dbx',[[['Hourly: the selected clusters all running'+note2(a.hm)],[money(a.hourly),1],[money(a.hourly*f),1]],
                  [['Daily: runs per day x a median run'+note2(a.dm)],[money(a.daily),1],[money(a.daily*f),1]],
                  [['Total for '+s.days+' day'+(s.days===1?'':'s')+note2(a.dm)],[money(a.daily*s.days),1],[money(a.daily*s.days*f),1]],
                  [['DBU classic, daily'],[money(dC),1],[money(dC*f),1]],
                  [['DBU Photon, daily'],[money(dP),1],[money(dP*f),1]]]);
    var g=storageD(on,a,s.days,inputsFor(on)),tb=function(v){return cfmt(v===null?null:v/1024,2)+' TiB';};
    var stot=g.transfer+g.rest+g.ops,dd=s.days+' day'+(s.days===1?'':'s');
    fill('cstore_dbx',[[['Backfill, once: '+g.inputs+' measured input'+(g.inputs===1?'':'s')],[tb(g.backfill),1],[tb(cup(g.backfill,h,1)),1]],
                   [['Copy per day'+(g.made?' ('+g.made+' produced in the POC, not copied)':'')+(g.est?' (~'+g.est+' workload'+(g.est===1?'':'s')+' estimated)':'')],[tb(g.copy),1],[tb(cup(g.copy,h,1)),1]],
                   [['Copied: backfill plus '+dd],[tb(g.copied),1],[tb(cup(g.copied,h,1)),1]],
                   [['Transfer, '+cd.rates_label.transfer],[money(g.transfer),1],[money(g.transfer*f),1]],
                   [['Storage at rest, everything kept'],[money(g.rest),1],[money(g.rest*f),1]],
                   [['Operations, one Class A rewrite per object'],[money(g.ops),1],[money(g.ops*f),1]],
                   [['Storage total'],[money(stot),1],[money(stot*f),1]]]);
    var ctot=a.daily*s.days, dCd=dC*s.days, dPd=dP*s.days;
    fill('cgrand_dbx',[[['Compute for '+dd],[money(ctot),1],[money(ctot*f),1]],
                   [['Storage for '+dd],[money(stot),1],[money(stot*f),1]],
                   [['Total (GCP only)'],[money(ctot+stot),1],[money((ctot+stot)*f),1]],
                   [['DBU classic for '+dd],[money(dCd),1],[money(dCd*f),1]],
                   [['DBU Photon for '+dd],[money(dPd),1],[money(dPd*f),1]],
                   [['All-in total (classic)'],[money(ctot+stot+dCd),1],[money((ctot+stot+dCd)*f),1]],
                   [['All-in total (Photon)'],[money(ctot+stot+dPd),1],[money((ctot+stot+dPd)*f),1]]]);
    compareD();}

  function exportD(){var on=pickedD(),s=settingsD(),f=1+s.h/100,a=agg(on),NLx=String.fromCharCode(10),lines=[];
    var q=function(v){v=v===null||v===undefined?'':String(v);return new RegExp('[",'+NLx+']').test(v)?'"'+v.replace(/"/g,'""')+'"':v;};
    var row=function(r){lines.push(r.map(q).join(','));};
    row(['setting','value']);row(['headroom_pct',s.h]);row(['days',s.days]);row(['selected_workloads',on.length]);
    row(['dbu_rate_classic',RC]);row(['dbu_rate_photon',RP]);row(['photon_multiplier',MULT]);lines.push('');
    var cols=cd.columns;
    row(['workload'].concat(cols).concat(['dbx_instance_classic','cluster_dbu_per_hr','dbu_daily_classic','allin_daily_classic',
         'dbx_instance_photon','cluster_dbu_per_hr_photon','dbu_daily_photon','allin_daily_photon']));
    on.forEach(function(i){var w=cd.workloads[i],p=w.plan,gcp=cnum(p.daily_cost_usd),cc=clusterC(w),dC=wlDaily(w,false),dP=wlDaily(w,true);
      var mc=mapC(p.worker_machine_types,cnum(p.vcpus_per_worker),cnum(p.memory_gb_per_worker));
      row([w.workload].concat(cols.map(function(c){return p[c];})).concat([
        dispC(mc), cc===null?'':cc.toFixed(2), dC===null?'':dC.toFixed(2), (gcp===null||dC===null)?'':(gcp+dC).toFixed(2),
        dispP(mc), cc===null?'':(cc*MULT).toFixed(2), dP===null?'':dP.toFixed(2), (gcp===null||dP===null)?'':(gcp+dP).toFixed(2)]));});
    lines.push('');
    var g=storageD(on,a,s.days,inputsFor(on)),stot=g.transfer+g.rest+g.ops,ctot=a.daily*s.days,dCd=setDaily(on,false)*s.days,dPd=setDaily(on,true)*s.days;
    row(['total','value']);row(['compute_usd',ctot.toFixed(2)]);row(['storage_usd',stot.toFixed(2)]);
    row(['dbu_classic_usd',dCd.toFixed(2)]);row(['dbu_photon_usd',dPd.toFixed(2)]);
    row(['allin_classic_usd',(ctot+stot+dCd).toFixed(2)]);row(['allin_photon_usd',(ctot+stot+dPd).toFixed(2)]);
    var blob=new Blob([lines.join(NLx)],{type:'text/csv'}),link=document.createElement('a');
    link.href=URL.createObjectURL(blob);link.download='databricks-cost-plan-'+cd.run+'.csv';document.body.appendChild(link);link.click();
    setTimeout(function(){URL.revokeObjectURL(link.href);link.remove();},0);}

  // ---------- wire the clone's own controls ----------
  ['headroom_dbx','days_dbx','rtransfer_dbx','rstorage_dbx','rclassa_dbx'].forEach(function(id){var e=el(id);if(e)e.addEventListener('input',planD);});
  host.querySelectorAll('input.dbxpick').forEach(function(b){b.addEventListener('change',planD);});
  host.querySelectorAll('button.dbxpickall').forEach(function(b){b.addEventListener('click',function(){
    host.querySelectorAll('input.dbxpick').forEach(function(x){x.checked=b.dataset.all==='1';});planD();});});
  host.querySelectorAll('button.dbxsetpick').forEach(function(b){b.addEventListener('click',function(){
    var x=(cd.sets||[]).filter(function(s){return s.id===b.dataset.set;})[0];if(!x)return;
    host.querySelectorAll('input.dbxpick').forEach(function(c){c.checked=x.rows.indexOf(+c.dataset.i)>=0;});planD();});});
  var ex=el('cexport_dbx');if(ex)ex.addEventListener('click',exportD);
  // Re-bind sortable tables inside the clone (the global binding ran before it existed).
  host.querySelectorAll('table.sortable').forEach(function(t){
    t.querySelectorAll('th').forEach(function(th,i){var b=th.querySelector('button');if(!b)return;
      b.addEventListener('click',function(){
        var rows=Array.prototype.slice.call(t.tBodies[0].rows),asc=th.getAttribute('aria-sort')!=='ascending';
        t.querySelectorAll('th').forEach(function(o){o.removeAttribute('aria-sort');});
        th.setAttribute('aria-sort',asc?'ascending':'descending');
        rows.sort(function(a,b){var x=a.cells[i].dataset.v,y=b.cells[i].dataset.v,p=parseFloat(x),cq=parseFloat(y);
          var c=(!isNaN(p)&&!isNaN(cq))?p-cq:String(x).localeCompare(String(y));return asc?c:-c;});
        rows.forEach(function(r){t.tBodies[0].appendChild(r);});});});});

  planD();
})();
</script>"""


def inject(html, pricing):
    pricing_script = ('<script type="application/json" id="dbx-pricing">'
                      + json.dumps(pricing, separators=(",", ":")) + "</script>")

    ts = html.find('<nav role="tablist">')
    if ts == -1:
        sys.exit("Could not find the tablist <nav> in the report.")
    # Place the Databricks tab immediately after the Cost tab button.
    cost_btn = html.find('data-tab="cost"', ts)
    if cost_btn != -1:
        at = html.find("</button>", cost_btn) + len("</button>")
    else:
        at = html.find("</nav>", ts)
    html = html[:at] + TAB_BUTTON + html[at:]

    cs = html.find('<section class="tab" id="cost"')
    if cs == -1:
        sys.exit("Could not find the Cost tab panel.")
    nxt = html.find('<section class="tab"', cs + 10)
    insert_at = nxt if nxt != -1 else html.find("</section>", cs) + len("</section>")
    html = html[:insert_at] + SECTION + html[insert_at:]

    be = html.rfind("</body>")
    be = be if be != -1 else len(html)
    html = html[:be] + pricing_script + RENDER_JS + html[be:]
    return html


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="path to the POC report HTML")
    ap.add_argument("-o", "--output", help="output path (default: <input>-databricks.html)")
    ap.add_argument("--pricing", default=DEFAULT_PRICING, help="Databricks GCP Enterprise pricing JSON")
    args = ap.parse_args()

    out = args.output or re.sub(r"\.html?$", "", args.input) + "-databricks.html"
    if os.path.abspath(out) == os.path.abspath(args.input):
        sys.exit("Refusing to overwrite the input file; choose a different --output.")

    pricing = compact_pricing(args.pricing)
    with open(args.input, encoding="utf-8") as f:
        html = f.read()
    html = inject(html, pricing)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote", out)
    print(f"  classic {len(pricing['classic'])}  photon {len(pricing['photon'])}  "
          f"rate ${pricing['rate_classic']:g}/DBU  photon x{pricing['photon_mult']}")


if __name__ == "__main__":
    main()
