# XP\#086

semafor on FN 1.5 FT with MXPOST + MST + HIERARCHY (with new .csv files)

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 65.4 | 54.9 | 59.7 |
| 60.3 | 54.9 | 57.5 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_086/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 086 -p semafor -s test -f /path/to/fndata-1.5-with-dev -u
```

### Preprocessing
```
./preprocess.sh -x 086 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 086 -u
```

### Decoding
```
./semafor.sh -m decode -x 086 -s test -u
```

### Scoring
```
./score.sh -x 086 -p semafor -s test
```
