# XP\#053

open-sesame on FN 1.7 FT with MXPOST

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
  --target /path/to/experiments/xp_053/data \
  --splits train \
  --output_sentences \
  --excluded_sentences 4106364 \
  --filter overlap_fes
```

### Data preparation
```
./prepare.sh -x 053 -p open-sesame -s test -f /path/to/fndata-1.7-with-dev
```

### Preprocessing
Splits are preprocessed with:
```
./preprocess.sh -x 053 -t mxpost -p open-sesame -v
```

### Training
```
./open-sesame.sh -m train -x 053
```

### Decoding
```
./open-sesame.sh -m decode -x 053 -s test
```

### Scoring
```
./score.sh -x 053 -p open-sesame -s test
```
