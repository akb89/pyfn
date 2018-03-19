# XP\#079

open-sesame on FN 1.5 FT with NLP4J + MST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 66.2 | 60.2 | 63.1 |
| 61.2 | 60.2 | 60.7 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_079/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 079 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 079 -t nlp4j -p open-sesame -d mst -v
```

### Training
```
./open-sesame.sh -m train -x 079 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 079 -s test -d
```

### Scoring
```
./score.sh -x 079 -p open-sesame -s test -f gold
```
