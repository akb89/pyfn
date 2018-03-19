# XP\#087

semafor on FN 1.5 FT + EX with MXPOST + MST + HIERARCHY (with new .csv files)

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 69.0 | 57.0 | 62.5 |
| 65.0 | 59.5 | 62.2 |
| 60.1 | 59.5 | 59.8 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_087/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 087 -p semafor -s test -f /path/to/fndata-1.5-with-dev -u -e
```

### Preprocessing
```
./preprocess.sh -x 087 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 087 -u
```

### Decoding
```
./semafor.sh -m decode -x 087 -s test -u
```

### Scoring
```
./score.sh -x 087 -p semafor -s test -f gold
```
