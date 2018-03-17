# XP\#165

semafor on FN 1.7 FT + EX with NLP4J + BMST + HIERARCHY + filtered no_fes with predicted frames trained on FT+EX

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 68.8 | 49.2 | 57.4 |

### Frame identification
```
./frameid.sh -m decode -x 165 -p semafor
```

### Decoding
```
./semafor.sh -m decode -x 165 -s test
```

### Scoring
```
./score.sh -x 165 -p semafor -s test -f predicted
```
