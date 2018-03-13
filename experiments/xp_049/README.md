# XP\#049

semafor on FN 1.7 FT + EX with NLP4J + BMST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.9 | 57.9 | 61.2 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_049/data \
  --splits train \
  --with_exemplars \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 049 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 049 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 049
```

### Decoding
```
./semafor.sh -m decode -x 049 -s test
```

### Scoring
```
./score.sh -x 049 -p semafor -s test
```
