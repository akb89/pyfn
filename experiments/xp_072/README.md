# XP\#072

rofames on FN 1.7 FT + EX with NLP4J + BMST + filtered sentences

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
  --target /path/to/experiments/xp_072/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_sentences 4129442 4129443 4113871 1390031 205489 891688 206654 4201324 367862 1390023 1253346 212521 1253341 1253365 1222433 4201300 1253343 1253367 1253364 1293497 4201253 1509302 1057652 1222461 1390039 1222422 1390013 1222429 1253345 1253357 1253344 1390036 4201290 1253349 1222434 4201280 4201183 205452 4201383 4201164 1222427 1253347 1253362
```

### Data preparation
```
./prepare.sh -x 072 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 072 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 072
```

### Decoding
```
./rofames.sh -m decode -x 072 -s test
```

### Scoring
```
./score.sh -x 072 -p rofames -s test
```
