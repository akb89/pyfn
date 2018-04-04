# XP\#094

semafor on FN 1.5 FT + EX with NLP4J + BMST + HIERARCHY

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.2 | 61.1 | 62.6 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_094/data \
  --splits train \
  --with_exemplars \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 094 -p semafor -s test -f /path/to/fndata-1.5-with-dev -u -e
```

### Preprocessing
```
./preprocess.sh -x 094 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 094 -u
```

### Decoding
```
./semafor.sh -m decode -x 094 -s test -u
```

### Scoring
```
./score.sh -x 094 -p semafor -s test -f gold
```
