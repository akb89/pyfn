# XP\#042

semafor on FN 1.5 FT with MXPOST + MST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 65.0 | 53.2 | 58.5 |
| 60.0 | 53.2 | 56.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_042/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 042 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 042 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 042
```

### Decoding
```
./semafor.sh -m decode -x 042 -s test
```

### Scoring
```
./score.sh -x 042 -p semafor -s test -f gold
```
