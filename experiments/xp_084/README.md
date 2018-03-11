# XP\#084

semafor on FN 1.7 FT with NLP4J + BARCH

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 61.2 | 55.8 | 58.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_084/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 084 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 084 -t nlp4j -d barch -p rofames
```

### Training
```
./rofames.sh -m train -x 084
```

### Decoding
```
./rofames.sh -m decode -x 084 -s test
```

### Scoring
```
./score.sh -x 084 -p rofames -s test
```
