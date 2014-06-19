import re, codecs
from basic import *

def preparator(source):

    def clean_tags(line):

        
        def remove_trash(line, trash_regexp, subst):
            m = re.search(trash_regexp, line)
            if m != None:
                line = re.sub(m.group(1), subst, line)
                ## print line
            return line

        def start_line_cleaner(line):
            m = re.search(u'(<p> ?</[ibu]>)', line)
            if m != None:
                line = re.sub(m.group(1), u'<p>', line)
            return line

        def style_line_cleaner(line):
            m = re.search(u'(<h4 style.+?[^<>]>)', line)
            if m != None:
                line = re.sub(m.group(1), u'<p>', line)
            return line

        def remove_repeating_tags_nospace(line):
            arr = [u'i', u'b', u'u', u'i', u'b', u'u']
            for i in arr:
                regexp = re.compile(u'</' + i + u'><' + i + u'>')
                line = re.sub(regexp, u'', line)
            return line

        def remove_repeating_tags_space(line):
            arr = [u'i', u'b', u'u', u'i', u'b', u'u']
            for i in arr:
                regexp = re.compile(u'(</' + i + u'>( *)<' + i + u'>)')
                m = re.search(regexp, line)
                while m != None:
                    line = re.sub(m.group(1), m.group(2), line)
                    m = re.search(regexp, line)
            return line

        def remove_empty_tags(line):
            arr = [u'i', u'b', u'u', u'i', u'b', u'u']
            for i in arr:
                regexp = re.compile(u'(<' + i + u'>( *)</' + i + u'>)')
                m = re.search(regexp, line)
                while m != None:
                    line = re.sub(m.group(1), m.group(2), line)
                    m = re.search(regexp, line)
            return line

        trash_subst_cor = [(u"(<p .+?[^<>]>)", u'<p>'),
                           (u"(<b .+?[^<>]>)", u'<b>'),
                           (u"(<i .+?[^<>]>)", u'<i>')]
        for pair in trash_subst_cor:
            line = remove_trash(line, pair[0], pair[1])
        
        line = re.sub(u'</span>', u'', line)
        line = re.sub(u'<istyle.+?[^<>]>', u'<i>', line)
        line = re.sub(u'<bstyle.+?[^<>]>', u'<b>', line)
        line = re.sub(u'<i style.+?[^<>]>', u'<i>', line)
        line = re.sub(u'<b style.+?[^<>]>', u'<b>', line)
        line = re.sub(u'</h4>', u'</p>', line)

        def remove_span(line, span_mark):
            m = re.search(u"(<" + span_mark + ".+?[^<]>)", line)
            while m != None:
                line = re.sub(m.group(1), u'', line)
                m = re.search(u'(<' + span_mark + '.+?[^<]>)', line)
    ##        print line
            return line

        span_marks = [u'span ', 'spanclass', 'spanlang', 'spanstyle', 'strong']
        for i in span_marks:
            line = remove_span(line, i)
        
        
        line = remove_repeating_tags_nospace(line)
        line = remove_repeating_tags_space(line)
        line = remove_empty_tags(line)
        line = start_line_cleaner(line)
        line = style_line_cleaner(line)

        return line




    coding = raw_input(u'Введите кодировку файла:\n>>> ')
    if coding == u'':
        coding = 'cp1251'
    src = codecs.open(source, 'r', coding)
    

    doc = ''

    for line in src:
        new_line = line.strip(u'\r\n')
        new_line = re.sub(u'<br>', u'</p><p>', new_line)
        new_line = re.sub(u'^', u'', new_line)
        doc += new_line
        doc += u' '

    m = re.search(u'(<body.*body>)', doc)
    if m != None:
        doc = m.group(1)

    doc = re.sub(u'<o:p></o:p>', u'', doc)
    doc = re.sub(u'<o:p>&nbsp;</o:p>', u'', doc)
                      
    text = doc.split(u'</p>')
    text_final = []

    m = re.search(u"(<body .+?[^<>]>)", text[0])
    if m != None:
        text[0] = re.sub(m.group(1), u'', text[0])

    m = re.search(u"(<div .+?[^<>]>)", text[0])
    if m != None:
        text[0] = re.sub(m.group(1), u'', text[0])

    line = re.sub(u'<br>', u'</p><p>', line)

    for i in text:
        if i != u'</div></body>':
            s = clean_tags(i)
            s += u'</p>'
            text_final.append(s)

    src.close()

    print 'source has been prepared...'

    return text_final

def double_space_remover(line):
    line = re.sub(u'  ', u' ', line)
    return line

def remove_trash(line, trash_regexp, subst):
    m = re.search(trash_regexp, line)
    if m != None:
        line = re.sub(m.group(1), subst, line)
    return line

def start_line_cleaner(line):
    m = re.search(u'(<p> ?</[ibu]>)', line)
    if m != None:
        line = re.sub(m.group(1), u'<p>', line)
    return line

def style_line_cleaner(line):
    m = re.search(u'(<h4 style.+?[^<>]>)', line)
    if m != None:
        line = re.sub(m.group(1), u'<p>', line)
    return line

def remove_repeating_tags_nospace(line):
    arr = [u'i', u'b', u'u', u'i', u'b', u'u']
    for i in arr:
        regexp = re.compile(u'</' + i + u'><' + i + u'>')
        line = re.sub(regexp, u'', line)
    return line

def remove_repeating_tags_space(line):
    arr = [u'i', u'b', u'u', u'i', u'b', u'u']
    for i in arr:
        regexp = re.compile(u'(</' + i + u'>( *)<' + i + u'>)')
        m = re.search(regexp, line)
        while m != None:
            line = re.sub(m.group(1), m.group(2), line)
            m = re.search(regexp, line)
    return line

def remove_empty_tags(line):
    arr = [u'i', u'b', u'u', u'i', u'b', u'u']
    for i in arr:
        regexp = re.compile(u'(<' + i + u'>( *)</' + i + u'>)')
        m = re.search(regexp, line)
        while m != None:
            line = re.sub(m.group(1), m.group(2), line)
            m = re.search(regexp, line)
    return line

def remove_index(line):
    m = re.search(u'(<sup>([0-9])</sup>)', line)
    if m != None:
        new_line = re.sub(m.group(1), u'', line)
    else:
        new_line = line
        print 'no indexes in lexeme'
    return new_line

