# XP\#045

semafor on FN 1.5 FT + EX with MXPOST + MST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 63.0 | 55.4 | 59.0 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_045/data \
  --splits train \
  --with_exemplars \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 045 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 045 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 045
```

### Decoding
```
./semafor.sh -m decode -x 045 -s test
```

### Scoring
```
./score.sh -x 045 -p semafor -s test -f gold
```
