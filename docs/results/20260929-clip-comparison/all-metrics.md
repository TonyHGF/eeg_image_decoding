# CLIP comparison: completed conditions

This report includes only the complete conditions listed below. Scheduler success
and feature/caption provenance must also be verified in the run record.

Values are mean ± sample SD across ten subjects, in percent. One seed only.
Each subject value averages metrics from three validation-selected checkpoints;
this is not prediction ensembling. Text metrics are caption retrieval.

CN-cached uses original repository features with shared runtime/evaluation fixes.
CN-shared versus OpenAI-shared isolates the encoder with identical new captions.
Comparisons involving CN-cached also include caption differences.

## All accuracy metrics

| Condition | Metric | Mean ± SD (%) |
|---|---|---:|
| cn-cached | retrieval_topk_1 | 50.267 ± 7.836 |
| cn-cached | retrieval_topk_2 | 65.600 ± 7.395 |
| cn-cached | retrieval_topk_3 | 73.467 ± 6.910 |
| cn-cached | retrieval_topk_4 | 78.317 ± 6.653 |
| cn-cached | retrieval_topk_5 | 81.383 ± 6.111 |
| cn-cached | retrieval_topk_6 | 83.967 ± 5.605 |
| cn-cached | retrieval_topk_7 | 86.000 ± 4.914 |
| cn-cached | retrieval_topk_8 | 87.600 ± 4.558 |
| cn-cached | retrieval_topk_9 | 88.883 ± 4.403 |
| cn-cached | retrieval_topk_10 | 90.183 ± 3.823 |
| cn-cached | text_topk_1 | 7.650 ± 1.500 |
| cn-cached | text_topk_2 | 13.817 ± 2.623 |
| cn-cached | text_topk_3 | 18.567 ± 3.178 |
| cn-cached | text_topk_4 | 22.733 ± 3.414 |
| cn-cached | text_topk_5 | 26.000 ± 3.415 |
| cn-cached | text_topk_6 | 29.400 ± 3.724 |
| cn-cached | text_topk_7 | 32.250 ± 3.495 |
| cn-cached | text_topk_8 | 34.983 ± 2.909 |
| cn-cached | text_topk_9 | 37.667 ± 2.955 |
| cn-cached | text_topk_10 | 39.833 ± 3.120 |
| cn-cached | retrieval_way_2 | 98.217 ± 0.699 |
| cn-cached | retrieval_way_4 | 96.383 ± 1.887 |
| cn-cached | retrieval_way_10 | 88.817 ± 4.266 |
| cn-cached | retrieval_way_20 | 82.917 ± 4.744 |
| cn-cached | retrieval_way_50 | 70.800 ± 7.569 |
| cn-cached | retrieval_way_100 | 61.183 ± 6.989 |
| cn-cached | text_way_2 | 84.283 ± 1.986 |
| cn-cached | text_way_4 | 67.617 ± 3.408 |
| cn-cached | text_way_10 | 46.850 ± 2.480 |
| cn-cached | text_way_20 | 32.783 ± 2.046 |
| cn-cached | text_way_50 | 20.550 ± 3.556 |
| cn-cached | text_way_100 | 14.100 ± 2.455 |
| cn-shared | retrieval_topk_1 | 50.117 ± 8.113 |
| cn-shared | retrieval_topk_2 | 65.700 ± 7.615 |
| cn-shared | retrieval_topk_3 | 73.783 ± 7.337 |
| cn-shared | retrieval_topk_4 | 78.517 ± 6.483 |
| cn-shared | retrieval_topk_5 | 81.633 ± 5.870 |
| cn-shared | retrieval_topk_6 | 84.017 ± 5.338 |
| cn-shared | retrieval_topk_7 | 85.917 ± 4.848 |
| cn-shared | retrieval_topk_8 | 87.567 ± 4.489 |
| cn-shared | retrieval_topk_9 | 89.050 ± 3.937 |
| cn-shared | retrieval_topk_10 | 90.333 ± 3.497 |
| cn-shared | text_topk_1 | 10.933 ± 2.559 |
| cn-shared | text_topk_2 | 17.750 ± 2.752 |
| cn-shared | text_topk_3 | 23.183 ± 3.681 |
| cn-shared | text_topk_4 | 27.683 ± 4.617 |
| cn-shared | text_topk_5 | 31.600 ± 4.891 |
| cn-shared | text_topk_6 | 34.900 ± 4.792 |
| cn-shared | text_topk_7 | 37.500 ± 4.573 |
| cn-shared | text_topk_8 | 39.783 ± 4.648 |
| cn-shared | text_topk_9 | 42.083 ± 4.895 |
| cn-shared | text_topk_10 | 44.450 ± 5.070 |
| cn-shared | retrieval_way_2 | 98.300 ± 0.781 |
| cn-shared | retrieval_way_4 | 96.050 ± 1.879 |
| cn-shared | retrieval_way_10 | 89.250 ± 4.105 |
| cn-shared | retrieval_way_20 | 82.733 ± 5.057 |
| cn-shared | retrieval_way_50 | 71.083 ± 7.653 |
| cn-shared | retrieval_way_100 | 61.900 ± 7.748 |
| cn-shared | text_way_2 | 87.000 ± 2.772 |
| cn-shared | text_way_4 | 72.317 ± 3.803 |
| cn-shared | text_way_10 | 53.000 ± 4.821 |
| cn-shared | text_way_20 | 38.567 ± 4.016 |
| cn-shared | text_way_50 | 25.017 ± 4.599 |
| cn-shared | text_way_100 | 17.617 ± 2.643 |
| openai-shared | retrieval_topk_1 | 47.283 ± 5.979 |
| openai-shared | retrieval_topk_2 | 62.883 ± 5.626 |
| openai-shared | retrieval_topk_3 | 70.900 ± 5.465 |
| openai-shared | retrieval_topk_4 | 76.950 ± 4.789 |
| openai-shared | retrieval_topk_5 | 80.733 ± 4.325 |
| openai-shared | retrieval_topk_6 | 83.417 ± 4.045 |
| openai-shared | retrieval_topk_7 | 85.433 ± 3.784 |
| openai-shared | retrieval_topk_8 | 87.033 ± 3.415 |
| openai-shared | retrieval_topk_9 | 88.217 ± 3.248 |
| openai-shared | retrieval_topk_10 | 89.267 ± 3.183 |
| openai-shared | text_topk_1 | 17.283 ± 3.068 |
| openai-shared | text_topk_2 | 26.817 ± 3.807 |
| openai-shared | text_topk_3 | 33.450 ± 4.511 |
| openai-shared | text_topk_4 | 39.483 ± 4.770 |
| openai-shared | text_topk_5 | 44.300 ± 5.048 |
| openai-shared | text_topk_6 | 48.233 ± 5.589 |
| openai-shared | text_topk_7 | 51.850 ± 5.397 |
| openai-shared | text_topk_8 | 55.100 ± 5.908 |
| openai-shared | text_topk_9 | 57.900 ± 6.337 |
| openai-shared | text_topk_10 | 60.900 ± 6.440 |
| openai-shared | retrieval_way_2 | 98.333 ± 0.749 |
| openai-shared | retrieval_way_4 | 95.433 ± 2.168 |
| openai-shared | retrieval_way_10 | 89.400 ± 2.268 |
| openai-shared | retrieval_way_20 | 79.300 ± 3.446 |
| openai-shared | retrieval_way_50 | 69.600 ± 5.824 |
| openai-shared | retrieval_way_100 | 57.950 ± 6.199 |
| openai-shared | text_way_2 | 92.583 ± 2.189 |
| openai-shared | text_way_4 | 83.150 ± 3.754 |
| openai-shared | text_way_10 | 66.100 ± 4.249 |
| openai-shared | text_way_20 | 50.817 ± 5.603 |
| openai-shared | text_way_50 | 35.767 ± 4.421 |
| openai-shared | text_way_100 | 25.117 ± 4.290 |

## Training and selected checkpoints

| Condition | Subject | Epochs | Selected epochs (zero based) | Best val loss | Seconds | Peak allocated GPU GiB |
|---|---:|---:|---|---:|---:|---:|
| cn-cached | 1 | 104 | 88;94;85 | 3.991578 | 281.63 | 8.804 |
| cn-cached | 2 | 99 | 82;89;77 | 4.181811 | 279.92 | 8.806 |
| cn-cached | 3 | 113 | 87;103;96 | 3.995017 | 321.22 | 8.804 |
| cn-cached | 4 | 103 | 93;83;91 | 3.853197 | 285.04 | 8.804 |
| cn-cached | 5 | 106 | 96;87;75 | 4.537310 | 303.45 | 8.804 |
| cn-cached | 6 | 119 | 102;107;109 | 4.040731 | 337.45 | 8.804 |
| cn-cached | 7 | 132 | 114;109;122 | 3.865896 | 376.34 | 8.803 |
| cn-cached | 8 | 133 | 114;100;123 | 3.452299 | 375.73 | 8.803 |
| cn-cached | 9 | 90 | 64;78;80 | 4.315086 | 266.18 | 8.804 |
| cn-cached | 10 | 124 | 95;114;79 | 3.403207 | 351.00 | 8.804 |
| cn-shared | 1 | 100 | 88;90;84 | 3.943151 | 275.95 | 8.805 |
| cn-shared | 2 | 99 | 82;89;77 | 4.144448 | 283.97 | 8.806 |
| cn-shared | 3 | 112 | 87;96;102 | 3.944502 | 299.81 | 8.806 |
| cn-shared | 4 | 101 | 85;91;88 | 3.800133 | 279.66 | 8.803 |
| cn-shared | 5 | 106 | 87;96;89 | 4.476930 | 289.28 | 8.806 |
| cn-shared | 6 | 119 | 93;102;109 | 3.975912 | 324.46 | 8.804 |
| cn-shared | 7 | 137 | 114;127;120 | 3.791204 | 363.97 | 8.804 |
| cn-shared | 8 | 128 | 114;100;118 | 3.387900 | 347.45 | 8.804 |
| cn-shared | 9 | 88 | 78;64;74 | 4.271143 | 245.10 | 8.807 |
| cn-shared | 10 | 124 | 114;95;107 | 3.351872 | 334.50 | 8.806 |
| openai-shared | 1 | 107 | 97;94;73 | 3.944729 | 275.23 | 8.805 |
| openai-shared | 2 | 74 | 57;62;64 | 3.997723 | 207.35 | 8.807 |
| openai-shared | 3 | 102 | 84;74;92 | 3.944168 | 278.15 | 8.804 |
| openai-shared | 4 | 98 | 88;79;86 | 3.764496 | 268.39 | 8.806 |
| openai-shared | 5 | 98 | 75;79;88 | 4.354298 | 268.85 | 8.805 |
| openai-shared | 6 | 96 | 86;78;82 | 3.867184 | 263.68 | 8.808 |
| openai-shared | 7 | 111 | 85;101;86 | 3.735909 | 301.86 | 8.804 |
| openai-shared | 8 | 107 | 96;97;92 | 3.363514 | 289.30 | 8.807 |
| openai-shared | 9 | 72 | 62;58;56 | 4.166625 | 191.27 | 8.805 |
| openai-shared | 10 | 98 | 88;82;79 | 3.310987 | 254.22 | 8.806 |

## Paired differences

Positive values favor the first named condition. Units: percentage points.

| Comparison | Metric | Mean ± SD (pp) |
|---|---|---:|
| openai-shared minus cn-shared | retrieval_topk_1 | -2.833 ± 3.700 |
| openai-shared minus cn-shared | retrieval_topk_2 | -2.817 ± 3.514 |
| openai-shared minus cn-shared | retrieval_topk_3 | -2.883 ± 2.935 |
| openai-shared minus cn-shared | retrieval_topk_4 | -1.567 ± 2.390 |
| openai-shared minus cn-shared | retrieval_topk_5 | -0.900 ± 2.536 |
| openai-shared minus cn-shared | retrieval_topk_6 | -0.600 ± 2.372 |
| openai-shared minus cn-shared | retrieval_topk_7 | -0.483 ± 2.135 |
| openai-shared minus cn-shared | retrieval_topk_8 | -0.533 ± 2.024 |
| openai-shared minus cn-shared | retrieval_topk_9 | -0.833 ± 1.849 |
| openai-shared minus cn-shared | retrieval_topk_10 | -1.067 ± 1.819 |
| openai-shared minus cn-shared | text_topk_1 | 6.350 ± 1.758 |
| openai-shared minus cn-shared | text_topk_2 | 9.067 ± 2.640 |
| openai-shared minus cn-shared | text_topk_3 | 10.267 ± 3.550 |
| openai-shared minus cn-shared | text_topk_4 | 11.800 ± 3.533 |
| openai-shared minus cn-shared | text_topk_5 | 12.700 ± 2.997 |
| openai-shared minus cn-shared | text_topk_6 | 13.333 ± 2.510 |
| openai-shared minus cn-shared | text_topk_7 | 14.350 ± 2.563 |
| openai-shared minus cn-shared | text_topk_8 | 15.317 ± 3.479 |
| openai-shared minus cn-shared | text_topk_9 | 15.817 ± 3.598 |
| openai-shared minus cn-shared | text_topk_10 | 16.450 ± 3.933 |
| openai-shared minus cn-shared | retrieval_way_2 | 0.033 ± 0.888 |
| openai-shared minus cn-shared | retrieval_way_4 | -0.617 ± 1.604 |
| openai-shared minus cn-shared | retrieval_way_10 | 0.150 ± 2.679 |
| openai-shared minus cn-shared | retrieval_way_20 | -3.433 ± 2.842 |
| openai-shared minus cn-shared | retrieval_way_50 | -1.483 ± 3.724 |
| openai-shared minus cn-shared | retrieval_way_100 | -3.950 ± 2.922 |
| openai-shared minus cn-shared | text_way_2 | 5.583 ± 2.480 |
| openai-shared minus cn-shared | text_way_4 | 10.833 ± 3.376 |
| openai-shared minus cn-shared | text_way_10 | 13.100 ± 3.500 |
| openai-shared minus cn-shared | text_way_20 | 12.250 ± 3.853 |
| openai-shared minus cn-shared | text_way_50 | 10.750 ± 2.770 |
| openai-shared minus cn-shared | text_way_100 | 7.500 ± 2.945 |
| cn-shared minus cn-cached | retrieval_topk_1 | -0.150 ± 1.697 |
| cn-shared minus cn-cached | retrieval_topk_2 | 0.100 ± 1.556 |
| cn-shared minus cn-cached | retrieval_topk_3 | 0.317 ± 0.938 |
| cn-shared minus cn-cached | retrieval_topk_4 | 0.200 ± 1.188 |
| cn-shared minus cn-cached | retrieval_topk_5 | 0.250 ± 0.995 |
| cn-shared minus cn-cached | retrieval_topk_6 | 0.050 ± 0.839 |
| cn-shared minus cn-cached | retrieval_topk_7 | -0.083 ± 1.072 |
| cn-shared minus cn-cached | retrieval_topk_8 | -0.033 ± 1.024 |
| cn-shared minus cn-cached | retrieval_topk_9 | 0.167 ± 1.186 |
| cn-shared minus cn-cached | retrieval_topk_10 | 0.150 ± 0.951 |
| cn-shared minus cn-cached | text_topk_1 | 3.283 ± 1.734 |
| cn-shared minus cn-cached | text_topk_2 | 3.933 ± 0.950 |
| cn-shared minus cn-cached | text_topk_3 | 4.617 ± 1.423 |
| cn-shared minus cn-cached | text_topk_4 | 4.950 ± 2.070 |
| cn-shared minus cn-cached | text_topk_5 | 5.600 ± 2.692 |
| cn-shared minus cn-cached | text_topk_6 | 5.500 ± 2.822 |
| cn-shared minus cn-cached | text_topk_7 | 5.250 ± 2.725 |
| cn-shared minus cn-cached | text_topk_8 | 4.800 ± 3.398 |
| cn-shared minus cn-cached | text_topk_9 | 4.417 ± 3.231 |
| cn-shared minus cn-cached | text_topk_10 | 4.617 ± 3.541 |
| cn-shared minus cn-cached | retrieval_way_2 | 0.083 ± 0.425 |
| cn-shared minus cn-cached | retrieval_way_4 | -0.333 ± 0.416 |
| cn-shared minus cn-cached | retrieval_way_10 | 0.433 ± 0.763 |
| cn-shared minus cn-cached | retrieval_way_20 | -0.183 ± 1.292 |
| cn-shared minus cn-cached | retrieval_way_50 | 0.283 ± 1.493 |
| cn-shared minus cn-cached | retrieval_way_100 | 0.717 ± 1.406 |
| cn-shared minus cn-cached | text_way_2 | 2.717 ± 1.969 |
| cn-shared minus cn-cached | text_way_4 | 4.700 ± 3.287 |
| cn-shared minus cn-cached | text_way_10 | 6.150 ± 3.742 |
| cn-shared minus cn-cached | text_way_20 | 5.783 ± 3.423 |
| cn-shared minus cn-cached | text_way_50 | 4.467 ± 1.802 |
| cn-shared minus cn-cached | text_way_100 | 3.517 ± 2.177 |
| openai-shared minus cn-cached | retrieval_topk_1 | -2.983 ± 3.472 |
| openai-shared minus cn-cached | retrieval_topk_2 | -2.717 ± 3.718 |
| openai-shared minus cn-cached | retrieval_topk_3 | -2.567 ± 2.951 |
| openai-shared minus cn-cached | retrieval_topk_4 | -1.367 ± 2.481 |
| openai-shared minus cn-cached | retrieval_topk_5 | -0.650 ± 2.248 |
| openai-shared minus cn-cached | retrieval_topk_6 | -0.550 ± 2.321 |
| openai-shared minus cn-cached | retrieval_topk_7 | -0.567 ± 1.886 |
| openai-shared minus cn-cached | retrieval_topk_8 | -0.567 ± 1.881 |
| openai-shared minus cn-cached | retrieval_topk_9 | -0.667 ± 1.897 |
| openai-shared minus cn-cached | retrieval_topk_10 | -0.917 ± 1.823 |
| openai-shared minus cn-cached | text_topk_1 | 9.633 ± 2.400 |
| openai-shared minus cn-cached | text_topk_2 | 13.000 ± 2.582 |
| openai-shared minus cn-cached | text_topk_3 | 14.883 ± 3.559 |
| openai-shared minus cn-cached | text_topk_4 | 16.750 ± 2.840 |
| openai-shared minus cn-cached | text_topk_5 | 18.300 ± 2.706 |
| openai-shared minus cn-cached | text_topk_6 | 18.833 ± 2.845 |
| openai-shared minus cn-cached | text_topk_7 | 19.600 ± 2.604 |
| openai-shared minus cn-cached | text_topk_8 | 20.117 ± 3.649 |
| openai-shared minus cn-cached | text_topk_9 | 20.233 ± 4.149 |
| openai-shared minus cn-cached | text_topk_10 | 21.067 ± 4.546 |
| openai-shared minus cn-cached | retrieval_way_2 | 0.117 ± 0.868 |
| openai-shared minus cn-cached | retrieval_way_4 | -0.950 ± 1.495 |
| openai-shared minus cn-cached | retrieval_way_10 | 0.583 ± 2.891 |
| openai-shared minus cn-cached | retrieval_way_20 | -3.617 ± 2.618 |
| openai-shared minus cn-cached | retrieval_way_50 | -1.200 ± 3.746 |
| openai-shared minus cn-cached | retrieval_way_100 | -3.233 ± 2.790 |
| openai-shared minus cn-cached | text_way_2 | 8.300 ± 1.805 |
| openai-shared minus cn-cached | text_way_4 | 15.533 ± 2.212 |
| openai-shared minus cn-cached | text_way_10 | 19.250 ± 3.604 |
| openai-shared minus cn-cached | text_way_20 | 18.033 ± 4.011 |
| openai-shared minus cn-cached | text_way_50 | 15.217 ± 2.499 |
| openai-shared minus cn-cached | text_way_100 | 11.017 ± 2.868 |

## Shared configuration

```json
{
  "epoch": 150,
  "batch_size": 1000,
  "encoder_type": "HYBRID",
  "seed": 2023,
  "alpha": 0.1,
  "no_pretrain": false,
  "load_pretrain_groups": "ALL",
  "init_groups": "T",
  "early_stopping": true,
  "insubject": 1,
  "eeg_data_path": "/public/home/hugf2022/Things_EEG2/Preprocessed_data_250Hz",
  "pretrain_dir": "/home_data/home/hugf2022/datasets/mindalign-assets/mae"
}
```
