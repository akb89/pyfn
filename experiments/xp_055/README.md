# XP\#055

open-sesame on FN 1.7 FT with NLP4J + MST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 63.6 | 57.9 | 60.6 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_055/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 055 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 055 -t nlp4j -p open-sesame -d mst -v
```

### Training
```
./open-sesame.sh -m train -x 055 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 055 -s test -d
```

### Scoring
```
./score.sh -x 055 -p open-sesame -s test
```
