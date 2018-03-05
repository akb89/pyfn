#! /usr/bin/env python3

import os, re, sys
import argparse, contextlib, functools
from collections import defaultdict

def convert_to_range(seq, prefixes = []):
    if len(prefixes) > 0:
        re_prefixes = '(%s)' % '|'.join(prefixes)
    else:
        re_prefixes = ''

    re_range = re.compile(re_prefixes+"([0-9]+-[0-9]+)")

    m = re_range.match(seq)

    if len(prefixes) > 0:
        seq = [int(s) for s in m.group(2).split('-')]
    else:
        seq = [int(s) for s in m.group(1).split('-')]

    if len(prefixes) > 0:
        return [(m.group(1), r) for r in range(seq[0], seq[1]+1)]
    return list(range(seq[0], seq[1]+1))


def convert_to_int(info, prefixes = []):
    if len(prefixes) > 0:
        re_prefixes = '(%s)' % '|'.join(prefixes)
    else:
        re_prefixes = ''

    re_range = re.compile(re_prefixes+"([0-9]+)")
    m = re_range.match(info)

    if len(prefixes) > 0:
        seq = int(m.group(2))
    else:
        seq = int(m.group(1))

    if len(prefixes) > 0:
        return (m.group(1), seq)
    return seq

def check_fields_description(fields, prefixes = []):
    if len(prefixes) > 0:
        re_prefixes = '(?:%s)' % '|'.join(prefixes)
    else:
        re_prefixes = ''

    re_fields = re.compile("(("+re_prefixes+"[0-9]+(-[0-9]+)*),)*("+re_prefixes+"[0-9]+(-[0-9]+)*)")
    m = re_fields.match(fields)

    if m is not None:
        length = m.span()[1]
        return length == len(fields)
    return False

def check_range(r, prefixes = []):
    if len(prefixes) > 0:
        re_prefixes = '(?:%s)' % '|'.join(prefixes)
    else:
        re_prefixes = ''

    re_range = re.compile(re_prefixes+"[0-9]+-[0-9]+")
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

def check_chars_and_masks(chars, masks):
    return len(chars) == len(masks)

def transform_fields(fields, prefixes = []):
    final_fields = []
    for info in fields.split(','):
        if check_range(info, prefixes):
            final_fields.extend(convert_to_range(info, prefixes))
        else:
            final_fields.append(convert_to_int(info, prefixes))
    return final_fields

def brown_to_conll(bdelim, sdelim, cdelim, filepath, insert_ids=False):
    with open(filepath) as stream:
        for line in stream:
            line = line.strip()
            items = re.split(sdelim, line)
            for i, it in enumerate(items):
                columns = it.split(bdelim)
                if insert_ids:
                    columns.insert(0, str(i+1))
                print(cdelim.join(columns))
            print("")


def conllize(delim, fields, files, cols = [], withs = []):
    final_fields = transform_fields(fields)
    replacements = dict(zip([int(c) for c in cols], withs))

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
    final_fields = transform_fields(fields)
    replacements = dict(zip([int(c) for c in cols], withs))

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
            for f in set(final_fields):
                if f-1 >= len(items):
                    print("Field %i not recoverable, exit..." % f, file=sys.stderr)
                    sys.exit(1)

                if f in replacements:
                    selection[f].append(replacements[f])
                else:
                    selection[f].append(items[f-1])

def mask_chars(direction, filepath, chars, masks, is_conll = False, fields = '', delim = '\t'):
    def apply(content):
        for char, mask in zip(chars, masks):
            if direction == 'mask':
                content = content.replace(char, mask)
            else:
                content = content.replace(mask, char)
        return content

    final_fields = []
    if is_conll:
        final_fields = transform_fields(fields)

    with open(filepath) as stream:
        for line in stream:
            line = line.strip()
            if is_conll:
                if line == "":
                    print("")
                    continue

                items = line.split(delim)
                for f in final_fields:
                    if f-1 >= len(items):
                        print("Field %i not recoverable, exit..." % f, file=sys.stderr)
                        sys.exit(1)
                    items[f-1] = apply(items[f-1])
                print(delim.join(items))
            else:
                line = apply(line)
                print(line)

def bios(conll_files, bios_files, fields):
    final_fields = transform_fields(fields, prefixes = ['b', 'c'])

    with contextlib.ExitStack() as stack:
        conll_files = [stack.enter_context(open(fname)) for fname in conll_files]
        bios_files = [stack.enter_context(open(fname)) for fname in bios_files]

        conll_sentences = []
        conll_sentence  = []
        for lines in zip(*conll_files):
            lines = [line.strip() for line in lines]
            lines = filter(lambda l: l != '', lines)
            lines = '\t'.join(lines)
            if lines == "":
                conll_sentences.append(conll_sentence)
                conll_sentence = []
                continue
            conll_sentence.append(lines.split('\t'))

        i = 0
        for lines in zip(*bios_files):
            lines = [line.strip() for line in lines]
            lines = filter(lambda l: l != '', lines)
            lines = '\t'.join(lines)

            if lines == '':
                i = 0
                print("")
                continue

            items = lines.split('\t')
            sent_num = int(items[6])
            conll_items = conll_sentences[sent_num][i]
            selection = []
            for (t, f) in final_fields:
                if f-1 >= len(items):
                    print("Field %i not recoverable, exit..." % f, file=sys.stderr)
                    sys.exit(1)

                if t == 'b':
                    selection.append(items[f-1])
                else:
                    selection.append(conll_items[f-1])
            i += 1
            print('\t'.join(selection))


def make_parser():
    parser = argparse.ArgumentParser(prog='CoNLLizer')
    subs = parser.add_subparsers(dest='commands')
    subs.required = True

    masker = subs.add_parser('mask', help='Mask some chars to avoid conflicts with subsequent preprocessors')
    masker.add_argument('-s', '--string', action='append', help='String to replace')
    masker.add_argument('-m', '--mask', action='append', help='Mask to use')

    unmasker = subs.add_parser('unmask', help='Unmask some chars to avoid conflicts with subsequent preprocessors')
    unmasker.add_argument('-s', '--string', action='append', help='Original string')
    unmasker.add_argument('-m', '--mask', action='append', help='Mask to unmask')

    for p in [unmasker, masker]:
        p.add_argument('-f', '--fields', default='', help='Fields for replacement (same description as for flatten or conll commands)')
        p.add_argument('-c', '--conll', action='store_true', help='Use CoNLL')
        p.add_argument('-d', '--delim', default='\t', help='CoNLL delimiter')
        p.add_argument('file', nargs='?', help='Absolute path to the file')

    brown = subs.add_parser('brown', help="Convert Brown format to CoNLL", prog="CoNLLizer")
    brown.add_argument('-d', '--delim', default='_', help='Delimiter between token and part-of-speech (default to tab)')
    brown.add_argument('-D', '--sdelim', default='\\s+', help='Delimiter between two elements (default to multi spaces)')
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
    bios.add_argument('-c', '--conll', action='append', required=True, help='CoNLL files (may be repeated)')
    bios.add_argument('-b', '--bios', action='append', required=True, help='BIOS files (may be repeated)')
    bios.add_argument('-f', '--fields', required=True, \
        help='Final fields ordering. You should prefix field (or range) by c for CoNLL et b for Bios (eg c1,b4-6,c2,b7,b7)')

    return parser

def main():
    parser = make_parser()
    args = parser.parse_args()

    if args.commands == 'brown':
        return brown_to_conll(args.delim, args.sdelim, args.cdelim, args.files, args.insert_id)
    elif args.commands == 'unmask' or args.commands == 'mask':
        if not check_chars_and_masks(args.string, args.mask):
            print('You should put as many chars as masks')
            sys.exit(1)

        if args.conll and not check_fields_description(args.fields):
            print("The field selection is not correct", file=sys.stderr)
            print("It should be either a number or a range or a combination of both separated by commas with no spaces", file=sys.stderr)
            sys.exit(1)
        mask_chars(args.commands, args.file, args.string, args.mask, args.conll, args.fields, args.delim)
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
        if not check_fields_description(args.fields, prefixes = ['b', 'c']):
            print("The field selection is not correct", file=sys.stderr)
            print("It should be either a number or a range or a combination of both separated by commas with no spaces and prefixed by 'c' or 'b'", file=sys.stderr)
            sys.exit(1)
        return bios(args.conll, args.bios, args.fields)


if __name__ == "__main__":
    main()
