# XP\#069

semafor on FN 1.5 FT with NLP4J + MST

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 60.2 | 55.4 | 57.7 |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_069/data \
  --splits train \
  --output_sentences
```

### Data preparation
```
./prepare.sh -x 069 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 069 -t nlp4j -d mst -p semafor
```

### Training
```
./semafor.sh -m train -x 069
```

### Decoding
```
./semafor.sh -m decode -x 069 -s test
```

### Scoring
```
./score.sh -x 069 -p semafor -s test -f gold
```
