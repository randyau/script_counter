# encoding: utf-8
import fileinput

if __name__ == '__main__':
    for line in fileinput.input():
        line = line.decode('shift-jis')
        ls = line.strip()
        fn = fileinput.filename()
        if len(ls) == 0: continue
        if ls[0] == '*':
            print line[1:].encode('utf-8').strip()
        elif len(ls) >1 and ls[0:2] == u'「「':
            print line[2:].encode('utf-8').strip()

