# XP\#075

semafor on FN 1.5 FT + EX with MXPOST + MST + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.4 | 59.1 | 61.6 |
| 59.6 | 59.1 | 59.4 |

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
  --excluded_frames 398 \
  --excluded_sentences 1565683 \
  --filter non_breaking_spaces no_fes
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
