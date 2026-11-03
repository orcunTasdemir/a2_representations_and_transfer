Exhibit 1. Dev MSE (MPa²), mean ± SD over runs. Lower is better.

| Method | n = 50 | n = 100 | n = 250 | n = 1000 | Runs/cell |
|---|---:|---:|---:|---:|---:|
| Ridge on the 160 raw gauges (incumbent) | 60.7 ± 5.6 | 56.5 ± 6.3 | 48.2 ± 0.6 | 47.5 ± 0.4 | 5 |
| Frozen pre-trained encoder + ridge | 33.5 ± 12.0 | 17.6 ± 5.4 | 10.8 ± 2.9 | 8.9 ± 2.3 | 15 |
| Frozen random encoder + ridge (control) | 39.2 ± 6.6 | 25.6 ± 3.5 | 18.6 ± 0.8 | 16.0 ± 0.2 | 5 |
| Network from scratch | 47.0 ± 17.8 | 23.3 ± 9.4 | 7.8 ± 1.5 | 3.5 ± 0.1 | 5 |
| Fine-tuned encoder | 45.2 ± 21.1 | 21.3 ± 5.0 | 7.2 ± 0.5 | 3.6 ± 0.3 | 5 |
| Reference: predict the mean of the n labels, no gauges | 190.2 ± 2.5 | 189.4 ± 0.6 | 189.4 ± 0.3 | 188.9 ± 0.1 | 5 |

With RMSE in MPa (square root of the mean MSE: the typical miss) in brackets:

| Method | n = 50 | n = 100 | n = 250 | n = 1000 | Runs/cell |
|---|---:|---:|---:|---:|---:|
| Ridge on the 160 raw gauges (incumbent) | 60.7 ± 5.6 (7.8) | 56.5 ± 6.3 (7.5) | 48.2 ± 0.6 (6.9) | 47.5 ± 0.4 (6.9) | 5 |
| Frozen pre-trained encoder + ridge | 33.5 ± 12.0 (5.8) | 17.6 ± 5.4 (4.2) | 10.8 ± 2.9 (3.3) | 8.9 ± 2.3 (3.0) | 15 |
| Frozen random encoder + ridge (control) | 39.2 ± 6.6 (6.3) | 25.6 ± 3.5 (5.1) | 18.6 ± 0.8 (4.3) | 16.0 ± 0.2 (4.0) | 5 |
| Network from scratch | 47.0 ± 17.8 (6.9) | 23.3 ± 9.4 (4.8) | 7.8 ± 1.5 (2.8) | 3.5 ± 0.1 (1.9) | 5 |
| Fine-tuned encoder | 45.2 ± 21.1 (6.7) | 21.3 ± 5.0 (4.6) | 7.2 ± 0.5 (2.7) | 3.6 ± 0.3 (1.9) | 5 |
| Reference: predict the mean of the n labels, no gauges | 190.2 ± 2.5 (13.8) | 189.4 ± 0.6 (13.8) | 189.4 ± 0.3 (13.8) | 188.9 ± 0.1 (13.7) | 5 |
