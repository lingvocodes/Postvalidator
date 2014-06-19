import re, codecs

def mistake(fragm, mistake_type):
    return '<font color="red"> !' + mistake_type + '! </font> <font color="green"><u>' + fragm + '</u></font>'

def mark_check(mark, mark_list):
    if mark in mark_list:
        return 'correct'
    else:
        return 'incorrect'

def string_to_arr(string):
    arr = []
    for i in string:
        arr.append(i)
    return arr

def tok(line, p):

    arr = line.split(u' ')
    for i in arr:
        regexp = re.compile(u'([^' + p + ']+)('+ p +')')
        m = re.search(regexp, i)
        if m != None:
            word_w_punct = i
            n = arr.index(i)
            arr.pop(n)
            arr.insert(n, m.group(1))
            arr.insert(n + 1, m.group(2))
    return arr

def collecting_checked_array(array):
    checked_line = u''
    punct = [u',', u';']
    for i in array:
        if i in punct:
            checked_line += i
        else:
            checked_line = checked_line + u' ' + i
    return checked_line

def replace_in_array(obj, repl, array):
    j = array.index(obj)
    array.pop(j)
    array.insert(j, repl)
    return array

def delete_empty_elements(array):
    for i in array:
        if i == u'':
            array.pop(array.index(i))
    return array

def element_by_element_comparison(arr1, arr2):
    if len(arr1) > len(arr2):
        while len(arr2) != len(arr1):
            arr2.append(u'None')
    elif len(arr2) > len(arr1):
        while len(arr1) != len(arr2):
            arr1.append(u'None')
    for i in range(len(arr1)):
        print i
        print arr1[i]
        print arr2[i]
        print u'\n'
    return ''

def frnt_space_remover(line):
    while line[0] == u' ':
        line = line[1:]
    return line

def rear_space_remover(line):
    while line[-1] == u' ':
        line = line[:-1]
    return line

def frame(line, length, step):
    arr = []
    start = 0
    finish = length
    while finish <= len(line):
        arr.append(line[start:finish])
        start += step
        finish += step
    return arr

def odd_space_marker(line):
    m = re.findall(u'([^ ])([ ]{2,})([^ ])', line)
    if m != []:
        print u'odd spaces found...'
        for i in m:
##            print i
            line = re.sub(i[0] + i[1] + i[2], i[0]+u'<font color="red">_</font>'+i[2], line)
        return line + u' <font color="red">Красным подчеркиванием помечены места, где в тексте стоят двойные пробелы</font>'        
    else:
        return line

def dot_underlined(line):
    m = re.findall(u'(<u>([^<]+)</u>(\.)?)', line)
    if m != []:
        for i in m:
            s = re.search(u'\.', i[1])
            if s == None and i[2] == u'.':
                line = re.sub(m.group(1), mistake(m.group(1), u'Проверьте, входит ли точка в подчеркивание'))
    return line
