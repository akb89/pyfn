# XP\#089

semafor on FN 1.5 FT + EX with MXPOST + MST + HIERARCHY + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 60.1 | 60.6 | 60.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_089/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 089 -p semafor -s test -f /path/to/fndata-1.5-with-dev -u -e
```

### Preprocessing
```
./preprocess.sh -x 089 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 089 -u
```

### Decoding
```
./semafor.sh -m decode -x 089 -s test -u
```

### Scoring
```
./score.sh -x 089 -p semafor -s test -f gold
```
