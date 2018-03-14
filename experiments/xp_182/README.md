# XP\#182

open-sesame on FN 1.5 FT with NLP4J + BMST with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 66.1 | 64.0 | 65.0 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_070/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Preprocessing
```
./preprocess.sh -x 182 -t nlp4j -d bmst -p semafor
```

### Data preparation
```
./prepare.sh -x 182 -p open-sesame -s test -d /path/to/fndata-1.5-with-dev -f predicted
```

### Decoding
```
./open-sesame.sh -m decode -x 182 -s test -d
```

### Scoring
```
./score.sh -x 182 -p open-sesame  -s test -f predicted
```
