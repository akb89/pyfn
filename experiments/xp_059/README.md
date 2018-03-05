# XP\#059

on CLCL7

open-sesame on FN 1.7 FT with NLP4J + filtered no_fes

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  |  |

### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.7 | TRUE | FALSE | GOLD |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.7-with-dev \
  --target /path/to/experiments/xp_059/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes no_fes
```

### Data preparation
```
./prepare.sh -x 059 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
Splits are preprocessed with:
```
./preprocess.sh -x 059 -t nlp4j -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 059
```

### Decoding
```
./open-sesame.sh -m decode -x 059 -s test
```

### Scoring
```
./score.sh -x 059 -s test
```
