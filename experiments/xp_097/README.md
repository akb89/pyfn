# XP\#097

semafor on FN 1.7 FT + EX with MXPOST + MST + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.8 | 54.9 | 59.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_097/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 097 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 097 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 097
```

### Decoding
```
./semafor.sh -m decode -x 097 -s test
```

### Scoring
```
./score.sh -x 097 -p semafor -s test -f gold
```
