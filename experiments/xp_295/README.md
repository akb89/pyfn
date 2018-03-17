# XP\#295

semafor on FN 1.5 FT + EX with NLP4J + BMST + HIERARCHY + filtered no_fes with predicted frames
trained on FT (no EX!)

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 66.8 | 50.3 | 57.4 |

### Frame identification
```
./frameid.sh -m decode -x 295 -p semafor
```

### Decoding
```
./semafor.sh -m decode -x 295 -s test
```

### Scoring
```
./score.sh -x 295 -p semafor -s test -f predicted
```
