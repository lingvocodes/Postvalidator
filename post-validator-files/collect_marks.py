import re, codecs

def marks_list(doc):
    a = []
    f = codecs.open(doc, 'r', 'utf-8')
    for line in f:
        line = line.strip(u'\r\n')
        a.append(line)
    return a

