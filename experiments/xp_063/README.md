# XP\#063

semafor on FN 1.7 FT + EX with MXPOST + MST + HIERARCHY + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 65.8 | 56.7 | 60.9 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_063/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 063 -p semafor -s test -f /path/to/fndata-1.7-with-dev -u -e
```

### Preprocessing
```
./preprocess.sh -x 063 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 063 -u
```

### Decoding
```
./semafor.sh -m decode -x 063 -s test -u
```

### Scoring
```
./score.sh -x 063 -p semafor -s test
```
