# XP\#056

semafor on FN 1.7 FT with NLP4J + MST

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 59.1 | 53.4 | 56.1 |
| 58.2 | 53.4 | 55.7 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_056/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 056 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 056 -t nlp4j -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 056
```

### Decoding
```
./semafor.sh -m decode -x 056 -s test
```

### Scoring
```
./score.sh -x 056 -p semafor -s test
```
