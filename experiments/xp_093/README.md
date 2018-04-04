# XP\#093

semafor on FN 1.5 FT + EX with NLP4J + BMST + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 69.4 | 60.2 | 64.5 |
| 64.3 | 60.2 | 62.2 |
| 65.0 | 60.0 | 62.4 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_093/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter no_fes
```

### Data preparation
```
./prepare.sh -x 093 -p semafor -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 093 -t nlp4j -d bmst -p semafor
```

### Training
```
./semafor.sh -m train -x 093
```

### Decoding
```
./semafor.sh -m decode -x 093 -s test
```

### Scoring
```
./score.sh -x 093 -p semafor -s test -f gold
```
