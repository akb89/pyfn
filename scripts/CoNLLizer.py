#! /usr/bin/env python3
#!
import os, re, sys
import argparse, contextlib, functools
from collections import defaultdict

def brown_to_conll(bdelim, sdelim, cdelim, filepath, insert_ids=False):
    with open(filepath) as stream:
        for line in stream:
            line = line.strip()
            items = line.split(sdelim)
            for i, it in enumerate(items):
                columns = it.split(bdelim)
                if insert_ids:
                    columns.insert(0, str(i+1))
                print(cdelim.join(columns))
            print("")

def convert_to_range(seq):
    seq = [int(s) for s in seq.split('-')]
    return list(range(seq[0], seq[1]+1))

def check_fields_description(fields):
    re_fields = re.compile("(([0-9]+(-[0-9]+)*),)*([0-9]+(-[0-9]+)*)")
    m = re_fields.match(fields)

    if m is not None:
        length = m.span()[1]
        return length == len(fields)
    return False

def check_range(r):
    re_range = re.compile("[0-9]+-[0-9]+")
    m = re_range.match(r)
    return m is not None

def check_replace_columns(cols):
    try:
        for c in cols:
            c = int(c)
            if c < 0:
                return False
    except ValueError:
        return False
    return True

def check_replace_with(cols, withs):
    return len(cols) == len(withs)

def conllize(delim, fields, files, cols = [], withs = []):
    final_fields = []
    replacements = dict(zip([int(c) for c in cols], withs))
    for info in fields.split(','):
        if check_range(info):
            final_fields.extend(convert_to_range(info))
        else:
            final_fields.append(int(info))

    with contextlib.ExitStack() as stack:
        files = [stack.enter_context(open(fname)) for fname in files]
        for lines in zip(*files):
            lines = [line.strip() for line in lines]
            lines = filter(lambda l: l != '', lines)
            lines = delim.join(lines)
            if lines == '':
                print("")
                continue
            items = lines.split(delim)
            selection = []
            for f in final_fields:
                if f-1 >= len(items):
                    print("Field %i not recoverable, exit..." % f, file=sys.stderr)
                    sys.exit(1)

                if f in replacements:
                    selection.append(replacements[f])
                else:
                    selection.append(items[f-1])
            print(delim.join(selection))

def flatten(delim, cdelim, fields, files, cols = [], withs = [], count_tokens = False):
    final_fields = []
    replacements = dict(zip([int(c) for c in cols], withs))
    for info in fields.split(','):
        if check_range(info):
            final_fields.extend(convert_to_range(info))
        else:
            final_fields.append(int(info))

    with contextlib.ExitStack() as stack:
        files = [stack.enter_context(open(fname)) for fname in files]

        selection = defaultdict(list)
        for lines in zip(*files):
            lines = [line.strip() for line in lines]
            lines = filter(lambda l: l != '', lines)
            lines = delim.join(lines)

            if lines == '':
                mline = []
                toknum = 0
                for f in final_fields:
                    info = selection[f]
                    toknum = len(info)
                    mline.append( delim.join(info) )

                if count_tokens:
                    mline.insert(0, "%i" % toknum)

                print(delim.join(mline))
                selection = defaultdict(list)
                continue

            items = lines.split(cdelim)
            for f in final_fields:
                if f-1 >= len(items):
                    print("Field %i not recoverable, exit..." % f, file=sys.stderr)
                    sys.exit(1)

                if f in replacements:
                    selection[f].append(replacements[f])
                else:
                    selection[f].append(items[f-1])


def make_parser():
    parser = argparse.ArgumentParser(prog='CoNLLizer')
    subs = parser.add_subparsers(dest='commands')
    subs.required = True

    brown = subs.add_parser('brown', help="Convert Brown format to CoNLL", prog="CoNLLizer")
    brown.add_argument('-d', '--delim', default='_', help='Delimiter between token and part-of-speech (default to tab)')
    brown.add_argument('-D', '--sdelim', default=' ', help='Delimiter between two elements (default to space)')
    brown.add_argument('-C', '--cdelim', default='\t', help='CoNLL delimiter (default to tab)')
    brown.add_argument('-i', '--insert-id', action='store_true', help='Insert ID (from 1 to n) in front of the columns?')
    brown.add_argument('files', nargs='?', help='Absolute path to the file')

    conllize = subs.add_parser('conll', help="Convert to CoNLL", prog="CoNLLizer")
    conllize.add_argument('-d', '--delim', default='\t', help='CoNLL delimiter (default to tab)')

    flatten = subs.add_parser('flatten', help="Flatten CoNLL", prog="CoNLLizer")
    flatten.add_argument('-d', '--delim', default='\t', help='Delimiter (default to tab)')
    flatten.add_argument('-C', '--cdelim', default='\t', help='CoNLL delimiter (default to tab)')
    flatten.add_argument('-c', '--count-tokens', action='store_true', help='Count number of tokens and put it at the beginning of the line')

    for p in [flatten, conllize]:
        p.add_argument('-f', '--fields', required=True, help='Fields to extract. Ranges are accepted, repeated columns too, possibility to invert columns (e.g: 7,1-2,4,3,6,3)')
        p.add_argument('-r', '--replace-col', action='append', help='Replace a column number (should be used with --with)')
        p.add_argument('-w', '--with', dest='withs', action='append', help='Text sequence used to replace a column (should be used with --replace-col)')
        p.add_argument('files', nargs='+', help='Absolute path to files')

    bios = subs.add_parser('bios', help="Merge BIOS and CoNLL", prog="CoNLLizer")

    return parser

def main():
    parser = make_parser()
    args = parser.parse_args()

    if args.commands == 'brown':
        return brown_to_conll(args.delim, args.sdelim, args.cdelim, args.files, args.insert_id)
    elif args.commands == 'conll' or args.commands == 'flatten':
        if not check_fields_description(args.fields):
            print("The field selection is not correct", file=sys.stderr)
            print("It should be either a number or a range or a combination of both separated by commas with no spaces", file=sys.stderr)
            sys.exit(1)

        cols = []
        if args.replace_col:
            cols = args.replace_col

        withs = []
        if args.withs:
            withs = args.withs

        if not check_replace_columns(cols):
            print("Columns in --replace-col should be positive integers")
            sys.exit(1)
        if not check_replace_with(cols, withs):
            print("--replace-col and --with should be called the same number of times")
            sys.exit(1)

        if args.commands == 'conll':
            return conllize(args.delim, args.fields, args.files, cols, withs)
        elif args.commands == 'flatten':
            return flatten(args.delim, args.cdelim, args.fields, args.files, cols, withs, args.count_tokens)
    elif args.commands == 'bios':
        pass

if __name__ == "__main__":
    main()
