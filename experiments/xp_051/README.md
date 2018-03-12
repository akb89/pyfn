# XP\#051

open-sesame on FN 1.5 FT with MXPOST + MST + HIERARCHY

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 65.3 | 54.9 | 59.7 |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_051/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 051 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 051 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 051 -u
```

### Decoding
```
./semafor.sh -m decode -x 051 -s test -u
```

### Scoring
```
./score.sh -x 051 -p semafor -s test
```
