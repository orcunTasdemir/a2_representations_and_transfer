Exhibit 1. Dev MSE (MPa²), mean ± SD over runs. Lower is better.

| Method | n = 50 | n = 100 | n = 250 | n = 1000 | Runs/cell |
|---|---:|---:|---:|---:|---:|
| Ridge on the 160 raw gauges (incumbent) | 60.7 ± 5.6 | 56.5 ± 6.3 | 48.2 ± 0.6 | 47.5 ± 0.4 | 5 |
| Frozen pre-trained encoder + ridge | 33.5 ± 12.0 | 17.6 ± 5.4 | 10.8 ± 2.9 | 8.9 ± 2.3 | 15 |
| Frozen random encoder + ridge (control) | 39.2 ± 6.6 | 25.6 ± 3.5 | 18.6 ± 0.8 | 16.0 ± 0.2 | 5 |
| Network from scratch | 47.0 ± 17.8 | 23.3 ± 9.4 | 7.8 ± 1.5 | 3.5 ± 0.1 | 5 |
| Fine-tuned encoder | 45.2 ± 21.1 | 21.3 ± 5.0 | 7.2 ± 0.5 | 3.6 ± 0.3 | 5 |
| Reference: predict the mean of the n labels, no gauges | 190.2 ± 2.5 | 189.4 ± 0.6 | 189.4 ± 0.3 | 188.9 ± 0.1 | 5 |
