# XP\#170

semafor on FN 1.5 FT with NLP4J + BMST with predicted frames

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
  --target /path/to/experiments/xp_170/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Preprocessing
```
./preprocess.sh -x 170 -t nlp4j -d bmst -p semafor
```

### Data preparation
```
./prepare.sh -x 170 -p semafor -s test -d /path/to/fndata-1.5-with-dev -f predicted
```

### Training
```
./semafor.sh -m train -x 170
```

### Decoding
```
./semafor.sh -m decode -x 170 -s test
```

### Scoring
```
./score.sh -x 170 -p semafor -s test -f predicted
```
