# GCP Enterprise — Lakeflow Jobs (classic) & Photon pricing

Scraped 2026-10-23 from https://www.databricks.com/product/pricing/product-pricing/instance-types

- **Cloud:** GCP  **Plan:** Enterprise
- **Jobs Compute (Lakeflow Jobs classic):** $0.20 / DBU
- **Jobs Compute Photon:** $0.20 / DBU
- `$/hr = DBU/hr x $/DBU`. **DBU charge only** — Google Cloud VM/infra billed separately.

## Jobs Compute ($0.2/DBU) — 174 instances

| Instance | vCPU | Mem (GB) | DBU/hr | $/hr |
|---|---:|---:|---:|---:|
| a2-highgpu-16g | 96 | 1360 | 63.84 | 12.7680 |
| a2-highgpu-1g | 12 | 85 | 5.43 | 1.0860 |
| a2-highgpu-2g | 24 | 170 | 10.86 | 2.1720 |
| a2-highgpu-4g | 48 | 340 | 21.72 | 4.3440 |
| a2-highgpu-8g | 96 | 680 | 43.44 | 8.6880 |
| a2-ultragpu-1g | 12 | 170 | 7.98 | 1.5960 |
| a2-ultragpu-2g | 24 | 340 | 15.96 | 3.1920 |
| a2-ultragpu-4g | 48 | 680 | 31.92 | 6.3840 |
| a2-ultragpu-8g | 96 | 1360 | 63.84 | 12.7680 |
| a3-highgpu-1g | 26 | 234 | 14.13 | 2.8260 |
| a3-highgpu-2g | 26 | 234 | 28.25 | 5.6500 |
| a3-highgpu-4g | 26 | 234 | 56.51 | 11.3020 |
| a3-highgpu-8g | 26 | 234 | 113.02 | 22.6040 |
| c2-standard-16 | 16 | 64 | 2.88 | 0.5760 |
| c2-standard-30 | 30 | 120 | 5.4 | 1.0800 |
| c2-standard-4 | 4 | 16 | 0.72 | 0.1440 |
| c2-standard-60 | 60 | 240 | 10.8 | 2.1600 |
| c2-standard-8 | 8 | 32 | 1.44 | 0.2880 |
| c3-highmem-22 | 22 | 176 | 6.6 | 1.3200 |
| c3-highmem-4 | 4 | 32 | 1.2 | 0.2400 |
| c3-highmem-44 | 44 | 352 | 13.2 | 2.6400 |
| c3-highmem-8 | 8 | 64 | 2.4 | 0.4800 |
| c3-highmem-88 | 88 | 704 | 26.4 | 5.2800 |
| c3-standard-176 (-lssd) | 176 | 704 | 37.4 | 7.4800 |
| c3-standard-22 (-lssd) | 22 | 88 | 4.68 | 0.9360 |
| c3-standard-4 (-lssd) | 4 | 16 | 0.85 | 0.1700 |
| c3-standard-44 (-lssd) | 44 | 176 | 9.35 | 1.8700 |
| c3-standard-8 (-lssd) | 8 | 32 | 1.7 | 0.3400 |
| c3-standard-88 (-lssd) | 88 | 352 | 18.7 | 3.7400 |
| c3d-highmem-16 (-lssd) | 16 | 128 | 4.8 | 0.9600 |
| c3d-highmem-180 (-lssd) | 180 | 1440 | 54 | 10.8000 |
| c3d-highmem-30 (-lssd) | 30 | 240 | 9 | 1.8000 |
| c3d-highmem-360 (-lssd) | 360 | 2880 | 108 | 21.6000 |
| c3d-highmem-4 (-lssd) | 4 | 32 | 1.2 | 0.2400 |
| c3d-highmem-60 (-lssd) | 60 | 480 | 18 | 3.6000 |
| c3d-highmem-8 (-lssd) | 8 | 64 | 2.4 | 0.4800 |
| c3d-highmem-90 (-lssd) | 90 | 720 | 27 | 5.4000 |
| c3d-standard-16 (-lssd) | 16 | 64 | 3.4 | 0.6800 |
| c3d-standard-180 (-lssd) | 180 | 720 | 38.25 | 7.6500 |
| c3d-standard-30 (-lssd) | 30 | 120 | 6.38 | 1.2760 |
| c3d-standard-360 (-lssd) | 360 | 1440 | 76.5 | 15.3000 |
| c3d-standard-4 (-lssd) | 4 | 16 | 0.85 | 0.1700 |
| c3d-standard-60 (-lssd) | 60 | 240 | 12.75 | 2.5500 |
| c3d-standard-8 (-lssd) | 8 | 32 | 1.7 | 0.3400 |
| c3d-standard-90 (-lssd) | 90 | 360 | 19.13 | 3.8260 |
| c4-standard-16 | 16 | 60 | 4.24 | 0.8500 |
| c4-standard-2 | 2 | 7 | 0.53 | 0.1100 |
| c4-standard-24 | 24 | 90 | 6.36 | 1.2700 |
| c4-standard-32 | 32 | 120 | 8.48 | 1.7000 |
| c4-standard-4 | 4 | 15 | 1.06 | 0.2100 |
| c4-standard-8 | 8 | 30 | 2.12 | 0.4200 |
| c4a-highmem-16 (-lssd) | 16 | 128 | 6.97 | 1.3940 |
| c4a-highmem-32 (-lssd) | 32 | 256 | 13.94 | 2.7880 |
| c4a-highmem-4 (-lssd) | 4 | 32 | 1.74 | 0.3480 |
| c4a-highmem-48 (-lssd) | 48 | 384 | 20.91 | 4.1820 |
| c4a-highmem-64 (-lssd) | 64 | 512 | 27.88 | 5.5760 |
| c4a-highmem-72 (-lssd) | 72 | 576 | 31.36 | 6.2720 |
| c4a-highmem-8 (-lssd) | 8 | 64 | 3.48 | 0.6960 |
| c4a-standard-16 (-lssd) | 16 | 64 | 4.93 | 0.9860 |
| c4a-standard-32 (-lssd) | 32 | 128 | 9.86 | 1.9720 |
| c4a-standard-4 (-lssd) | 4 | 16 | 1.23 | 0.2460 |
| c4a-standard-48 (-lssd) | 48 | 192 | 14.78 | 2.9560 |
| c4a-standard-64 (-lssd) | 64 | 256 | 19.71 | 3.9420 |
| c4a-standard-72 (-lssd) | 72 | 288 | 22.18 | 4.4360 |
| c4a-standard-8 (-lssd) | 8 | 32 | 2.46 | 0.4920 |
| c4d-standard-16 | 16 | 62 | 5.94 | 1.1900 |
| c4d-standard-2 | 2 | 7 | 0.74 | 0.1500 |
| c4d-standard-32 | 32 | 124 | 11.88 | 2.3800 |
| c4d-standard-4 | 4 | 15 | 1.49 | 0.3000 |
| c4d-standard-8 | 8 | 31 | 2.97 | 0.5900 |
| e2_highcpu_16 | 16 | 16 | 2.16 | 0.4320 |
| e2_highcpu_32 | 32 | 32 | 4.32 | 0.8640 |
| e2_highmem_16 | 16 | 128 | 3.84 | 0.7680 |
| e2_highmem_2 | 2 | 16 | 0.48 | 0.0960 |
| e2_highmem_4 | 4 | 32 | 0.96 | 0.1920 |
| e2_highmem_8 | 8 | 64 | 1.92 | 0.3840 |
| e2_standard_16 | 16 | 64 | 2.88 | 0.5760 |
| e2_standard_32 | 32 | 128 | 5.76 | 1.1520 |
| e2_standard_4 | 4 | 16 | 0.72 | 0.1440 |
| e2_standard_8 | 8 | 32 | 1.44 | 0.2880 |
| g2-standard-12 | 12 | 48 | 4.32 | 0.8640 |
| g2-standard-16 | 16 | 64 | 5.76 | 1.1520 |
| g2-standard-24 | 24 | 96 | 8.64 | 1.7280 |
| g2-standard-32 | 32 | 128 | 11.52 | 2.3040 |
| g2-standard-4 | 4 | 16 | 1.44 | 0.2880 |
| g2-standard-48 | 48 | 192 | 17.28 | 3.4560 |
| g2-standard-8 | 8 | 32 | 2.88 | 0.5760 |
| g2-standard-96 | 96 | 384 | 34.56 | 6.9120 |
| g4-standard-192 | 192 | 720 | 77.76 | 15.5520 |
| g4-standard-384 | 384 | 1440 | 155.52 | 31.1040 |
| g4-standard-48 | 48 | 180 | 19.44 | 3.8880 |
| g4-standard-96 | 96 | 360 | 38.88 | 7.7760 |
| n1-highcpu-16 | 16 | 14 | 2.14 | 0.4280 |
| n1-highcpu-32 | 32 | 29 | 4.27 | 0.8540 |
| n1-highcpu-64 | 64 | 58 | 8.54 | 1.7080 |
| n1-highcpu-96 | 96 | 86 | 12.82 | 2.5640 |
| n1-highmem-16 | 16 | 104 | 3.48 | 0.6960 |
| n1-highmem-32 | 32 | 208 | 6.96 | 1.3920 |
| n1-highmem-4 | 4 | 26 | 0.87 | 0.1740 |
| n1-highmem-64 | 64 | 416 | 13.92 | 2.7840 |
| n1-highmem-8 | 8 | 52 | 1.74 | 0.3480 |
| n1-highmem-96 | 96 | 624 | 20.88 | 4.1760 |
| n1-standard-16 | 16 | 60 | 2.82 | 0.5640 |
| n1-standard-32 | 32 | 120 | 5.64 | 1.1280 |
| n1-standard-4 | 4 | 15 | 0.71 | 0.1420 |
| n1-standard-64 | 64 | 240 | 11.28 | 2.2560 |
| n1-standard-8 | 8 | 30 | 1.41 | 0.2820 |
| n1-standard-96 | 96 | 360 | 16.92 | 3.3840 |
| n2-highcpu-16 | 16 | 16 | 2.16 | 0.4320 |
| n2-highcpu-32 | 32 | 32 | 4.32 | 0.8640 |
| n2-highcpu-48 | 48 | 48 | 6.48 | 1.2960 |
| n2-highcpu-64 | 64 | 64 | 8.64 | 1.7280 |
| n2-highcpu-80 | 80 | 80 | 10.8 | 2.1600 |
| n2-highmem-16 | 16 | 128 | 3.84 | 0.7680 |
| n2-highmem-2 | 2 | 16 | 0.48 | 0.0960 |
| n2-highmem-32 | 32 | 256 | 7.68 | 1.5360 |
| n2-highmem-4 | 4 | 32 | 0.96 | 0.1920 |
| n2-highmem-48 | 48 | 384 | 11.52 | 2.3040 |
| n2-highmem-64 | 64 | 512 | 15.36 | 3.0720 |
| n2-highmem-8 | 8 | 64 | 1.92 | 0.3840 |
| n2-highmem-80 | 80 | 640 | 19.2 | 3.8400 |
| n2-standard-16 | 16 | 64 | 2.88 | 0.5760 |
| n2-standard-32 | 32 | 128 | 5.76 | 1.1520 |
| n2-standard-4 | 4 | 16 | 0.72 | 0.1440 |
| n2-standard-48 | 48 | 192 | 8.64 | 1.7280 |
| n2-standard-64 | 64 | 256 | 11.52 | 2.3040 |
| n2-standard-8 | 8 | 32 | 1.44 | 0.2880 |
| n2-standard-80 | 80 | 320 | 14.4 | 2.8800 |
| n2d-highcpu-128 | 128 | 128 | 17.28 | 3.4560 |
| n2d-highcpu-16 | 16 | 16 | 2.16 | 0.4320 |
| n2d-highcpu-224 | 224 | 224 | 30.24 | 6.0480 |
| n2d-highcpu-32 | 32 | 32 | 4.32 | 0.8640 |
| n2d-highcpu-48 | 48 | 48 | 6.48 | 1.2960 |
| n2d-highcpu-64 | 64 | 64 | 8.64 | 1.7280 |
| n2d-highcpu-80 | 80 | 80 | 10.8 | 2.1600 |
| n2d-highcpu-96 | 96 | 96 | 12.96 | 2.5920 |
| n2d-highmem-16 | 16 | 128 | 3.84 | 0.7680 |
| n2d-highmem-2 | 2 | 16 | 0.48 | 0.0960 |
| n2d-highmem-32 | 32 | 256 | 7.68 | 1.5360 |
| n2d-highmem-4 | 4 | 32 | 0.96 | 0.1920 |
| n2d-highmem-48 | 48 | 384 | 11.52 | 2.3040 |
| n2d-highmem-64 | 64 | 512 | 15.36 | 3.0720 |
| n2d-highmem-8 | 8 | 64 | 1.92 | 0.3840 |
| n2d-highmem-80 | 80 | 640 | 19.2 | 3.8400 |
| n2d-highmem-96 | 96 | 768 | 23.04 | 4.6080 |
| n2d-standard-128 | 128 | 512 | 23.04 | 4.6080 |
| n2d-standard-16 | 16 | 64 | 2.88 | 0.5760 |
| n2d-standard-224 | 224 | 896 | 40.32 | 8.0640 |
| n2d-standard-32 | 32 | 128 | 5.76 | 1.1520 |
| n2d-standard-4 | 4 | 16 | 0.72 | 0.1440 |
| n2d-standard-48 | 48 | 192 | 8.64 | 1.7280 |
| n2d-standard-64 | 64 | 256 | 11.52 | 2.3040 |
| n2d-standard-8 | 8 | 32 | 1.44 | 0.2880 |
| n2d-standard-80 | 80 | 320 | 14.4 | 2.8800 |
| n2d-standard-96 | 96 | 384 | 17.28 | 3.4560 |
| n4-standard-16 | 16 | 64 | 3.36 | 0.6700 |
| n4-standard-2 | 2 | 8 | 0.42 | 0.0800 |
| n4-standard-32 | 32 | 128 | 6.72 | 1.3400 |
| n4-standard-4 | 4 | 16 | 0.84 | 0.1700 |
| n4-standard-8 | 8 | 32 | 1.68 | 0.3400 |
| n4d-highmem-16 | 16 | 128 | 4.76 | 0.9500 |
| n4d-highmem-2 | 2 | 16 | 0.6 | 0.1200 |
| n4d-highmem-32 | 32 | 256 | 9.52 | 1.9000 |
| n4d-highmem-4 | 4 | 32 | 1.19 | 0.2400 |
| n4d-highmem-48 | 48 | 384 | 14.28 | 2.8600 |
| n4d-highmem-64 | 64 | 512 | 19.04 | 3.8100 |
| n4d-highmem-8 | 8 | 64 | 2.38 | 0.4800 |
| n4d-standard-16 | 16 | 64 | 4.16 | 0.8300 |
| n4d-standard-2 | 2 | 8 | 0.52 | 0.1000 |
| n4d-standard-32 | 32 | 128 | 8.32 | 1.6600 |
| n4d-standard-4 | 4 | 16 | 1.04 | 0.2100 |
| n4d-standard-48 | 48 | 192 | 12.48 | 2.5000 |
| n4d-standard-64 | 64 | 256 | 16.64 | 3.3300 |
| n4d-standard-8 | 8 | 32 | 2.08 | 0.4200 |

## Jobs Compute Photon ($0.2/DBU) — 74 instances

| Instance | vCPU | Mem (GB) | DBU/hr | $/hr |
|---|---:|---:|---:|---:|
| c3-standard-176 (-lssd) (Photon) | 176 | 704 | 93.5 | 18.7000 |
| c3-standard-22 (-lssd) (Photon) | 22 | 88 | 11.7 | 2.3400 |
| c3-standard-4 (-lssd) (Photon) | 4 | 16 | 2.13 | 0.4250 |
| c3-standard-44 (-lssd) (Photon) | 44 | 176 | 23.38 | 4.6750 |
| c3-standard-8 (-lssd) (Photon) | 8 | 32 | 4.25 | 0.8500 |
| c3-standard-88 (-lssd) (Photon) | 88 | 352 | 46.75 | 9.3500 |
| c3d-highmem-16 (-lssd) (Photon) | 16 | 128 | 12 | 2.4000 |
| c3d-highmem-180 (-lssd) (Photon) | 180 | 1440 | 135 | 27.0000 |
| c3d-highmem-30 (-lssd) (Photon) | 30 | 240 | 22.5 | 4.5000 |
| c3d-highmem-360 (-lssd) (Photon) | 360 | 2880 | 270 | 54.0000 |
| c3d-highmem-4 (-lssd) (Photon) | 4 | 32 | 3 | 0.6000 |
| c3d-highmem-60 (-lssd) (Photon) | 60 | 480 | 45 | 9.0000 |
| c3d-highmem-8 (-lssd) (Photon) | 8 | 64 | 6 | 1.2000 |
| c3d-highmem-90 (-lssd) (Photon) | 90 | 720 | 67.5 | 13.5000 |
| c3d-standard-16 (-lssd) (Photon) | 16 | 64 | 8.5 | 1.7000 |
| c3d-standard-180 (-lssd) (Photon) | 180 | 720 | 95.63 | 19.1250 |
| c3d-standard-30 (-lssd) (Photon) | 30 | 120 | 15.95 | 3.1900 |
| c3d-standard-360 (-lssd) (Photon) | 360 | 1440 | 191.25 | 38.2500 |
| c3d-standard-4 (-lssd) (Photon) | 4 | 16 | 2.13 | 0.4250 |
| c3d-standard-60 (-lssd) (Photon) | 60 | 240 | 31.88 | 6.3750 |
| c3d-standard-8 (-lssd) (Photon) | 8 | 32 | 4.25 | 0.8500 |
| c3d-standard-90 (-lssd) (Photon) | 90 | 360 | 47.82 | 9.5650 |
| c4a-highmem-16 (-lssd) (Photon) | 16 | 128 | 17.43 | 3.4850 |
| c4a-highmem-32 (-lssd) (Photon) | 32 | 256 | 34.85 | 6.9700 |
| c4a-highmem-4 (-lssd) (Photon) | 4 | 32 | 4.35 | 0.8700 |
| c4a-highmem-48 (-lssd) (Photon) | 48 | 384 | 52.28 | 10.4550 |
| c4a-highmem-64 (-lssd) (Photon) | 64 | 512 | 69.7 | 13.9400 |
| c4a-highmem-72 (-lssd) (Photon) | 72 | 576 | 78.4 | 15.6800 |
| c4a-highmem-8 (-lssd) (Photon) | 8 | 64 | 8.7 | 1.7400 |
| c4a-standard-16 (-lssd) (Photon) | 16 | 64 | 12.33 | 2.4650 |
| c4a-standard-32 (-lssd) (Photon) | 32 | 128 | 24.65 | 4.9300 |
| c4a-standard-4 (-lssd) (Photon) | 4 | 16 | 3.08 | 0.6150 |
| c4a-standard-48 (-lssd) (Photon) | 48 | 192 | 36.95 | 7.3900 |
| c4a-standard-64 (-lssd) (Photon) | 64 | 256 | 49.28 | 9.8550 |
| c4a-standard-72 (-lssd) (Photon) | 72 | 288 | 55.45 | 11.0900 |
| c4a-standard-8 (-lssd) (Photon) | 8 | 32 | 6.15 | 1.2300 |
| e2_standard_16 (Photon) | 16 | 64 | 7.2 | 1.4400 |
| e2_standard_32 (Photon) | 32 | 128 | 14.4 | 2.8800 |
| e2_standard_4 (Photon) | 4 | 16 | 1.8 | 0.3600 |
| e2_standard_8 (Photon) | 8 | 32 | 3.6 | 0.7200 |
| n2-highmem-16 (Photon) | 16 | 128 | 9.6 | 1.9200 |
| n2-highmem-2 (Photon) | 2 | 16 | 1.2 | 0.2400 |
| n2-highmem-32 (Photon) | 32 | 256 | 19.2 | 3.8400 |
| n2-highmem-4 (Photon) | 4 | 32 | 2.4 | 0.4800 |
| n2-highmem-48 (Photon) | 48 | 384 | 28.8 | 5.7600 |
| n2-highmem-64 (Photon) | 64 | 512 | 38.4 | 7.6800 |
| n2-highmem-8 (Photon) | 8 | 64 | 4.8 | 0.9600 |
| n2-highmem-80 (Photon) | 80 | 640 | 48 | 9.6000 |
| n2-standard-16 (Photon) | 16 | 64 | 7.2 | 1.4400 |
| n2-standard-32 (Photon) | 32 | 128 | 14.4 | 2.8800 |
| n2-standard-4 (Photon) | 4 | 16 | 1.8 | 0.3600 |
| n2-standard-48 (Photon) | 48 | 192 | 21.6 | 4.3200 |
| n2-standard-64 (Photon) | 64 | 256 | 28.8 | 5.7600 |
| n2-standard-8 (Photon) | 8 | 32 | 3.6 | 0.7200 |
| n2-standard-80 (Photon) | 80 | 320 | 36 | 7.2000 |
| n2d-highmem-16 (Photon) | 16 | 128 | 9.6 | 1.9200 |
| n2d-highmem-2 (Photon) | 2 | 16 | 1.2 | 0.2400 |
| n2d-highmem-32 (Photon) | 32 | 256 | 19.2 | 3.8400 |
| n2d-highmem-4 (Photon) | 4 | 32 | 2.4 | 0.4800 |
| n2d-highmem-48 (Photon) | 48 | 384 | 28.8 | 5.7600 |
| n2d-highmem-64 (Photon) | 64 | 512 | 38.4 | 7.6800 |
| n2d-highmem-8 (Photon) | 8 | 64 | 4.8 | 0.9600 |
| n2d-highmem-80 (Photon) | 80 | 640 | 48 | 9.6000 |
| n2d-highmem-96 (Photon) | 96 | 768 | 57.6 | 11.5200 |
| n2d-standard-128 (Photon) | 128 | 512 | 57.6 | 11.5200 |
| n2d-standard-16 (Photon) | 16 | 64 | 7.2 | 1.4400 |
| n2d-standard-224 (Photon) | 224 | 896 | 100.8 | 20.1600 |
| n2d-standard-32 (Photon) | 32 | 128 | 14.4 | 2.8800 |
| n2d-standard-4 (Photon) | 4 | 16 | 1.8 | 0.3600 |
| n2d-standard-48 (Photon) | 48 | 192 | 21.6 | 4.3200 |
| n2d-standard-64 (Photon) | 64 | 256 | 28.8 | 5.7600 |
| n2d-standard-8 (Photon) | 8 | 32 | 3.6 | 0.7200 |
| n2d-standard-80 (Photon) | 80 | 320 | 36 | 7.2000 |
| n2d-standard-96 (Photon) | 96 | 384 | 43.2 | 8.6400 |
