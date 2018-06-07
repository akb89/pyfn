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

### Splits generation for argument identification
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_148/data \
  --splits train \
  --output_sentences
```

### Preprocessing for argument identification
```
./preprocess.sh -x 148 -t nlp4j -p open-sesame -v
```

### Preprocessing for frame identification
Needs to be after preprocessing for arg. id.
```
./preprocess.sh -x 148 -t nlp4j -d bmst -p semafor
```

### Data preparation
```
./prepare.sh -x 148 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Training frame identification
```
./frameid.sh -m train -x 148
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
