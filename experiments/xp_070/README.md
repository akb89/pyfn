# XP\#070

rofames on FN 1.5 FT with NLP4J + BMST

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
  --target /path/to/experiments/xp_070/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 070 -p rofames -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 070 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 070
```

### Decoding
```
./rofames.sh -m decode -x 070 -s test
```

### Scoring
```
./score.sh -x 070 -p rofames -s test
```
