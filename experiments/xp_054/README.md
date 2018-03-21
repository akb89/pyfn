# XP\#054

semafor on FN 1.7 FT with MXPOST + MST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 57.5 | 52.6 | 54.9 |
| 61.4 | 53.5 | 57.2 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_054/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 054 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 054 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 054
```

### Decoding
```
./semafor.sh -m decode -x 054 -s test
```

### Scoring
```
./score.sh -x 054 -p semafor -s test -f gold
```
