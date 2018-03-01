# XP\#044

Memory leak on test

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  | |

## Setup
### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.5 | TRUE | FALSE | GOLD |

### Filtering in training data
| No FEs | Overlapping FEs | Discontinuous FEs | Discontinuous targets |
| --- | --- | --- | --- |
| FALSE | TRUE | FALSE | FALSE |

### Preprocessing
| POS tagger | Lemmatizer | Dependency parser |
| --- | --- | --- |
| MXPOST | NLP4J | MST |

### Frame Semantic Parsing
| Parser | Hierarchy feature |
| --- | --- |
| OPEN-SESAME | FALSE |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev
  --target /path/to/experiments/xp_044/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398
  --excluded_sentences 1271774 1277988 1278010 \
  --filter overlap_fes
```
Excluded sentences are excluded from train.
Excluded frames (Test35) are from train and dev.

Following sentences are excluded as they lead to multiple roots with the MSTParser:
```
Partly as a result of the shortcomings in the Nuclear Non - Proliferation Treaty ( NPT ) safeguards system -- which allowed the rapid development of the Iraqi nuclear program in the 1970s and North Korea 's in the 1990s to go largely undetected -- and partly by assessing Iran 's intentions , the international community and the International Atomic Energy Agency ( IAEA ) have increased their scrutiny of Iran 's activities over the last several years .

The above groups pose the following dangers : 1- Attacking for the purpose of : A : Assassination B : Kidnapping C : Aerial raids and artillery attacks 2- Sabotage A : Setting fires B : Explosions C : Technical sabotage D : Chemical sabotage 3- Spying A : Recruiting a member of society B : Planting a mole within society C : Spying surveillance operation 4- Stealing 5- Pests : A : Poisonous such as snakes and scorpions B : Harmful such as rats and cockroaches C : Sickening such as mosquitoes

The distance between the first and fourth bump should be 100 meters , and the distance between the fourth and the sixth should be 50 meters , so cars can not travel fast in the direction of the building 5- Barbed Wires : They should be placed around the building , around the walls , or on top of the walls 6- Nails Obstacle : These are placed at the main gate in order to puncture the tires of any car crashing in
```

### Preparing data
```
./prepare.sh -x 044 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
Splits are preprocessed with:
```
./preprocess.sh -x 044 -t mxpost -p open-sesame -d mst -v
```

### Training
```
./open-sesame.sh -m train -x 044 -d
```

### Decoding
```
./open-sesame.sh -m decode
```

### Scoring
```
./score.sh
```
