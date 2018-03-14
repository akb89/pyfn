# XP\#148

open-sesame on FN 1.7 FT with NLP4J with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 64.0 | 55.2 | 59.3 |

### Frame identification
```
./frameid.sh -m decode -x 148 -p open-sesame
```

### Decoding
```
./open-sesame.sh -m decode -x 148 -s test
```

### Scoring
```
./score.sh -x 148 -p open-sesame -s test -f predicted
```
