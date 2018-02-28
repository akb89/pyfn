# Scripts

## CoNLLizer
Each command help can be printed using 

```bash
./CoNLLizer command_name -h
```

### brown command
The *brown* command transform the brown format (i.e. token1_POS1 token2_POS2 ...) to a CoNLL format. 
Using the ``-i`` option, the command will create the token numbers for you.

### conll command
The *conll* command transform a serie of CoNLL-like files and extract some columns in a predefined order.

For instance using ``-f 1,2,4-6,2`` will take the first column, the second column, the fourth, fifth and sixth one and repeat the second one at the end.

Using ``-r`` in conjonction with ``-w`` allows to replace a column by a string

### flatten command
TBA

### bios command
TBA
