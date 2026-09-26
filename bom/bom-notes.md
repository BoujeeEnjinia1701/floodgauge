# BOM notes

- Costs are indicative, at quantity 1, in USD. Every line is priced; supplier types are given where no supplier is chosen. Only the A02YYUW list price ($15.90, DFRobot product page) was checked on 2026-09-25; the radar module and housing prices are not verified.
- Item numbers 1 to 8 match the callouts in `media/exploded.png` and the parts in `cad/src/model.py`. Items 9 and 10 are not modeled.
- Under FLG-DDR-001 D1 (adopted for TRL 3 pending Amish's review), the FieldNode core is costed in the FieldNode repo ($126.00, FND-CAL-001) and R16 covers FloodGauge-specific parts only. Line 1 stays in this BOM for the complete-gauge total.
- FloodGauge-specific parts (lines 2 to 10): $145.50 against `budget_usd` $150, a margin of $4.50. Complete gauge with FieldNode: $271.50. Both are printed by `docs/04-calcs/sizing.py` [M1].
- Change from TRL 2: a 10 kΩ NTC ($0.50) added to the drain head for speed-of-sound compensation (FLG-CAL-001, C2).
- Not included: the LoRaWAN gateway, installation labor, coring the basin wall, trenching, traffic management and any permits.
- A street-only variant with an ultrasonic street head and no drain parts would cost about $188 (TRL 2 estimate, not rechecked) and misses R2.
