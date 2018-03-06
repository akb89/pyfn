# XP\#056

on CLCL9

rofames on FN 1.7 FT with NLP4J + MST

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
  --target /path/to/experiments/xp_056/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 056 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 056 -t nlp4j -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 056
```

### Decoding
```
./rofames.sh -m decode -x 056 -s test
```

### Scoring
```
./score.sh -x 056 -p rofames -s test
```
