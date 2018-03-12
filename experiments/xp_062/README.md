# XP\#062

semafor on FN 1.7 FT + EX with MXPOST + MST + HIERARCHY

### Test scores
| P | R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_062/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 062 -p semafor -s test -f /path/to/fndata-1.7-with-dev -u -e
```

### Preprocessing
```
./preprocess.sh -x 062 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 062 -u
```

### Decoding
```
./semafor.sh -m decode -x 062 -s test -u
```

### Scoring
```
./score.sh -x 062 -p semafor -s test
```
