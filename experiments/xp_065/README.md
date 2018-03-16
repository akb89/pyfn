# XP\#065

semafor on FN 1.7 FT + EX with NLP4J + BMST + HIERARCHY + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 67.9 | 59.9 | 63.7 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_065/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 065 -p semafor -s test -f /path/to/fndata-1.7-with-dev -u -e
```

### Preprocessing
```
./preprocess.sh -x 065 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 065 -u
```

### Decoding
```
./semafor.sh -m decode -x 065 -s test -u
```

### Scoring
```
./score.sh -x 065 -p semafor -s test
```
