# Recap on experiments

- [x] XP042: rofames on FN 1.5 FT with MXPOST + MST XXX
- [x] XP043: open-sesame on FN 1.5 FT with MXPOST
- [x] XP044: open-sesame on FN 1.5 FT with MXPOST + MST
- [x] XP045: rofames on FN 1.5 FT + EX with MXPOST + MST XXX
- [-] XP046: open-sesame on FN 1.5 FT + EX with MXPOST (20 days??)
- [x] XP047: rofames on FN 1.7 FT with NLP4J + BMST
- [x] XP048: open-sesame on FN 1.7 FT with NLP4J
- [-] XP049: rofames on FN 1.7 FT + EX with NLP4J + BMST (BUG Conllizer)
- [-] XP050: open-sesame on FN 1.7 FT + EX with NLP4J + BMST (BUG Conllizer)
- [-] XP051: rofames on FN 1.5 FT with MXPOST + MST + HIERARCHY
- [-] XP052: rofames on FN 1.5 FT + EX with MXPOST + MST + HIERARCHY
- [-] XP053: open-sesame on FN 1.7 FT with MXPOST (BUG Conllizer REDO all)
- [ ] XP054: rofames on FN 1.7 FT with MXPOST
- [ ] XP055: open-sesame on FN 1.7 FT with NLP4J + MST
- [ ] XP056: rofames on FN 1.7 FT with NLP4J + MST
- [-] XP057: open-sesame on FN 1.7 FT with NLP4J + BMST
- [ ] XP058: rofames on FN 1.7 FT with NLP4J + BMST + filtered no_fes
- [ ] XP059: open-sesame on FN 1.7 FT with NLP4J + filtered no_fes
- [ ] XP060: open-sesame on FN 1.7 FT with NLP4J + BMST + filtered no_fes
- [ ] XP061: rofames on FN 1.7 FT with NLP4J + BMST + HIERARCHY
- [ ] XP062: rofames on FN 1.7 FT + EX with NLP4J + BMST + HIERARCHY
- [ ] XP063: rofames on FN 1.7 FT with NLP4J + BMST with PRED FRAMES
- [ ] XP064: open-sesame on FN 1.7 FT with NLP4J with PRED FRAMES
- [ ] XP065: open-sesame on FN 1.7 FT with NLP4J + BMST with PRED FRAMES
- [ ] XP066: rofames on FN 1.7 FT + EX with NLP4J + BMST with PRED FRAMES
- [ ] XP067: XP045 with a batch size of 4,000 instead of 40,000
- [-] XP068: rofames on FN 1.7 FT with MXPOST + MST (BUG)

| XP | P| R | F1 |
| --- | --- | --- | --- |
| 042 | 65.2 | 53.8 | 59.0 | REDO DECODING
| 043 | 65.7 | 58.8 | 62.1 | REDO TRAINING with 15 EPOCH
| 044 | 65.6 | 59.7 | 62.5 | REDO TRAINING with 15 EPOCH
| 045 | 68.4 | 55.1 | 61.0 | REDO DECODING
| 046 |  |  |  |
| 047 | 60.3 | 55.5 | 57.8 |
| 048 | 63.5 | 59.2 | 61.3 | REDO TRAINING with 15 EPOCH
| 049 |  |  |  |
| 050 |  |  |  |
| 051 | 65.3 | 54.9 | 59.7 |
| 052 |  |  |  |
| 053 |  |  |  | REDO TRAINING with 15 EPOCH
| 054 |  |  |  |
| 055 |  |  |  |
| 056 |  |  |  |
| 057 |  |  |  |
|  |  |  |  |

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
