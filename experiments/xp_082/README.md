# XP\#082

open-sesame on FN 1.5 FT with NLP4J + BMST

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 69.4 | 59.6 | 64.1 |
| 64.1 | 59.6 | 61.2 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_082/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 082 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 082 -t nlp4j -p open-sesame -d bmst -v
```

### Training
```
./open-sesame.sh -m train -x 082 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 082 -s test -d
```

### Scoring
```
./score.sh -x 082 -p open-sesame -s test -f gold
```
