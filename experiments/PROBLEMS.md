# Problems with FN DATA

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


Excluded sentences are excluded from train.
Excluded frames (Test35) are from train and dev.

Following sentences are excluded as they lead to multiple roots with the MSTParser:
```
Partly as a result of the shortcomings in the Nuclear Non - Proliferation Treaty ( NPT ) safeguards system -- which allowed the rapid development of the Iraqi nuclear program in the 1970s and North Korea 's in the 1990s to go largely undetected -- and partly by assessing Iran 's intentions , the international community and the International Atomic Energy Agency ( IAEA ) have increased their scrutiny of Iran 's activities over the last several years .

The above groups pose the following dangers : 1- Attacking for the purpose of : A : Assassination B : Kidnapping C : Aerial raids and artillery attacks 2- Sabotage A : Setting fires B : Explosions C : Technical sabotage D : Chemical sabotage 3- Spying A : Recruiting a member of society B : Planting a mole within society C : Spying surveillance operation 4- Stealing 5- Pests : A : Poisonous such as snakes and scorpions B : Harmful such as rats and cockroaches C : Sickening such as mosquitoes

The distance between the first and fourth bump should be 100 meters , and the distance between the fourth and the sixth should be 50 meters , so cars can not travel fast in the direction of the building 5- Barbed Wires : They should be placed around the building , around the walls , or on top of the walls 6- Nails Obstacle : These are placed at the main gate in order to puncture the tires of any car crashing in
```

Problems in the test set with this sentence:
```
Because they just say there 's either no room in the system , you know , in the jails for them or , you know , it 's just that it seems like the automatic sentences - if - if a judge has leeway on what he 's going to , you know , sentence someone for between , you know , two months and uh fifty years and you know what 's his whim to decide it should be two months .
```
which produces the following (with multiple roots):

```
1	Because	_	because	_	IN	112	_	_	15	_	VMOD	_	_	O	_
2	they	_	they	_	PRP	112	_	_	4	_	SUB	_	_	O	_
3	just	_	just	_	RB	112	_	_	4	_	VMOD	_	_	O	_
4	say	_	say	_	VBP	112	_	_	1	_	SBAR	_	_	O	_
5	there	_	there	_	EX	112	_	_	6	_	SUB	_	_	O	_
6	's	_	's	_	VBZ	112	_	_	4	_	VMOD	_	_	O	_
7	either	_	either	_	DT	112	_	_	9	_	NMOD	_	_	O	_
8	no	_	no	_	DT	112	_	_	9	_	NMOD	_	_	O	_
9	room	_	room	_	NN	112	_	_	6	_	PRD	_	_	O	_
10	in	_	in	_	IN	112	_	_	9	_	NMOD	_	_	O	_
11	the	_	the	_	DT	112	_	_	12	_	NMOD	_	_	O	_
12	system	_	system	_	NN	112	_	_	10	_	PMOD	_	_	O	_
13	,	_	,	_	,	112	_	_	15	_	P	_	_	O	_
14	you	_	you	_	PRP	112	_	_	15	_	SUB	_	_	O	_
15	know	_	know	_	VBP	112	_	_	71	_	VMOD	_	_	O	_
16	,	_	,	_	,	112	_	_	15	_	P	_	_	O	_
17	in	_	in	_	IN	112	_	_	15	_	VMOD	_	_	O	_
18	the	_	the	_	DT	112	_	_	19	_	NMOD	_	_	O	_
19	jails	_	jail	_	NNS	112	_	_	17	_	PMOD	_	_	O	_
20	for	_	for	_	IN	112	_	_	19	_	NMOD	_	_	O	_
21	them	_	them	_	PRP	112	_	_	20	_	PMOD	_	_	O	_
22	or	_	or	_	CC	112	_	_	71	_	VMOD	_	_	O	_
23	,	_	,	_	,	112	_	_	25	_	P	_	_	O	_
24	you	_	you	_	PRP	112	_	_	25	_	SUB	_	_	S-Cognizer	Core
25	know	_	know	_	VBP	112	_	_	71	_	VMOD	know.v	Awareness	O	_
26	,	_	,	_	,	112	_	_	25	_	P	_	_	O	_
27	it	_	it	_	PRP	112	_	_	28	_	SUB	_	_	O	_
28	's	_	's	_	VBZ	112	_	_	71	_	VMOD	_	_	O	_
29	just	_	just	_	RB	112	_	_	30	_	AMOD	_	_	O	_
30	that	_	that	_	IN	112	_	_	28	_	PRD	_	_	O	_
31	it	_	it	_	PRP	112	_	_	32	_	SUB	_	_	O	_
32	seems	_	seem	_	VBZ	112	_	_	30	_	SBAR	_	_	O	_
33	like	_	like	_	IN	112	_	_	32	_	PRD	_	_	O	_
34	the	_	the	_	DT	112	_	_	36	_	NMOD	_	_	O	_
35	automatic	_	automatic	_	JJ	112	_	_	36	_	NMOD	_	_	O	_
36	sentences	_	sentence	_	NNS	112	_	_	33	_	PMOD	_	_	O	_
37	-	_	-	_	:	112	_	_	28	_	P	_	_	O	_
38	if	_	if	_	IN	112	_	_	28	_	VMOD	_	_	O	_
39	-	_	-	_	:	112	_	_	71	_	P	_	_	O	_
40	if	_	if	_	IN	112	_	_	53	_	VMOD	_	_	O	_
41	a	_	a	_	DT	112	_	_	42	_	NMOD	_	_	O	_
42	judge	_	judge	_	NN	112	_	_	43	_	SUB	_	_	O	_
43	has	_	have	_	VBZ	112	_	_	40	_	SBAR	_	_	O	_
44	leeway	_	leeway	_	VBN	112	_	_	43	_	VC	_	_	O	_
45	on	_	on	_	IN	112	_	_	44	_	VMOD	_	_	O	_
46	what	_	what	_	WP	112	_	_	45	_	PMOD	_	_	O	_
47	he	_	he	_	PRP	112	_	_	48	_	SUB	_	_	O	_
48	's	_	's	_	VBZ	112	_	_	46	_	SBAR	_	_	O	_
49	going	_	go	_	VBG	112	_	_	48	_	VC	_	_	O	_
50	to	_	to	_	TO	112	_	_	49	_	VMOD	_	_	O	_
51	,	_	,	_	,	112	_	_	53	_	P	_	_	O	_
52	you	_	you	_	PRP	112	_	_	53	_	SUB	_	_	O	_
53	know	_	know	_	VBP	112	_	_	61	_	VMOD	_	_	O	_
54	,	_	,	_	,	112	_	_	53	_	P	_	_	O	_
55	sentence	_	sentence	_	NN	112	_	_	56	_	NMOD	_	_	O	_
56	someone	_	someone	_	NN	112	_	_	53	_	OBJ	_	_	O	_
57	for	_	for	_	IN	112	_	_	56	_	NMOD	_	_	O	_
58	between	_	between	_	IN	112	_	_	57	_	PMOD	_	_	O	_
59	,	_	,	_	,	112	_	_	61	_	P	_	_	O	_
60	you	_	you	_	PRP	112	_	_	61	_	SUB	_	_	O	_
61	know	_	know	_	VBP	112	_	_	71	_	VMOD	_	_	O	_
62	,	_	,	_	,	112	_	_	68	_	P	_	_	O	_
63	two	_	#crd#	_	CD	112	_	_	64	_	NMOD	_	_	O	_
64	months	_	month	_	NNS	112	_	_	68	_	NMOD	_	_	O	_
65	and	_	and	_	CC	112	_	_	68	_	NMOD	_	_	O	_
66	uh	_	uh	_	JJ	112	_	_	68	_	NMOD	_	_	O	_
67	fifty	_	#crd#	_	JJ	112	_	_	68	_	NMOD	_	_	O	_
68	years	_	year	_	NNS	112	_	_	61	_	OBJ	_	_	O	_
69	and	_	and	_	CC	112	_	_	71	_	VMOD	_	_	O	_
70	you	_	you	_	PRP	112	_	_	71	_	SUB	_	_	O	_
71	know	_	know	_	VBP	112	_	_	0	_	ROOT	_	_	O	_
72	what	_	what	_	WP	112	_	_	71	_	VMOD	_	_	O	_
73	's	_	's	_	VBZ	112	_	_	0	_	ROOT	_	_	O	_
74	his	_	his	_	PRP$	112	_	_	75	_	NMOD	_	_	O	_
75	whim	_	whim	_	NN	112	_	_	73	_	PRD	_	_	O	_
76	to	_	to	_	TO	112	_	_	77	_	VMOD	_	_	O	_
77	decide	_	decide	_	VB	112	_	_	0	_	ROOT	_	_	O	_
78	it	_	it	_	PRP	112	_	_	79	_	SUB	_	_	O	_
79	should	_	should	_	MD	112	_	_	0	_	ROOT	_	_	O	_
80	be	_	be	_	VB	112	_	_	79	_	VC	_	_	O	_
81	two	_	#crd#	_	CD	112	_	_	82	_	NMOD	_	_	O	_
82	months	_	month	_	NNS	112	_	_	80	_	PRD	_	_	O	_
83	.	_	.	_	.	112	_	_	79	_	P	_	_	O	_
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
