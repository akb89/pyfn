# XP\#057

open-sesame on FN 1.7 FT with NLP4J + BMST

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  | |

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
  --target /path/to/experiments/xp_057/data \
  --splits train \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 057 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 057 -t nlp4j -p open-sesame -d bmst -v
```

### Training
```
./open-sesame.sh -m train -x 057 -d
```

### Decoding
```
./open-sesame.sh -m decode
```

### Scoring
```
./score.sh
```