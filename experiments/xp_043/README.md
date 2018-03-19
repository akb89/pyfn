# XP\#043

open-sesame on FN 1.5 FT with MXPOST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.9 | 58.9 | 61.8 |
| 60.0 | 58.9 | 59.4 |


### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_043/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 043 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 043 -t mxpost -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 043
```

### Decoding
```
./open-sesame.sh -m decode -x 043 -s test
```

### Scoring
```
./score.sh -x 043 -p open-sesame -s test -f gold
```
