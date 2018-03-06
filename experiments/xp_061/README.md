# XP\#061

rofames on FN 1.7 FT with NLP4J + BMST + HIERARCHY

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
  --target /path/to/experiments/xp_061/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 061 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 061 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 061 -u
```

### Decoding
```
./rofames.sh -m decode -x 061 -s test -u
```

### Scoring
```
./score.sh -x 061 -p rofames -s test
```
