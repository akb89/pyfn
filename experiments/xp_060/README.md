# XP\#060

open-sesame on FN 1.7 FT with NLP4J + BMST + filtered no_fes

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  | |


### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_060/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes no_fes
```

### Data preparation
```
./prepare.sh -x 060 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 060 -t nlp4j -p open-sesame -d bmst -v
```

### Training
```
./open-sesame.sh -m train -x 060 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 060 -s test
```

### Scoring
```
./score.sh -x 060 -p open-sesame -s test
```
