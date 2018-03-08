# XP\#069

rofames on FN 1.5 FT with NLP4J + MST

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 66.2 | 55.5 | 60.3 |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_069/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 069 -p rofames -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 069 -t nlp4j -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 069
```

### Decoding
```
./rofames.sh -m decode -x 069 -s test
```

### Scoring
```
./score.sh -x 069 -p rofames -s test
```
