#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import sys
import wordcount
import argparse


def remove_comments(line, comment_chars=["//","#","$"]):
    """culls out lines that are marked w/ leading comment characters, emits empty
    tring if a commented line is found"""
    emit = True
    comment_trigger = ''
    for comment_mark in comment_chars:
        if line.strip()[:len(comment_mark)] == comment_mark:
            comment_trigger = comment_mark
            emit=False
    if emit:
        return (line,None)
    else:
        return ('',(comment_trigger,line))

def read_charfile(fn):
    output = []
    for line in open(fn,'r'):
        output.append(line)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Try to count text and asian characters.')
    parser.add_argument("-c", "--char_file", type=str, dest="char_file", default="", help="""Lines starting with these characters are ignored, one per line""")
    parser.add_argument("-e","--encoding", type=str, dest="encoding",default="shift_jis", help="Input encoding, shift_jis, utf-8, etc")
    args = parser.parse_args()
    encoding = args.encoding
    char_fn = args.char_file

    if char_fn == "":
        comments_list = []
    else:
        comment_list = read_charfile(char_fn)

    full_text = []
    dropped_dict = {}
    istream = codecs.getreader(encoding)(sys.stdin)
    line_counter = 0

    for line in istream:
        line, dropped = remove_comments(line,comment_chars = comment_list)
        full_text.append(line)
        if len(line.strip()) != 0: line_counter += 1
        if dropped != None:
            comment_trigger, bad_line= dropped
            dropped_dict.setdefault(comment_trigger,[]).append(bad_line)


    wc = wordcount.get_wordcount(''.join(full_text))
    print "TEXT:",wc
    print "COUNTED LINES WITH TEXT::", line_counter
    for k,v in dropped_dict.iteritems():
        count = wordcount.get_wordcount(''.join(v))
        print "DROPPED (%s):" % (k,), count
