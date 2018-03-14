# XP\#178

open-sesame on FN 1.5 FT with NLP4J with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 63.7 | 64.4 | 64.1 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_178/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Preprocessing
```
./preprocess.sh -x 178 -t nlp4j -d bmst -p semafor
```

### Data preparation
```
./prepare.sh -x 178 -p open-sesame -s test -d /path/to/fndata-1.5-with-dev -f predicted
```

### Decoding
```
./open-sesame.sh -m decode -x 178 -s test
```

### Scoring
```
./score.sh -x 178 -p open-sesame  -s test -f predicted
```
