# XP\#092

semafor on FN 1.5 FT + EX with NLP4J + BMST

### Test scores
| P | R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_092/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 092 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 092 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 092
```

### Decoding
```
./semafor.sh -m decode -x 092 -s test
```

### Scoring
```
./score.sh -x 092 -p semafor -s test
```
