# XP\#096

semafor on FN 1.7 FT with MXPOST + MST + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 62.9 | 53.4 | 57.8 |
| 62.0 | 53.4 | 57.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_096/data \
  --splits train \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 096 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 096 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 096
```

### Decoding
```
./semafor.sh -m decode -x 096 -s test
```

### Scoring
```
./score.sh -x 096 -p semafor -s test -f gold
```
