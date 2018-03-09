# XP\#042

rofames on FN 1.5 FT with MXPOST + MST

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 65.4 | 53.4 | 58.8 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_042/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 042 -p rofames -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 042 -t mxpost -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 042
```

### Decoding
```
./rofames.sh -m decode -x 042 -s test
```

### Scoring
```
./score.sh -x 042 -p rofames -s test
```
