# XP\#068

rofames on FN 1.7 FT + EX with NLP4J + BMST

with a batch size of 4,000 instead of 40,000

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_068/data \
  --splits train \
  --with_exemplars \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 068 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 068 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 068
```

### Decoding
```
./rofames.sh -m decode -x 068 -s test
```

### Scoring
```
./score.sh -x 068 -p rofames -s test
```
