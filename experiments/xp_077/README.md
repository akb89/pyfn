# XP\#077

open-sesame on FN 1.5 FT with MXPOST + MST + filtered no_fes

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.8 | 60.3 | 62.5 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev
  --target /path/to/experiments/xp_077/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --excluded_sentences 1271774 1277988 1278010 \
  --filter overlap_fes no_fes
```

### Data preparation
```
./prepare.sh -x 077 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 077 -t mxpost -p open-sesame -d mst -v
```

### Training
```
./open-sesame.sh -m train -x 077 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 077 -s test -d
```

### Scoring
```
./score.sh -x 077 -s test
```
