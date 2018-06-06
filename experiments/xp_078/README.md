# XP\#078

open-sesame on FN 1.5 FT with NLP4J

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.8 | 60.2 | 62.4 |


### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_078/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 078 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 078 -t nlp4j -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 078
```

### Decoding
```
./open-sesame.sh -m decode -x 078 -s test
```

### Scoring
```
./score.sh -x 078 -p open-sesame -s test -f gold
```
