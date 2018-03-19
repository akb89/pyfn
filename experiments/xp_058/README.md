# XP\#058

semafor on FN 1.7 FT with NLP4J + BMST + filtered no_fes

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 60.6 | 55.7 | 58.1 |
| 59.7 | 55.7 | 57.7 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_058/data \
  --splits train \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 058 -p semafor -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 058 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 058
```

### Decoding
```
./semafor.sh -m decode -x 058 -s test
```

### Scoring
```
./score.sh -x 058 -p semafor -s test -f gold
```
