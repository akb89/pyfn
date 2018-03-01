# XP\#046

FATERMIND

OPEN-SESAME on FN 1.5 FT + EX with MXPOST and GOLD frames

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  | |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_046/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398 \
  --excluded_sentences 1565683 \
  --filter overlap_fes non_breaking_spaces
```

### Data preparation
```
./prepare.sh -x 046 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 046 -t mxpost -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 046
```

### Decoding
```
./open-sesame.sh -m decode
```

### Scoring
```
./score.sh
```
