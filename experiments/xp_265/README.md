# XP\#265

semafor on FN 1.7 FT + EX with NLP4J + BMST + HIERARCHY + filtered no_fes with predicted frames trained on FT only

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 68.7 | 48.5 | 56.9 |

### Frame identification
```
./frameid.sh -m decode -x 265 -p semafor
```

### Decoding
```
./semafor.sh -m decode -x 265 -s test
```

### Scoring
```
./score.sh -x 265 -p semafor -s test -f predicted
```
