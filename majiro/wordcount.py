# encoding: utf-8
import fileinput

if __name__ == '__main__':
    out_agg={}
    for line in fileinput.input():
        line = line.decode('shift-jis')
        ls = line.strip()
        fn = fileinput.filename()
        if len(ls) == 0: continue
        if ls[0] == '*':
            out_agg[fn]= out_agg.setdefault(fn,0)+len(line.split(" "))
        elif len(ls) >1 and ls[0:2] == u'「「':
            out_agg[fn]= out_agg.setdefault(fn,0)+len(line.split(" "))

    s = []
    for fn, lines in out_agg.iteritems():
        s.append((fn,lines))

    s.sort()
    for f,l in s:
        print f, l
