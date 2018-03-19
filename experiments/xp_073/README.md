# XP\#073

semafor on FN 1.7 FT + EX with NLP4J + BMST + filtered no_fes

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 60.7 | 57.6 | 59.1 |
| 59.8 | 57.6 | 58.7 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_073/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 073 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 073 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 073
```

### Decoding
```
./semafor.sh -m decode -x 073 -s test
```

### Scoring
```
./score.sh -x 073 -p semafor -s test -f gold
```
