# XP\#047

ROFAMES on FN 1.7 FT with NLP4J + BMST

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 60.3 | 55.5 | 57.8 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_047/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 047 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 047 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 047
```

### Decoding
```
./rofames.sh -m decode -x 047 -s test
```

### Scoring
```
./score.sh -x 047 -p rofames -s test
```
