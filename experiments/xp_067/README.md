# XP\#067

With a batch size of 4000 on CLCL9

ROFAMES on FN 1.5 FT + EX with MXPOST + MST and GOLD frames

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 66.7 | 56.5 | 61.2 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_067/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398 \
  --excluded_sentences 1565683 \
  --filter non_breaking_spaces
```

### Data preparation
```
./prepare.sh -x 067 -p rofames -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 067 -t mxpost -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 067
```

### Decoding
```
./rofames.sh -m decode -x 067 -s test
```

### Scoring
```
./score.sh -x 067 -p rofames -s test
```
