# XP\#053

open-sesame on FN 1.7 FT with MXPOST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 63.1 | 58.1 | 60.5 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_053/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 053 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 053 -t mxpost -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 053
```

### Decoding
```
./open-sesame.sh -m decode -x 053 -s test
```

### Scoring
```
./score.sh -x 053 -p open-sesame -s test
```
