# XP\#071

rofames on FN 1.7 FT + EX with NLP4J + BMST + filtered discontinuous targets

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
  --target /path/to/experiments/xp_071/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter disc_targets
```

### Data preparation
```
./prepare.sh -x 071 -p rofames -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 071 -t nlp4j -d bmst -p rofames
```

### Training
```
./rofames.sh -m train -x 071
```

### Decoding
```
./rofames.sh -m decode -x 071 -s test
```

### Scoring
```
./score.sh -x 071 -p rofames -s test
```
