# XP\#075

rofames on FN 1.5 FT + EX with MXPOST + MST + filtered no_fes

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 68.4 | 55.1 | 61.0 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_075/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398 \
  --excluded_sentences 1565683 \
  --filter non_breaking_spaces no_fes
```

### Data preparation
```
./prepare.sh -x 075 -p rofames -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 075 -t mxpost -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 075
```

### Decoding
```
./rofames.sh -m decode -x 075 -s test
```

### Scoring
```
./score.sh -x 075 -p rofames -s test
```
