import re, codecs
import os

from basic import *
from preparator import *
from intro import *
from synopsis import *
from entries import *
from collect_marks import *


print u'Если программа падает - не стреляйте в программиста!'
print u'Возможно, это происходит из-за неправильно отформатированного текста'
chapters = 'TRUE'

article_name = raw_input(u'Введите имя статьи: ')
article = u'articles/' + article_name + u'.html'

## СБОР ПОМЕТ ====================

grammar_forms = marks_list('marks/grammar_forms.txt')
grammar_underlined = marks_list('marks/grammar_underlined.txt')
other_underlined = marks_list('marks/other_underlined.txt')
parts_of_speech = marks_list('marks/parts_of_speech.txt')
special_marks = marks_list('marks/special_marks.txt')
style_marks = marks_list('marks/style_marks.txt')
syntactic_constructions = marks_list('marks/syntactic_constructions.txt')
syntactic_marks = marks_list('marks/syntactic_marks.txt')
verb_perf = marks_list('marks/verb_perf.txt')
semantic_collocations = marks_list('marks/semantic_collocations.txt')


## ПОДГОТОВКА HTML ================

src_prepared = codecs.open('source_prepared.html', 'w', 'utf-8')
source_edition = preparator(article)
print str(len(source_edition)) + ' lines in source'
for i in source_edition:
    src_prepared.write(i)

print 'temp file created...'

src_prepared.close()

## =========================

f = codecs.open('source_prepared.html', 'r', 'utf-8').read()
f = double_space_remover(f)
print u'double spaces removed'
f_result = codecs.open(u'results/' + article_name + '_result.html', 'w', 'cp1251')

text_lines = f.split(u'</p>')
print u'SYNOPSIS'
for line in text_lines:
    m = re.search(u'<p><b>(.+[^<])</b>, [А-Я]+[;.]?', line)
    if m != None:
        print "intro found"
        v_intro = line
        lexeme = m.group(1).lower()
        lexeme = re.sub(u'\^', u'', lexeme)
        lexeme = remove_empty_tags(lexeme)
        lexeme = remove_repeating_tags_nospace(lexeme)
        lexeme = remove_index(lexeme)
        print 'lexeme: ' + lexeme
        intro_warning = 0
        break
    else:
        print 'intro: m = None'
        v_intro = text_lines[0]
        print 'INTRO WARNING'
        intro_warning = 1
        m = re.search(u'<b>([^<>]+)</b>', v_intro)
        if m != None:
            lexeme = m.group(1).lower()
            lexeme = re.sub(u'\^', u'', lexeme)
            lexeme = remove_empty_tags(lexeme)
            lexeme = remove_repeating_tags_nospace(lexeme)
            lexeme = remove_index(lexeme)
            print u'lexeme: ' + lexeme
        else:
            print "something is really wrong"
        break
print v_intro
print intro_warning
v_synopsis = []
v_headings = []
for line in text_lines:
    m = re.search(u"(<p>(<b>[^А-Я]+ ?</b>(.*)))", line)
    if m != None:
        if u':' in m.group(1):
            v_synopsis.append(line)
        else:
            v_headings.append(line)


print u'ENTRIES'
if len(v_headings) > 0:
    v_entries = text_lines[text_lines.index(v_headings[0]):]
else:
    v_entries = text_lines

print u'HEADINGS'
v_headings_2 = []
for i in v_headings:
    s = re.sub(u'<p>', u'', i, flags = re.U)
    v_headings_2.append(s)
v_headings = v_headings_2
v_headings_2 = []

if len(v_headings) != 0:
    for i in v_headings:
        i = i.strip()
        v_headings_2.append(i)
    v_headings = v_headings_2
else:
    print u'if there are headings in this article, something is wrong with them'


print 'intro processing...'
regexp = re.compile(u'<i>')
m = re.search(regexp, v_intro)
if intro_warning == 0:
    if m != None:
        print 'long intro is processed'
        intro_edited = intro_long(v_intro, parts_of_speech, grammar_underlined, grammar_forms, verb_perf, syntactic_marks)
    else:
        print 'short intro is processed'
        intro_edited = intro_short(v_intro, parts_of_speech, grammar_underlined, grammar_forms, verb_perf, syntactic_marks)
else:
    intro_edited = u'<font color="red">Ошибка в тегах или в структуре входа; вход не проверен. Проверьте структуру входа.</font> ' + v_intro
    
print 'synopsis processing...'
synopsis_edited = synopsis(v_synopsis, lexeme, v_headings)
if synopsis_edited == []:
    print 'no synopsis found'
    synopsis_existing = 0
    if len(v_headings) > 0:
        print 'headings found'
        headings_existing = 1
        entries_amount = 'many'
    else:
        print 'headings not found'
        headings_existing = 0
        entries_amount = 'only'
else:
    print 'synopsis found'
    synopsis_existing = 1
    headings_existing = 1
    entries_amount = 'many'
    
print 'entries processing...'
if headings_existing == 1:
    entries_edited = entry_many(v_entries, lexeme)
else:
    entries_edited = entry_only(v_entries, lexeme)

entries_edited_2 = []
for i in entries_edited:
    s = entry_edition(i, semantic_collocations, entries_amount)
    entries_edited_2.append(s)
entries_edited = entries_edited_2


f_result_array = []
f_result_array.append(intro_edited + u'</i>')
for i in synopsis_edited:
    f_result_array.append(i)
for i in entries_edited:
    for s in i:
        f_result_array.append(s)

f_result_array_2 = []
for i in f_result_array:
    s = odd_space_marker(i)
    f_result_array_2.append(s)

f_result_array = f_result_array_2


for i in f_result_array:
    if i != u'':
        f_result.write(i + u'</p>\n')
        
f_result.close()

##os.remove('source_prepared.html')
os.remove('basic.pyc')
os.remove('collect_marks.pyc')
os.remove('entries.pyc')
os.remove('intro.pyc')
os.remove('preparator.pyc')
os.remove('synopsis.pyc')
print 'temp files deleted...'

