# Paired image/text rank fusion

Exploratory follow-up using one validation-best checkpoint per backend. No retraining.
All branches vote on the same image/caption ID. C/L are selected by validation only.
Validation: 740 queries, each with its positive plus 199 fixed distractors from validation.
Test: 200 queries against all 200 test pairs. Values: subject mean ± sample SD (%).
These are single-checkpoint baselines, distinct from the prior three-checkpoint metric averages.

| Split | Method | Top-1 | Top-5 | Top-10 |
|---|---|---:|---:|---:|
| val | image_text_equal_C1_L5 | 26.108 ± 5.902 | 60.216 ± 7.854 | 73.149 ± 6.457 |
| val | image_text_equal_C1_L10 | 26.459 ± 6.195 | 60.649 ± 7.901 | 73.081 ± 6.888 |
| val | image_text_equal_C4-3_L5 | 26.041 ± 5.919 | 60.216 ± 7.854 | 73.149 ± 6.457 |
| val | image_text_equal_C4-3_L10 | 26.432 ± 6.146 | 60.716 ± 7.887 | 73.081 ± 6.888 |
| val | image_text_equal_C5-3_L5 | 25.703 ± 5.857 | 60.216 ± 7.854 | 73.149 ± 6.457 |
| val | image_text_equal_C5-3_L10 | 26.203 ± 5.855 | 60.703 ± 7.794 | 73.081 ± 6.888 |
| val | image_text_equal_C2_L5 | 25.270 ± 5.524 | 60.216 ± 7.854 | 73.149 ± 6.457 |
| val | image_text_equal_C2_L10 | 25.878 ± 5.411 | 60.500 ± 7.702 | 73.081 ± 6.888 |
| val | four_equal_C1_L5 | 31.054 ± 6.209 | 63.514 ± 7.360 | 74.392 ± 6.706 |
| val | four_equal_C1_L10 | 31.014 ± 6.061 | 64.027 ± 7.342 | 75.797 ± 6.978 |
| val | four_equal_C4-3_L5 | 30.919 ± 6.231 | 63.527 ± 7.410 | 74.392 ± 6.706 |
| val | four_equal_C4-3_L10 | 30.824 ± 5.990 | 64.189 ± 7.561 | 75.851 ± 6.998 |
| val | four_equal_C5-3_L5 | 30.500 ± 5.901 | 63.716 ± 7.418 | 74.392 ± 6.706 |
| val | four_equal_C5-3_L10 | 30.568 ± 5.950 | 64.338 ± 7.682 | 75.851 ± 6.910 |
| val | four_equal_C2_L5 | 30.243 ± 5.634 | 63.946 ± 7.402 | 74.392 ± 6.706 |
| val | four_equal_C2_L10 | 30.243 ± 5.902 | 64.486 ± 7.740 | 76.027 ± 6.862 |
| val | cn_image | 34.784 ± 7.857 | 65.486 ± 7.639 | 77.459 ± 6.627 |
| val | cn_text | 8.392 ± 1.972 | 24.824 ± 3.231 | 36.649 ± 4.548 |
| val | openai_image | 33.027 ± 6.236 | 64.784 ± 7.297 | 76.392 ± 6.399 |
| val | openai_text | 11.811 ± 2.489 | 33.378 ± 5.208 | 48.041 ± 6.014 |
| test | image_text_equal_C1_L5 | 38.250 ± 6.277 | 77.850 ± 5.986 | 88.250 ± 3.751 |
| test | image_text_equal_C1_L10 | 38.850 ± 5.888 | 78.400 ± 5.990 | 88.000 ± 4.096 |
| test | image_text_equal_C4-3_L5 | 38.250 ± 6.277 | 77.850 ± 5.986 | 88.250 ± 3.751 |
| test | image_text_equal_C4-3_L10 | 38.800 ± 5.846 | 78.150 ± 6.083 | 88.000 ± 4.096 |
| test | image_text_equal_C5-3_L5 | 37.700 ± 6.317 | 77.850 ± 5.986 | 88.250 ± 3.751 |
| test | image_text_equal_C5-3_L10 | 38.100 ± 5.763 | 78.200 ± 6.001 | 88.000 ± 4.096 |
| test | image_text_equal_C2_L5 | 37.200 ± 6.024 | 77.850 ± 5.986 | 88.250 ± 3.751 |
| test | image_text_equal_C2_L10 | 37.650 ± 5.788 | 78.050 ± 5.833 | 88.000 ± 4.096 |
| test | four_equal_C1_L5 | 43.900 ± 7.074 | 80.750 ± 4.861 | 89.650 ± 4.416 |
| test | four_equal_C1_L10 | 44.000 ± 7.528 | 81.350 ± 5.056 | 90.450 ± 3.752 |
| test | four_equal_C4-3_L5 | 44.000 ± 7.102 | 80.850 ± 4.905 | 89.650 ± 4.416 |
| test | four_equal_C4-3_L10 | 43.650 ± 7.315 | 81.200 ± 4.928 | 90.450 ± 3.662 |
| test | four_equal_C5-3_L5 | 43.300 ± 7.029 | 80.700 ± 4.951 | 89.650 ± 4.416 |
| test | four_equal_C5-3_L10 | 43.000 ± 6.758 | 81.450 ± 4.764 | 90.450 ± 3.452 |
| test | four_equal_C2_L5 | 42.400 ± 6.616 | 80.500 ± 4.732 | 89.650 ± 4.416 |
| test | four_equal_C2_L10 | 42.500 ± 6.778 | 81.200 ± 4.442 | 90.500 ± 3.488 |
| test | cn_image | 50.350 ± 7.990 | 82.100 ± 5.232 | 90.550 ± 3.476 |
| test | cn_text | 10.800 ± 2.627 | 31.550 ± 4.930 | 44.900 ± 4.909 |
| test | openai_image | 47.300 ± 6.804 | 80.500 ± 4.933 | 89.000 ± 3.771 |
| test | openai_text | 17.600 ± 3.098 | 44.700 ± 5.095 | 60.950 ± 6.274 |

Validation-selected methods:

- image_text_equal: image_text_equal_C1_L10
- four_equal: four_equal_C1_L5
- Global validation selection: four_equal_C1_L5

Ties: vote rounded to 12 decimals, then lower weighted mean full rank, then candidate ID.
All per-query selected image/caption pairs and contributing branch ranks are in paired_predictions.csv.
