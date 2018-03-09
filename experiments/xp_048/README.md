# XP\#048

open-sesame on FN 1.7 FT with NLP4J

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 63.5 | 59.2 | 61.3 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_048/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 048 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 048 -t nlp4j -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 048
```

### Decoding
```
./open-sesame.sh -m decode -x 048 -s test
```

### Scoring
```
./score.sh -x 048 -s test
```
