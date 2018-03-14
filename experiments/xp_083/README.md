# XP\#083

open-sesame on FN 1.5 FT with NLP4J + BARCH

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 66.4 | 61.3 | 63.7 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_083/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 083 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 083 -t nlp4j -p open-sesame -d barch -v
```

### Training
```
./open-sesame.sh -m train -x 083 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 083 -s test -d
```

### Scoring
```
./score.sh -x 083 -p open-sesame -s test
```
