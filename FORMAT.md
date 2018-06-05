# Format

## FrameNet XML
```xml
<sentence corpID="135" docID="23605" sentNo="5" paragNo="7" aPos="0" ID="4099596">
        <text>' I think , overall , things went very well , ' said Lawton Davis , head of the South Central Health District .</text>
        <annotationSet cDate="06/06/2006 02:39:48 PDT Tue" status="UNANN" ID="6534937">
            <layer rank="1" name="PENN">
                <label end="0" start="0" name="''"/>
                <label end="2" start="2" name="PP"/>
                <label end="8" start="4" name="VVP"/>
                <label end="10" start="10" name=","/>
                <label end="18" start="12" name="rb"/>
                <label end="20" start="20" name=","/>
                <label end="27" start="22" name="nns"/>
                <label end="32" start="29" name="VVD"/>
                <label end="37" start="34" name="rb"/>
                <label end="42" start="39" name="rb"/>
                <label end="44" start="44" name=","/>
                <label end="46" start="46" name="''"/>
                <label end="51" start="48" name="VVD"/>
                <label end="58" start="53" name="NP"/>
                <label end="64" start="60" name="NP"/>
                <label end="66" start="66" name=","/>
                <label end="71" start="68" name="nn"/>
                <label end="74" start="73" name="in"/>
                <label end="78" start="76" name="dt"/>
                <label end="84" start="80" name="NP"/>
                <label end="92" start="86" name="NP"/>
                <label end="99" start="94" name="NP"/>
                <label end="108" start="101" name="NP"/>
                <label end="110" start="110" name="sent"/>
            </layer>
            <layer rank="1" name="NER">
                <label end="64" start="53" name="person"/>
                <label end="108" start="80" name="organization"/>
            </layer>
            <layer rank="1" name="WSL">
                <label end="0" start="0" name="NT"/>
                <label end="2" start="2" name="NT"/>
                <label end="10" start="10" name="NT"/>
                <label end="18" start="12" name="NT"/>
                <label end="20" start="20" name="NT"/>
                <label end="37" start="34" name="NT"/>
                <label end="42" start="39" name="NT"/>
                <label end="44" start="44" name="NT"/>
                <label end="46" start="46" name="NT"/>
                <label end="58" start="53" name="NT"/>
                <label end="64" start="60" name="NT"/>
                <label end="66" start="66" name="NT"/>
                <label end="74" start="73" name="NT"/>
                <label end="78" start="76" name="NT"/>
                <label end="84" start="80" name="NT"/>
                <label end="92" start="86" name="NT"/>
                <label end="99" start="94" name="NT"/>
                <label end="108" start="101" name="NT"/>
                <label end="110" start="110" name="NT"/>
            </layer>
        </annotationSet>
        <annotationSet cDate="06/12/2006 03:43:02 PDT Mon" luID="169" luName="think.v" frameID="19" frameName="Awareness" status="MANUAL" ID="6535298">
            <layer rank="1" name="Target">
                <label cBy="RLG" end="8" start="4" name="Target"/>
            </layer>
            <layer rank="1" name="FE">
                <label cBy="RLG" feID="83" bgColor="FF0000" fgColor="FFFFFF" end="2" start="2" name="Cognizer"/>
                <label cBy="RLG" feID="84" bgColor="0000FF" fgColor="FFFFFF" end="42" start="12" name="Content"/>
            </layer>
            <layer rank="1" name="GF">
                <label end="2" start="2" name="Ext"/>
                <label end="42" start="12" name="Dep"/>
            </layer>
            <layer rank="1" name="PT">
                <label end="2" start="2" name="NP"/>
                <label end="42" start="12" name="Sfin"/>
            </layer>
            <layer rank="1" name="Other"/>
            <layer rank="1" name="Sent"/>
            <layer rank="1" name="Verb"/>
        </annotationSet>
        <annotationSet cDate="06/12/2006 03:43:45 PDT Mon" luID="751" luName="say.v" frameID="43" frameName="Statement" status="MANUAL" ID="6535299">
            <layer rank="1" name="Target">
                <label cBy="RLG" end="51" start="48" name="Target"/>
            </layer>
            <layer rank="1" name="FE">
                <label cBy="RLG" feID="185" bgColor="00BFFF" fgColor="FFFFFF" end="46" start="0" name="Message"/>
                <label cBy="RLG" feID="183" bgColor="FF0000" fgColor="FFFFFF" end="108" start="53" name="Speaker"/>
            </layer>
            <layer rank="1" name="GF">
                <label end="46" start="0" name="Head"/>
                <label end="108" start="53" name="Ext"/>
            </layer>
            <layer rank="1" name="PT">
                <label end="46" start="0" name="QUO"/>
                <label end="108" start="53" name="NP"/>
            </layer>
            <layer rank="1" name="Other"/>
            <layer rank="1" name="Sent"/>
            <layer rank="1" name="Verb"/>
        </annotationSet>
        <annotationSet cDate="06/12/2006 03:49:28 PDT Mon" luID="1588" luName="head.n" frameID="73" frameName="Leadership" status="MANUAL" ID="6535300">
            <layer rank="1" name="Target">
                <label cBy="RLG" end="71" start="68" name="Target"/>
            </layer>
            <layer rank="1" name="FE">
                <label cBy="RLG" feID="6431" bgColor="0000FF" fgColor="FFFFFF" end="108" start="73" name="Governed"/>
                <label cBy="KmG" feID="347" bgColor="FF0000" fgColor="FFFFFF" end="71" start="68" name="Leader"/>
            </layer>
            <layer rank="1" name="GF">
                <label end="108" start="73" name="Dep"/>
            </layer>
            <layer rank="1" name="PT">
                <label end="108" start="73" name="PP"/>
            </layer>
            <layer rank="1" name="Other"/>
            <layer rank="1" name="Sent"/>
            <layer rank="1" name="Noun"/>
        </annotationSet>
    </sentence>
```

## BIOS
```
1	'	_	'	_	''	0	_	_	3	_	punct	_	_	O	_
2	I	_	I	_	PRP	0	_	_	3	_	nsubj	_	_	S-Cognizer	Core
3	think	_	think	_	VBP	0	_	_	13	_	ccomp	think.v	Awareness	O	_
4	,	_	,	_	,	0	_	_	3	_	punct	_	_	O	_
5	overall	_	overall	_	RB	0	_	_	8	_	advmod	_	_	B-Content	Core
6	,	_	,	_	,	0	_	_	8	_	punct	_	_	I-Content	Core
7	things	_	thing	_	NNS	0	_	_	8	_	nsubj	_	_	I-Content	Core
8	went	_	go	_	VBD	0	_	_	3	_	ccomp	_	_	I-Content	Core
9	very	_	very	_	RB	0	_	_	10	_	advmod	_	_	I-Content	Core
10	well	_	well	_	RB	0	_	_	8	_	advmod	_	_	I-Content	Core
11	,	_	,	_	,	0	_	_	13	_	punct	_	_	O	_
12	'	_	'	_	''	0	_	_	13	_	punct	_	_	O	_
13	said	_	say	_	VBD	0	_	_	0	_	root	_	_	O	_
14	Lawton	_	lawton	_	NNP	0	_	_	15	_	nn	_	_	O	_
15	Davis	_	davis	_	NNP	0	_	_	13	_	nsubj	_	_	O	_
16	,	_	,	_	,	0	_	_	15	_	punct	_	_	O	_
17	head	_	head	_	NN	0	_	_	15	_	appos	_	_	O	_
18	of	_	of	_	IN	0	_	_	17	_	prep	_	_	O	_
19	the	_	the	_	DT	0	_	_	23	_	det	_	_	O	_
20	South	_	south	_	NNP	0	_	_	23	_	nn	_	_	O	_
21	Central	_	central	_	NNP	0	_	_	23	_	nn	_	_	O	_
22	Health	_	health	_	NNP	0	_	_	23	_	nn	_	_	O	_
23	District	_	district	_	NNP	0	_	_	18	_	pobj	_	_	O	_
24	.	_	.	_	.	0	_	_	13	_	punct	_	_	O	_
```

## CoNLL
```
1	0.0	3	Awareness	think.v	2	think	0	Cognizer	1	Content	4:9
1	0.0	3	Statement	say.v	12	said	0	Message	0:11	Speaker	13:22
1	0.0	3	Leadership	head.n	16	head	0	Governed	17:22	Leader	16
```

```
1	'	'	''	''	_	3	punct	_	_
2	I	I	PRP	PRP	_	3	nsubj	_	_
3	think	think	VBP	VBP	_	13	ccomp	_	_
4	,	,	,	,	_	3	punct	_	_
5	overall	overall	RB	RB	_	8	advmod	_	_
6	,	,	,	,	_	8	punct	_	_
7	things	thing	NNS	NNS	_	8	nsubj	_	_
8	went	go	VBD	VBD	_	3	ccomp	_	_
9	very	very	RB	RB	_	10	advmod	_	_
10	well	well	RB	RB	_	8	advmod	_	_
11	,	,	,	,	_	13	punct	_	_
12	'	'	''	''	_	13	punct	_	_
13	said	say	VBD	VBD	_	0	root	_	_
14	Lawton	lawton	NNP	NNP	_	15	nn	_	_
15	Davis	davis	NNP	NNP	_	13	nsubj	_	_
16	,	,	,	,	_	15	punct	_	_
17	head	head	NN	NN	_	15	appos	_	_
18	of	of	IN	IN	_	17	prep	_	_
19	the	the	DT	DT	_	23	det	_	_
20	South	south	NNP	NNP	_	23	nn	_	_
21	Central	central	NNP	NNP	_	23	nn	_	_
22	Health	health	NNP	NNP	_	23	nn	_	_
23	District	district	NNP	NNP	_	18	pobj	_	_
24	.	.	.	.	_	13	punct	_	_
```

## SEMEVAL XML
