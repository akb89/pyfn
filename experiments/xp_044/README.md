# XP\#044

open-sesame on FN 1.5 FT with MXPOST + MST

### Test scores
| P| R | F1 |
| --- | --- | --- |
| 65.6 | 59.7 | 62.5 |

### Splits generation
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev
  --target /path/to/experiments/xp_044/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
  --filter overlap_fes
```

Former:
```
pyfn convert \
  --from fnxml \
  --to bios \
  --source /path/to/fndata-1.5-with-dev
  --target /path/to/experiments/xp_044/data \
  --splits train \
  --output_sentences \
  --excluded_frames 398 \
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

### Data preparation
```
./prepare.sh -x 044 -p open-sesame -s test -f /path/to/fndata-1.5-with-dev
```

### Preprocessing
```
./preprocess.sh -x 044 -t mxpost -p open-sesame -d mst -v
```

### Training
```
./open-sesame.sh -m train -x 044 -d
```

### Decoding
```
./open-sesame.sh -m decode -x 044 -s test -d
```

### Scoring
```
./score.sh
```

### Problems
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
