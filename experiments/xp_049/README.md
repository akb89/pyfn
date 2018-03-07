# XP\#049

on FATERMIND batch 40,000 10 threads

ROFAMES on FN 1.7 FT + EX with NLP4J + BMST

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 59.7 | 56.0 | 57.8 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_049/data \
  --splits train \
  --with_exemplars \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 049 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 049 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 049
```

### Decoding
```
./rofames.sh -m decode -x 049 -s test
```

### Scoring
```
./score.sh -x 049 -p rofames -s test
```
