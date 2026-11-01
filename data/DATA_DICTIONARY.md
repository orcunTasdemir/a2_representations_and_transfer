# Kestrel Composites — data dictionary

Extract prepared by Process Engineering, September 2026.

**Grain.** One row per cured panel.

---

## The gauges (160 columns, identical in every file)

Every panel is cured in an autoclave instrumented with 160 gauges. All 160 are logged automatically for every panel, whether or not that panel is ever tested.

| Block | Columns | What it reads |
|---|---|---|
| Oven zone temperature | `cure_temp_z01` … `cure_temp_z40` | Thermocouples distributed through the oven, °C |
| Tool pressure | `press_p01` … `press_p32` | Pressure taps under the vacuum bag, kPa |
| Resin flow | `resin_flow_f01` … `resin_flow_f32` | Flow-front gauges around the tool, arbitrary units |
| Dielectric cure monitor | `dielectric_d01` … `dielectric_d32` | Ion-viscosity probes tracking the cure reaction |
| Vacuum line | `vacuum_v01` … `vacuum_v24` | Line pressures at the bag ports, kPa |

The gauges are **highly redundant**. They are 160 different views of a much smaller number of underlying process conditions — how hot the part actually got, how fast it got there, how completely the resin flowed, how much contamination was present. Two gauges on opposite sides of the same oven zone tell you nearly the same thing. This redundancy is why a gauge that drops out can be reconstructed from the others, and it is worth keeping in mind when you look at what pre-training does.

## The identifier and the target

| Column | Definition |
|---|---|
| `panel_id` | Panel identifier, unique across all four files. The prefix says which file a panel is in: `TR` train, `DV` dev, `TS` test, `UL` unlabelled. |
| `strength_mpa` | **Target.** Interlaminar shear strength, MPa. Measured by loading the panel to failure in a press. Present only in the three `labeled_*` files. |

Measuring it destroys the panel. That is the whole problem: a labelled row costs a saleable part plus about four hours of lab time, and an unlabelled row costs nothing at all.

**A note on negative values.** About 1–2% of labelled panels show a strength below zero, which no real panel can have. Like every dataset in this course, this extract is simulated, and those values come from the simulation's severe-contamination term rather than from a measurement. Leave them in: they are the badly delaminated panels, and the prescribed models and every comparison in the brief are computed with them included.

## What Process Engineering says about strength

> Strength needs two things to go right at once. The resin has to flow far enough to wet out every ply, and the cure has to run far enough to convert the matrix. A panel that is beautifully wetted but under-cured is weak. A panel that is fully cured but resin-starved is weak in a different way. **You cannot make up for a deficit in one with a surplus in the other** — the two failure modes multiply rather than add.
>
> Separately, contamination above a threshold causes delamination. Below the threshold it does nothing measurable; above it, strength falls away sharply.

That paragraph is a description of the physics, not a hint about modelling. It is here because it is what the process engineers would tell you, and it is relevant to at least one thing you will observe.

---

## The files

| File | Rows | Labelled | Use |
|---|---|---|---|
| `labeled_train.csv` | 2,000 | yes | fitting |
| `labeled_dev.csv` | 1,000 | yes | every comparison you make |
| `labeled_test.csv` | 1,000 | yes | scored once, at the end |
| `unlabeled_traces.csv.gz` | 20,000 | no | pre-training |

All four come from the same autoclave and the same period. No panel appears in more than one file. The unlabelled file is gzipped; `pandas.read_csv` opens it directly, and `starter/kestrel.py` already does.

`dev` and `test` are interchangeable except in what you are allowed to do with them: `dev` is where you compare things, `test` is scored once on whatever you end up recommending. They are not equally hard — `var(y)` is about 10% lower on `test` — so expect a small difference and report it rather than accounting for it.
