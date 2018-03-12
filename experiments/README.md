# Recap on experiments

- [x] XP042: semafor on FN 1.5 FT with MXPOST + MST
- [-] XP043: open-sesame on FN 1.5 FT with MXPOST
- [-] XP044: open-sesame on FN 1.5 FT with MXPOST + MST
- [-] XP045: semafor on FN 1.5 FT + EX with MXPOST + MST
- [-] XP046: open-sesame on FN 1.5 FT + EX with MXPOST (_dynet.pyx: Magnitude of gradient is bad)
- [-] XP047: semafor on FN 1.7 FT with NLP4J + BMST
- [-] XP048: open-sesame on FN 1.7 FT with NLP4J
- [-] XP049: semafor on FN 1.7 FT + EX with NLP4J + BMST
- [-] XP050: open-sesame on FN 1.7 FT + EX with NLP4J + BMST (BUG)
- [x] XP051: semafor on FN 1.5 FT with MXPOST + MST + HIERARCHY (with old .csv files)
- [x] XP052: semafor on FN 1.5 FT + EX with MXPOST + MST + HIERARCHY (with old .csv files)
- [-] XP053: open-sesame on FN 1.7 FT with MXPOST
- [x] XP054: semafor on FN 1.7 FT with MXPOST + MST
- [-] XP055: open-sesame on FN 1.7 FT with NLP4J + MST
- [x] XP056: semafor on FN 1.7 FT with NLP4J + MST
- [-] XP057: open-sesame on FN 1.7 FT with NLP4J + BMST
- [x] XP058: semafor on FN 1.7 FT with NLP4J + BMST + filtered no_fes
- [-] XP059: open-sesame on FN 1.7 FT with NLP4J + filtered no_fes
- [-] XP060: open-sesame on FN 1.7 FT with NLP4J + BMST + filtered no_fes
- [ ] XP061: semafor on FN 1.7 FT with MXPOST + MST + HIERARCHY
- [ ] XP062: semafor on FN 1.7 FT + EX with MXPOST + MST + HIERARCHY
- [ ] XP063: semafor on FN 1.7 FT with NLP4J + BMST with PRED FRAMES
- [ ] XP064: open-sesame on FN 1.7 FT with NLP4J with PRED FRAMES
- [ ] XP065: open-sesame on FN 1.7 FT with NLP4J + BMST with PRED FRAMES
- [ ] XP066: semafor on FN 1.7 FT + EX with NLP4J + BMST with PRED FRAMES
- [x] XP067: XP045 with a batch size of 4,000 instead of 40,000
- [x] XP068: XP049 with a batch size of 4,000 instead of 40,000
- [x] XP069: semafor on FN 1.5 FT with NLP4J + MST
- [x] XP070: semafor on FN 1.5 FT with NLP4J + BMST
- [x] XP071: semafor on FN 1.7 FT + EX with NLP4J + BMST + filtered discontinuous targets
- [x] XP072: semafor on FN 1.7 FT + EX with NLP4J + BMST + filtered sentences
- [x] XP073: semafor on FN 1.7 FT + EX with NLP4J + BMST + filtered no_fes
- [-] XP074: semafor on FN 1.5 FT with MXPOST + MST + filtered no_fes
- [x] XP075: semafor on FN 1.5 FT + EX with MXPOST + MST + filtered no_fes
- [-] XP076: open-sesame on FN 1.5 FT with MXPOST + filtered no_fes
- [-] XP077: open-sesame on FN 1.5 FT with MXPOST + MST + filtered no_fes
- [-] XP078: open-sesame on FN 1.5 FT with NLP4J
- [-] XP079: open-sesame on FN 1.5 FT with NLP4J + MST
- [-] XP080: open-sesame on FN 1.7 FT with MXPOST + MST
- [x] XP081: semafor on FN 1.5 FT with NLP4J + BARCH
- [-] XP082: open-sesame on FN 1.5 FT with NLP4J + BMST
- [-] XP083: open-sesame on FN 1.5 FT with NLP4J + BARCH
- [x] XP084: semafor on FN 1.7 FT with NLP4J + BARCH
- [-] XP085: open-sesame on FN 1.7 FT with NLP4J + BARCH
- [ ] XP086: semafor on FN 1.5 FT with MXPOST + MST + HIERARCHY (with new .csv files)
- [ ] XP087: semafor on FN 1.5 FT + EX with MXPOST + MST + HIERARCHY (with new .csv files)
- [ ] XP088: semafor on FN 1.7 FT + EX with MXPOST + MST

| XP | P | R | F1 |
| --- | --- | --- | --- |
| 042 | 65.4 | 53.4 | 58.8 | X
| 043 | 65.7 | 58.8 | 62.1 | X
| 044 | 65.6 | 59.7 | 62.5 | X
| 045 | 68.4 | 55.1 | 61.0 |
| 046 |  |  |  |
| 047 | 61.2 | 55.2 | 58.1 | X
| 048 | 63.5 | 59.2 | 61.3 | X
| 049 | 59.7 | 56.0 | 57.8 |
| 050 |  |  |  |
| 051 | 65.3 | 54.9 | 59.7 |
| 052 | 68.6 | 57.0 | 62.3 |
| 053 | 62.2 | 59.1 | 60.6 | X
| 054 | 57.5 | 52.6 | 54.9 | X
| 055 |  |  |  |
| 056 | 59.1 | 53.4 | 56.1 |
| 057 | 65.3 | 60.0 | 62.5 | X
| 058 | 60.6 | 55.7 | 58.1 |
| 059 | 62.4 | 59.3 | 60.8 | X
| 060 |  |  |  | X
| 061 |  |  |  |
| 062 |  |  |  |
| 063 |  |  |  |
| 064 |  |  |  |
| 065 |  |  |  |
| 066 |  |  |  |
| 067 | 66.7 | 56.5 | 61.2 |
| 068 | 57.9 | 56.4 | 57.2 |
| 069 | 66.2 | 55.5 | 60.3 |
| 070 | 67.5 | 56.9 | 61.7 |
| 071 | 59.8 | 55.8 | 57.8 |
| 072 | 59.1 | 56.2 | 57.6 |
| 073 | 60.7 | 57.6 | 59.1 |
| 074 | 65.2 | 53.8 | 58.9 |
| 075 | 64.4 | 59.1 | 61.6 |
| 076 |  |  |  |
| 077 |  |  |  |
| 078 |  |  |  |
| 079 |  |  |  |
| 080 |  |  |  |
| 081 | 67.6 | 56.8 | 61.7 |
| 082 |  |  |  |
| 083 |  |  |  |
| 084 | 61.2 | 55.8 | 58.4 |
| 085 |  |  |  |


Excluded sentences:

--excluded_sentences 4106364 4129442 4129443 4113871 1390031 205489 891688 206654 4201324 367862 1390023 1253346 212521 1253341 1253365 1222433 4201300 1253343 1253367 1253364 1293497 4201253 1509302 1057652 1222461 1390039 1222422 1390013 1222429 1253345 1253357 1253344 1390036 4201290 1253349 1222434 4201280 4201183 205452 4201383 4201164 1222427 1253347 1253362

- 4106364: ANC__110CYL067.xml / 've got problem in FN1.7
- 4129442: || symbol in LU 1.7
- 4129443: || in LU 1.7
- 4113871: LU 1.7
- 1390031: LU 1.7
- 205489: LU 1.5 and 1.7
- 891688: LU 1.5 and 1.7
- 206654: LU 1.5 and 1.7
- 4201324: LU 1.7
- 367862: LU 1.5 and 1.7
- 1390023: LU 1.7
- 1253346: LU 1.5 and 1.7
- 212521: LU 1.5 and 1.7
- 1253341: LU 1.5 and 1.7
- 1253365: LU 1.5 and 1.7
- 1222433: LU 1.5 and 1.7
- 4201300: LU 1.7
- 1253343: LU 1.5 and 1.7
- 1253367: LU 1.5 and 1.7
- 1253364: LU 1.5 and 1.7
- 1293497: LU 1.5 and 1.7
- 4201253: LU 1.7
- 1509302: LU 1.5 and 1.7
- 1057652: LU 1.5 and 1.7
- 1222461: LU 1.5 and 1.7
- 1390039: LU 1.7
- 1222422: LU 1.5 and 1.7
- 1390013: LU 1.7
- 1222429: LU 1.5 and 1.7
- 1253345: LU 1.5 and 1.7
- 1253357: LU 1.5 and 1.7
- 1253344: LU 1.5 and 1.7
- 1390036: LU 1.7
- 4201290: LU 1.7
- 1253349: LU 1.5 and 1.7
- 1222434: LU 1.5 and 1.7
- 4201280: LU 1.7
- 4201183: LU 1.7
- 205452: LU 1.5 and 1.7
- 4201383: LU 1.7
- 4201164: LU 1.7
- 1222427: LU 1.5 and 1.7
- 1253347: LU 1.5 and 1.7
- 1253362: LU 1.5 and 1.7
