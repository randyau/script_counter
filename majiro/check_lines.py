# encoding: utf-8
import fileinput
import operator

def check_line_ok(line):
    "True if line is good, False if line is bad"
    line = line.decode('shift-jis')
    l = line.split()

    if len(line.strip()) == 0: return True
    if line.strip()[-1] == '\\':
        return True
    elif line[0:2] in [u'「「','\r\n','\s']:
        return True
    elif line[0] in ['*','/','$', '','\n','#']:
        return True
    elif l[0] in ['goto','mov','void']:
        return True
    else:
        return False

if __name__=='__main__':
    out_agg = []
    for line in fileinput.input():
        if not check_line_ok(line):
            fn = fileinput.filename()
            ln = fileinput.filelineno()
            out_agg.append([fn, ln, line.replace("\n",'')])

    out_agg.sort(key=operator.itemgetter(2,0,1))
    for fn, ln, line in out_agg:
        print "@", line, "@", fn, ln
