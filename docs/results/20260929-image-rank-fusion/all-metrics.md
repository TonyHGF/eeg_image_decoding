# Paired image/text rank fusion

Exploratory follow-up using one validation-best checkpoint per backend. No retraining.
All branches vote on the same image/caption ID. C/L are selected by validation only.
Validation: 740 queries, each with its positive plus 199 fixed distractors from validation.
Test: 200 queries against all 200 test pairs. Values: subject mean ± sample SD (%).
These are single-checkpoint baselines, distinct from the prior three-checkpoint metric averages.

| Split | Method | Top-1 | Top-5 | Top-10 |
|---|---|---:|---:|---:|
| val | two_images_equal_C1_L5 | 37.122 ± 7.460 | 69.041 ± 7.813 | 80.568 ± 6.007 |
| val | two_images_equal_C1_L10 | 37.311 ± 7.320 | 69.932 ± 7.539 | 80.203 ± 6.366 |
| val | two_images_equal_C4-3_L5 | 37.135 ± 7.436 | 69.054 ± 7.837 | 80.568 ± 6.007 |
| val | two_images_equal_C4-3_L10 | 37.311 ± 7.364 | 69.932 ± 7.545 | 80.203 ± 6.366 |
| val | two_images_equal_C5-3_L5 | 37.135 ± 7.474 | 69.054 ± 7.837 | 80.568 ± 6.007 |
| val | two_images_equal_C5-3_L10 | 37.351 ± 7.357 | 69.973 ± 7.588 | 80.189 ± 6.367 |
| val | two_images_equal_C2_L5 | 36.973 ± 7.800 | 69.054 ± 7.837 | 80.568 ± 6.007 |
| val | two_images_equal_C2_L10 | 37.135 ± 7.531 | 70.108 ± 7.631 | 80.189 ± 6.367 |
| val | cn_image | 34.784 ± 7.857 | 65.486 ± 7.639 | 77.459 ± 6.627 |
| val | cn_text | 8.392 ± 1.972 | 24.824 ± 3.231 | 36.649 ± 4.548 |
| val | openai_image | 33.027 ± 6.236 | 64.784 ± 7.297 | 76.392 ± 6.399 |
| val | openai_text | 11.811 ± 2.489 | 33.378 ± 5.208 | 48.041 ± 6.014 |
| test | two_images_equal_C1_L5 | 52.950 ± 7.872 | 86.000 ± 4.944 | 93.250 ± 2.751 |
| test | two_images_equal_C1_L10 | 53.050 ± 8.153 | 86.000 ± 4.927 | 93.350 ± 3.154 |
| test | two_images_equal_C4-3_L5 | 52.950 ± 7.872 | 86.000 ± 4.944 | 93.250 ± 2.751 |
| test | two_images_equal_C4-3_L10 | 53.000 ± 7.969 | 85.800 ± 4.785 | 93.350 ± 3.154 |
| test | two_images_equal_C5-3_L5 | 52.950 ± 7.872 | 86.000 ± 4.944 | 93.250 ± 2.751 |
| test | two_images_equal_C5-3_L10 | 53.000 ± 7.832 | 85.650 ± 5.011 | 93.350 ± 3.154 |
| test | two_images_equal_C2_L5 | 52.600 ± 7.763 | 86.000 ± 4.944 | 93.250 ± 2.751 |
| test | two_images_equal_C2_L10 | 52.700 ± 7.685 | 85.500 ± 5.033 | 93.300 ± 3.164 |
| test | cn_image | 50.350 ± 7.990 | 82.100 ± 5.232 | 90.550 ± 3.476 |
| test | cn_text | 10.800 ± 2.627 | 31.550 ± 4.930 | 44.900 ± 4.909 |
| test | openai_image | 47.300 ± 6.804 | 80.500 ± 4.933 | 89.000 ± 3.771 |
| test | openai_text | 17.600 ± 3.098 | 44.700 ± 5.095 | 60.950 ± 6.274 |

Validation-selected methods:

- two_images_equal: two_images_equal_C5-3_L10
- Global validation selection: two_images_equal_C5-3_L10

Ties: vote rounded to 12 decimals, then lower weighted mean full rank, then candidate ID.
All per-query selected image/caption pairs and contributing branch ranks are in paired_predictions.csv.
