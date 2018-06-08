# XP\#178

open-sesame on FN 1.5 FT with NLP4J with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 63.7 | 64.4 | 64.1 |

### Splits generation for frame identification
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_178/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Preprocessing for frame identification
Needs to be after preprocessing for arg. id.
```
./preprocess.sh -x 178 -t nlp4j -d bmst -p semafor
```

### Training frame identification
```
./frameid.sh -m train -x 178
```

### Splits generation for argument identification
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_178/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 178 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing for argument identification
```
./preprocess.sh -x 178 -t nlp4j -p open-sesame -v
```

### Training argument identification
```
./open-sesame.sh -m train -x 178
```

### Decoding frame identification
```
./frameid.sh -m decode -x 178 -p open-sesame
```

### Decoding argument identification
```
./open-sesame.sh -m decode -x 178 -s test
```

### Scoring
```
./score.sh -x 178 -p open-sesame -s test -f predicted
```
