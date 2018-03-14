# XP\#070

semafor on FN 1.5 FT with NLP4J + BMST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 67.5 | 56.4 | 61.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_070/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Data preparation
```
./prepare.sh -x 070 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 070 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 070
```

### Decoding
```
./semafor.sh -m decode -x 070 -s test
```

### Scoring
```
./score.sh -x 070 -p semafor -s test
```
