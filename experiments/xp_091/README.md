# XP\#091

semafor on FN 1.5 FT with NLP4J + BMST + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 66.3 | 57.5 | 61.6 |
| 61.3 | 57.5 | 59.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_091/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 091 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 091 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 091
```

### Decoding
```
./semafor.sh -m decode -x 091 -s test
```

### Scoring
```
./score.sh -x 091 -p semafor -s test
```
