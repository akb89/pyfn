# XP\#182

open-sesame on FN 1.5 FT with NLP4J + BMST with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 66.1 | 64.0 | 65.0 |

### Splits generation for frame identification
```
pyfn convert \
  --from fnxml \
  --to semafor \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_182/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Splits generation for argument identification
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev \
  --target /path/to/experiments/xp_182/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
```

### Preprocessing for argument identification
```
./preprocess.sh -x 182 -t nlp4j -p open-sesame -d bmst -v
```

### Preprocessing for frame identification
Needs to be after preprocessing for arg. id.
```
./preprocess.sh -x 182 -t nlp4j -d bmst -p semafor
```

### Data preparation
```
./prepare.sh -x 182 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Training frame identification
```
./frameid.sh -m train -x 182
```

### Training argument identification
```
./open-sesame.sh -m train -x 182 -d
```

### Decoding frame identification
```
./frameid.sh -m decode -x 182 -p open-sesame
```

### Decoding argument identification
```
./open-sesame.sh -m decode -x 182 -s test -d
```

### Scoring
```
./score.sh -x 182 -p open-sesame -s test -f predicted
```
