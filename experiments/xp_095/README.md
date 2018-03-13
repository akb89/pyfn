# XP\#095

semafor on FN 1.5 FT + EX with NLP4J + BMST + HIERARCHY + filtered no_fes

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
  --target /path/to/experiments/xp_095/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398 \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 095 -p semafor -s test -f /path/to/fndata-1.5-with-dev -u -e
```

### Preprocessing
```
./preprocess.sh -x 095 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 095 -u
```

### Decoding
```
./semafor.sh -m decode -x 095 -s test -u
```

### Scoring
```
./score.sh -x 095 -p semafor -s test
```
