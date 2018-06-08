# XP\#157

open-sesame on FN 1.7 FT with NLP4J + BMST with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 65.7 | 62.9 | 64.3 |

### Splits generation for frame identification
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_157/data \
  --splits train \
  --output_sentences
```

### Preprocessing for frame identification
```
./preprocess.sh -x 157 -t nlp4j -d bmst -p semafor
```

### Training frame identification
```
./frameid.sh -m train -x 157
```

### Splits generation for argument identification
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_157/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 157 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing for argument identification
```
./preprocess.sh -x 157 -t nlp4j -p open-sesame -d bmst -v
```

### Training argument identification
```
./open-sesame.sh -m train -x 157 -d
```

### Decoding frame identification
```
./frameid.sh -m decode -x 157 -p open-sesame
```

### Decoding argument identification
```
./open-sesame.sh -m decode -x 157 -s test -d
```

### Scoring
```
./score.sh -x 157 -p open-sesame -s test -f predicted
```
