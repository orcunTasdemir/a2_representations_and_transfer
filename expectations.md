# Expectations, written before Exhibit 1 was run

Written by me before any model in the table was fitted. The only number known
at the time: predicting the mean strength scores **MSE 188.9 MPa²** on dev
(RMSE 13.7 MPa). Every error below is dev MSE in MPa²; lower is better, 0 is
perfect, 188.9 is "the gauges told us nothing".

Not a deliverable. Kept so the table has something to be compared against,
and as evidence for the process note.

---

## 1. Ridge on the 160 raw gauges (the incumbent)

- At n = 50, roughly where? Above or below 188.9?
- At n = 1000?
- Shape from 50 → 1000: keeps falling, or flattens? Why?

>

## 2. Frozen pre-trained encoder + ridge

- Better or worse than raw ridge at n = 50? At n = 1000? Why?

>

## 3. Frozen random encoder + ridge (the control)

- Closer to row 1 or to row 2? What would each outcome mean?

>

## 4. Network from scratch

- At n = 50 (it trains on 37, early-stops on 13)?
- At n = 1000, against raw ridge at n = 1000?

>

## 5. Fine-tuned encoder

- Against scratch at the same n: where does starting from the encoder help most?
- Against the frozen encoder: where does letting the encoder adjust pay off?

>

## 6. Spread (standard deviations)

- Which label count will have the largest SDs? Which row?

>

## 7. Crossover

- Frozen encoder vs scratch: does the ordering flip? Between which label counts?

>

## 8. What would look too good, or wrong

- What result would make me suspect a bug rather than believe it?

>
