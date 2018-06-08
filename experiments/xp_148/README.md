# XP\#148

open-sesame on FN 1.7 FT with NLP4J with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.0 | 55.2 | 59.3 |

### Splits generation for frame identification
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_148/data \
  --splits train \
  --output_sentences
```

### Preprocessing for frame identification
```
./preprocess.sh -x 148 -t nlp4j -d bmst -p semafor
```

### Training frame identification
```
./frameid.sh -m train -x 148
```

### Splits generation for argument identification
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_148/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 148 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing for argument identification
```
./preprocess.sh -x 148 -t nlp4j -p open-sesame -v
```

### Training argument identification
```
./open-sesame.sh -m train -x 148
```

### Decoding frame identification
```
./frameid.sh -m decode -x 148 -p open-sesame
```

### Decoding argument identification
```
./open-sesame.sh -m decode -x 148 -s test
```

### Scoring
```
./score.sh -x 148 -p open-sesame -s test -f predicted
```
