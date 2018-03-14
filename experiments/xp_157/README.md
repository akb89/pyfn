# XP\#157

open-sesame on FN 1.7 FT with NLP4J + BMST with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 65.7 | 62.9 | 64.3 |

### Frame identification
```
./frameid.sh -m decode -x 157 -p open-sesame
```

### Decoding
```
./open-sesame.sh -m decode -x 157 -s test -d
```

### Scoring
```
./score.sh -x 157 -p open-sesame -s test -f predicted
```
