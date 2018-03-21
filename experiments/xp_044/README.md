# XP\#044

open-sesame on FN 1.5 FT with MXPOST + MST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.8 | 60.9 | 62.8 |
| 60.6 | 59.7 | 60.1 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_044/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 044 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 044 -t mxpost -p open-sesame -d mst -v
```

### Training
```
./open-sesame.sh -m train -x 044 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 044 -s test -d
```

### Scoring
```
./score.sh -x 044 -p open-sesame -s test -f gold
```
