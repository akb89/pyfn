# XP\#080

open-sesame on FN 1.7 FT with MXPOST + MST

### Test scores
| P | R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_080/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 080 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 080 -t mxpost -p open-sesame -d mst -v
```

### Training
```
./open-sesame.sh -m train -x 080 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 080 -s test -d
```

### Scoring
```
./score.sh -x 080 -s test
```
