# XP\#087

semafor on FN 1.5 FT + EX with MXPOST + MST + HIERARCHY

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 61.7 | 58.2 | 59.9 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_087/data \
  --splits train \
  --with_exemplars \
  --output_sentences
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
