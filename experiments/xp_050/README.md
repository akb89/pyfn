# XP\#050

on CLCL8

open-sesame on FN 1.7 FT + EX with NLP4J + BMST

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
  --target /path/to/experiments/xp_050/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 050 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
```
./preprocess.sh -x 050 -t nlp4j -p open-sesame -d bmst -v
```

### Training
```
./open-sesame.sh -m train -x 050 -d
```

### Decoding
```
./open-sesame.sh -m decode
```

### Scoring
```
./score.sh
```
