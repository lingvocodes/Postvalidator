import re, codecs

from basic import *
from collect_marks import *
from preparator import *
from intro import *
from synopsis import *
def array_search(var, array):
    for i in array:
        if re.search(var, i) != None:
            return array.index(i)
    

def entry_many(array, lexeme):
    arr = []
    arr2 = []
    counter = 0
    while counter < len(array):
        if re.search(u'<b>', array[counter]) != None:
            if arr2 != []:
                arr.append(arr2)
            arr2 = []
            arr2.append(array[counter])
        else:
            arr2.append(array[counter])
        counter += 1
        if arr2 != []:
            arr.append(arr2)

    arr3 = []
    for i in arr:
        if i not in arr3:
            arr3.append(i)
                    
    return arr3

def entry_only(array, lexeme):
    arr = array[1:]
    arr_outer = [arr]
    return arr_outer


def head_edition(line):
    line = line.strip()
    m = re.search(u'(.*)</b>(.+)', line)
    if m != None:
        if m.group(2) != u'':
            if line[-1] != u'.':
                line += mistake(u'.', u'Проверьте, стоит ли здесь точка')
            
        else:
            if line[-1] == u'.':
                line += mistake(u'', u'Проверьте, стоит ли здесь точка')

    return line

def example_edition(line):

    return line

def meaning_edition(line):
    m = re.search(u'ЗНАЧЕНИЕ\. ?<i> ?(.)', line)
    if m != None:
        if m.group(1).lower() == m.group(1):
            line = re.sub(m.group(1), mistake(u'', u'Толкование должно начинаться с большой буквы') + m.group(1), line)
    return line

def illustrations_edition(line):
    
    def three_dots(line):
        
        new_line = re.sub(u'\[...\]', mistake(u'[...]', u'[…] Многоточие должно быть одним символом'), line)
        new_line_2 = re.sub(u'&lt;', mistake(u'[', u'При пропуске в цитате должны стоять квдратные скобки'), new_line)
        new_line_3 = re.sub(u'%gt;', mistake(u']', u'При пропуске в цитате должны стоять квдратные скобки'), new_line_2)


        return new_line_3

    def initials_c(line):
        initials_arr = re.findall(u'(\([А-Я]\.(&nbsp;| )[А-Я][а-я]+\))', line)
        if initials_arr != []:
            for i in initials_arr:
                if i[1] == u' ':
                    line = re.sub(i[0], mistake(i[0], u'Между инициалами должен быть неразрывный пробел'), line)
        return line

    def initials_a(line):
        initials_arr = re.findall(u'(\([А-Я]\.(&nbsp;| )[А-Я]\.(&nbsp;| )[А-Я][а-я]+\))', line)
        if initials_arr != []:
            for i in initials_arr:
                if i[2] == u' ' and i[1] == None:
                    line = re.sub(i[0], mistake(i[0], u'Между инициалами отчества и фамилии должен быть неразрывный пробел'), line)
                elif i[1] != None and i[2] == u' ':
                    line = re.sub(i[0], mistake(i[0], u'Между инициалами имени и отчества не должно быть пробела; кроме того, между отчеством и фамилией должен быть неразрывный пробел'), line)
                elif i[1] != None and i[2] == u'&nbsp;':
                    line = re.sub(i[0], mistake(i[0], u'Между инициалами имени и отчества не должно быть пробела'), line)
        return line
    line = three_dots(line)
    line = initials_c(line)
    line = initials_a(line)

    return line

def semantics_edition(line):
    return line

def entry_edition(array, semantic_collocations, amount):
    
    def comments(array):
        
        def search_keyword(kw_array, line):
            counter = 0
            for i in kw_array:
                m = re.search(i, line)
                if m != None:
                    counter += 1
            return counter
            
        entries = [u'ПРИМЕРЫ',
                   u'ЗНАЧЕНИЕ',
                   u'УПРАВЛЕНИЕ',
                   u'СОЧЕТАЕМОСТЬ',
                   u'ИЛЛЮСТРАЦИИ']
        comments = []
        counter = 0
        for num in range(0, len(array) - 1):
            if re.search(u'КОММЕНТАРИИ', array[num]) != None:
                comments.append([array[num], num])
                counter += 1
                if num + counter < len(array) - 1:
                    while search_keyword(entries, array[num + counter]) == 0:
                        comments.append([array[num + counter], num + counter])
                        counter += 1

        return comments
                
                            
    head = u''
    examples = u''
    meaning = u''
    government = u''
    compatibility = u''
    illustrations = u''
    semantics = u''
    for i in array:
        if re.search(u'<b>', i) != None:
            head = frnt_space_remover(i)
            head = rear_space_remover(head)
        if re.search(u'ПРИМЕРЫ', i) != None:
            examples = frnt_space_remover(i)
            examples = rear_space_remover(examples)
        if re.search(u'ЗНАЧЕНИЕ', i) != None:
            meaning = frnt_space_remover(i)
            meaning = rear_space_remover(meaning)
        if re.search(u'УПРАВЛЕНИЕ', i) != None:
            government = frnt_space_remover(i)
            government = rear_space_remover(government)
        if re.search(u'%', i) != None:
            government += rear_space_remover(frnt_space_remover(i))
        if re.search(u'СОЧЕТАЕМОСТЬ', i) != None:
            compatibility = frnt_space_remover(i)
            compatibility = rear_space_remover(compatibility)
        if re.search(u'ИЛЛЮСТРАЦИИ', i) != None:
            illustrations = frnt_space_remover(i)
            illustrations = rear_space_remover(illustrations)
        for mark in semantic_collocations:
            m = re.search(mark, i)
            if m != None:
                semantics = i
                break

    if amount == 'many':
        print 'returned with head'
        to_return = [head_edition(head), example_edition(examples), meaning_edition(meaning), government, compatibility, illustrations_edition(illustrations), semantics_edition(semantics)]
        for arr in comments(array):
            to_return.insert(arr[1], arr[0])
        return to_return
        
    elif amount == 'only':
        print 'returned without heads'
        to_return = [example_edition(examples), meaning_edition(meaning), government, compatibility, illustrations_edition(illustrations), semantics_edition(semantics)]
        for arr in comments(array):
            to_return.insert(arr[1], arr[0])
        return to_return
