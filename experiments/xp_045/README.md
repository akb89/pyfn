# XP\#045

With a batch size of 40,000

BUG with lemmatization: #TODO CHECK

### Test scores
| P| R | F1 |
| --- | --- | --- |
|  |  |  |

## Setup
### Splits
| FrameNet version | Fulltext | Exemplar | Frames
| --- | --- | --- | --- |
| 1.5 | TRUE | TRUE | GOLD |

### Filtering in training data
| No FEs | Overlapping FEs | Discontinuous FEs | Discontinuous targets |
| --- | --- | --- | --- |
| FALSE | FALSE | FALSE | FALSE |

### Preprocessing
| POS tagger | Lemmatizer | Dependency parser |
| --- | --- | --- | --- |
| MXPOST | NLP4J | MST |

### Frame Semantic Parsing
| Parser | Hierarchy feature |
| --- | --- |
| ROFAMES | FALSE |

### Splits generation
Splits are generated with:
```
pyfn convert \
  --from fnxml \
  --to rofames \
  --source /path/to/fndata-1.5 \
  --target /path/to/experiments/xp_045/data \
  --splits train \
  --with_exemplars \
  --output_sentences \
  --excluded_frames 398 \
  --excluded_sentences 1565683 \
  --filter non_breaking_spaces
```

Due to the way MXPOST processes non-breaking spaces, we filter them out.
It excludes 12 sentences from train.lu:
```
Built_JJ as_IN part_NN of_IN a_DT new_JJ outer_JJ defensive_NN wall_NN in_IN 1512_CD it_PRP originally_RB had_VBD a_DT flat_JJ roof — the_NN ornate_NN peak_NN giving_VBG it_PRP such_JJ panache_NN was_VBD added_VBN by_IN de_NNP Keyser_NNP later_RB in_IN 1606_CD ._.
Getting_VBG a_DT federal_JJ government_NN 's_POS priorities_NNS in_IN proper_JJ perspective_NN ,_, one_CD member_NN of_IN parliament_NN bemoaned_VBD the_DT cultural_JJ center_NN as_IN ``_`` 50_CD years_NNS ahead_RB of_IN its_PRP$ time — that_NN 's_VBZ how_WRB long_RB it_PRP 'll_MD take_VB the_DT taxpayers_NNS to_TO meet_VB the_DT 500_CD percent_NN cost_NN overrun_NN ._. ``_``
Just_RB simple_JJ farmers_NNS seeking_VBG a_DT place_NN in_IN the_DT sun_NN to_TO work_VB a_DT piece_NN of_IN land_NN ,_, the_DT pioneers_NNS came_VBD at_IN a_DT time_NN when_WRB territorial_JJ expansion_NN was_VBD much_JJ in_IN vogue — the_NNP French_NNP in_IN the_DT Pacific_NNP and_CC Algeria_NNP ,_, the_DT British_JJ in_IN Africa_NNP and_CC the_DT Far_NNP East_NNP ._.
Near_RB the_DT village_NN of_IN Agía_NNP Déka — named_VBN after_IN ten_JJ saints_NNS who_WP were_VBD martyred_VBN here — and_RB widely_RB scattered_VBN in_IN farmland_NN ,_, are_VBP the_DT remains_NNS of_IN Górtis_NNP (_NNP Gortyn_NNP )_NNP ,_, capital_NN of_IN the_DT island_NN during_IN the_DT Roman_JJ era_NN (_NN from_IN 65_CD b.c._NN )_NN and_CC also_RB an_DT important_JJ city_NN in_IN Minoan_NNP times_NNS ._.
Near_RB the_DT village_NN of_IN Agía_NNP Déka — named_VBN after_IN ten_JJ saints_NNS who_WP were_VBD martyred_VBN here — and_RB widely_RB scattered_VBN in_IN farmland_NN ,_, are_VBP the_DT remains_NNS of_IN Górtis_NNP (_NNP Gortyn_NNP )_NNP ,_, capital_NN of_IN the_DT island_NN during_IN the_DT Roman_JJ era_NN (_NN from_IN 65_CD b.c._NN )_NN and_CC also_RB an_DT important_JJ city_NN in_IN Minoan_NNP times_NNS ._.
On_IN the_DT streets_NNS around_IN the_DT park — each_NN named_VBN after_IN a_DT flower — there_NN are_VBP small_JJ hotels_NNS and_CC restaurants_NNS ,_, plus_CC portable_JJ stalls_NNS selling_VBG fresh_JJ fruit_NN juices_NNS or_CC hot_JJ Mexican_JJ snacks_NNS ._.
On_IN the_DT streets_NNS around_IN the_DT park — each_NN named_VBN after_IN a_DT flower — there_NN are_VBP small_JJ hotels_NNS and_CC restaurants_NNS ,_, plus_CC portable_JJ stalls_NNS selling_VBG fresh_JJ fruit_NN juices_NNS or_CC hot_JJ Mexican_JJ snacks_NNS ._.
The_DT Costa_NNP del_NNP Sol_NNP is_VBZ an_DT ideal_JJ place_NN for_IN vacationing_VBG families_NNS with_IN kids — it_NN is_VBZ ,_, after_IN all_DT ,_, one_CD long_JJ beach_NN ._.
When_WRB he_PRP finally_RB succeeded_VBD ,_, after_IN a_DT prolonged_JJ siege_NN and_CC heavy_JJ losses_NNS ,_, he_PRP punished_VBD the_DT local_JJ population_NN by_IN cutting_VBG off_RP the_DT noses_NNS and_CC lips_NNS of_IN all_DT men — except_NN those_DT who_WP played_VBD wind_NN instruments_NNS ._.
With_IN such_PDT a_DT long_JJ stretch_NN of_IN coast_NN to_TO cover_VB and_CC so_RB many_JJ historic_JJ towns_NNS to_TO visit_VB inland_NNP ,_, the_DT Costa_NNP Blanca_NNP may_MD seem_VB difficult_JJ to_TO navigate — particularly_RB if_IN you_PRP do_VBP n't_RB have_VB a_DT car_NN ._.
Within_IN a_DT day_NN 's_POS walk_NN are_VBP a_DT lake_NN and_CC streams_NNS with_IN good_JJ fishing_NN ,_, especially_RB for_IN trout_NN ,_, and_CC you_PRP 'll_MD have_VB a_DT fair_JJ chance_NN of_IN spotting_VBG some_DT of_IN the_DT park_NN 's_POS wildlife_NN ,_, too — bobcats_NNS ,_, coyotes_NNS ,_, golden_JJ eagles_NNS ,_, black_JJ bear_NN ,_, spotted_VBD skunk_NN ,_, and_CC cougar_NN ._.
You_PRP 'll_MD find_VB a_DT full_JJ range_NN of_IN sports_NNS offered_VBN :_: from_IN tennis_NN ,_, windsurfing_NN ,_, and_CC waterskiing_NN to_TO snorkeling_VBG and_CC diving — however_VB it_PRP is_VBZ fair_JJ to_TO say_VB that_IN the_DT underwater_JJ world_NN so_RB close_RB to_TO the_DT capital_NN can_MD be_VB disappointing_JJ ._.

```
Sentence 1565683 is filtered due to the way MXPOST processes certain characters:
```
The goal of the American Cancer Society , __ Unit , is to reach the employees and officers of every business in the county with important cancer information .
```

### Preprocessing
Splits are preprocessed with:
```
./preprocess.sh -x 045 -t mxpost -d mst -p rofames
```

### Training
```
./rofames.sh -m train -x 045 -t mxpost
```

### Decoding
```
./
```

### Scoring
```
./score.sh
```
