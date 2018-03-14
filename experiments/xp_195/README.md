# XP\#195

semafor on FN 1.5 FT + EX with NLP4J + BMST + HIERARCHY + filtered no_fes with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
|  |  |  |

### Frame identification
```
./frameid.sh -m decode -x 195 -p semafor
```

### Decoding
```
./semafor.sh -m decode -x 195 -s test
```

### Scoring
```
./score.sh -x 195 -p semafor -s test -f predicted
```
