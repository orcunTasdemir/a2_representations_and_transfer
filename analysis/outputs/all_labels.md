All 2000 training labels, dev MSE (MPa²), mean ± SD over 5 inner seeds (RMSE in MPa in brackets). The SD does not include label-draw variation.

| Method | n = 2000 | Runs/cell |
|---|---:|---:|
| Ridge on the 160 raw gauges (incumbent) | 46.9 ± 0.2 (6.8) | 5 |
| Frozen pre-trained encoder + ridge | 8.5 ± 2.1 (2.9) | 15 |
| Frozen random encoder + ridge (control) | 15.7 ± 0.0 (4.0) | 5 |
| Network from scratch | 3.0 ± 0.1 (1.7) | 5 |
| Fine-tuned encoder | 3.1 ± 0.2 (1.7) | 5 |
| Reference: predict the mean of the n labels, no gauges | 188.9 ± 0.0 (13.7) | 5 |
