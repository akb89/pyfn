# XP\#073

rofames on FN 1.7 FT + EX with NLP4J + BMST + filtered no_fes

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 59.0 | 58.1 | 58.5 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_073/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 073 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 073 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 073
```

### Decoding
```
./rofames.sh -m decode -x 073 -s test
```

### Scoring
```
./score.sh -x 073 -p rofames -s test
```
