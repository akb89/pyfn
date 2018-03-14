# XP\#147

semafor on FN 1.7 FT with NLP4J + BMST with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 63.1 | 60.6 | 61.8 |

### Frame identification
```
./frameid.sh -m decode -x 147 -p semafor
```

### Decoding
```
./semafor.sh -m decode -x 147 -s test
```

### Scoring
```
./score.sh -x 147 -p semafor -s test -f predicted
```
