# XP\#088

semafor on FN 1.7 FT + EX with MXPOST + MST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 63.7 | 54.2 | 58.6 |
| 62.7 | 54.2 | 58.1 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_088/data \
  --splits train \
  --with_exemplars \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 088 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 088 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 088
```

### Decoding
```
./semafor.sh -m decode -x 088 -s test
```

### Scoring
```
./score.sh -x 088 -p semafor -s test -f gold
```
