# XP\#170

semafor on FN 1.5 FT with NLP4J + BMST with predicted frames

### Test scores
| P | R | F1 |
| --- | --- | --- |
| 63.4 | 60.2 | 61.8 |

### Preprocessing
```
./frameid.sh -m decode -x 170 -p semafor
```

### Decoding
```
./semafor.sh -m decode -x 170 -s test
```

### Scoring
```
./score.sh -x 170 -p semafor -s test -f predicted
```
