# XP\#085

open-sesame on FN 1.7 FT with NLP4J + BARCH

### Test scores
| P | R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_085/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 085 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 085 -t nlp4j -p open-sesame -d barch -v
```

### Training
```
./open-sesame.sh -m train -x 085 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 085 -s test -d
```

### Scoring
```
./score.sh -x 085 -p open-sesame -s test
```
