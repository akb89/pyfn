# XP\#058

rofames on FN 1.7 FT with NLP4J + BMST + filtered no_fes

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
  --target /path/to/experiments/xp_058/data \
  --splits train \
  --output_sentences \
  --no_fes
```

### Data preparation
```
./prepare.sh -x 058 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 058 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 058
```

### Decoding
```
./rofames.sh -m decode -x 058 -s test
```

### Scoring
```
./score.sh -x 058 -p rofames -s test
```
