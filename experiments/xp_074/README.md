# XP\#074

semafor on FN 1.5 FT with MXPOST + MST + filtered no_fes

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 65.2 | 53.8 | 58.9 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_074/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 074 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 074 -t mxpost -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 074
```

### Decoding
```
./semafor.sh -m decode -x 074 -s test
```

### Scoring
```
./score.sh -x 074 -p semafor -s test
```
