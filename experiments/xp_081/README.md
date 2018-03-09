# XP\#081

rofames on FN 1.5 FT with NLP4J + BARCH

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_081/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 081 -p rofames -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 081 -t nlp4j -d barch -p rofames
```

### Training
```
./rofames.sh -m train -x 081
```

### Decoding
```
./rofames.sh -m decode -x 081 -s test
```

### Scoring
```
./score.sh -x 081 -p rofames -s test
```
