# XP\#064

semafor on FN 1.7 FT + EX with NLP4J + BMST + HIERARCHY

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 65.8 | 58.6 | 62.0 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_064/data \
  --splits train \
  --with_exemplars \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 064 -p semafor -s test -f /path/to/fndata-1.7-with-dev -u -e
```

### Preprocessing
```
./preprocess.sh -x 064 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 064 -u
```

### Decoding
```
./semafor.sh -m decode -x 064 -s test -u
```

### Scoring
```
./score.sh -x 064 -p semafor -s test -f gold
```
