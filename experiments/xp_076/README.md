# XP\#076

open-sesame on FN 1.5 FT with MXPOST + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 66.2 | 59.7 | 62.8 |


### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_076/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter overlap_fes no_fes
```

### Data preparation
```
./prepare.sh -x 076 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 076 -t mxpost -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 076
```

### Decoding
```
./open-sesame.sh -m decode -x 076 -s test
```

### Scoring
```
./score.sh -x 076 -p open-sesame -s test
```
