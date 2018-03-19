# XP\#084

semafor on FN 1.7 FT with NLP4J + BARCH

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 61.2 | 55.8 | 58.4 |
| 60.4 | 55.8 | 58.0 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_084/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 084 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 084 -t nlp4j -d barch -p semafor
```

### Training
```
./semafor.sh -m train -x 084
```

### Decoding
```
./semafor.sh -m decode -x 084 -s test
```

### Scoring
```
./score.sh -x 084 -p semafor -s test
```
