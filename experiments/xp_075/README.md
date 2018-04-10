# XP\#075

semafor on FN 1.5 FT + EX with MXPOST + MST + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 59.9 | 58.9 | 59.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_075/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 075 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 075 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 075
```

### Decoding
```
./semafor.sh -m decode -x 075 -s test
```

### Scoring
```
./score.sh -x 075 -p semafor -s test -f gold
```
