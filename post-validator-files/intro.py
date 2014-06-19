import re, codecs
from basic import *
from collect_marks import *

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

def intro_long(line, parts_of_speech, grammar_underlined, grammar_forms, verb_perf, syntactic_marks):

    line = line.strip()
    print u'line: i' + line + u'i'
    if line[-1] == u'.':
        new_line = u''
        dot = 1
        print 'dot exists'
        for i in range(len(line) - 1):
            new_line += line[i]
        line = new_line
    else:
        dot = 0
        print 'dot does not exist'

    def zone1(line):

        zone1 = []
      
        m = re.search(u'(<b>.+</b>)([,;]) ?([^,;]+)([,;])(.*)', line)
        if m != None:
            zone1.append(m.group(1))
            zone1.append(m.group(2))
            zone1.append(m.group(3))
            zone1.append(m.group(4))

        else:
            print u'm = none'

        if zone1 != []:
            returned = []
            returned.append(zone1)
            returned.append(m.group(5))
            for i in zone1:
                print i
            return returned
        else:
            return 'zone 1 not found'

    def check_zone1(array):
        if array[1] != u',':
            array[1] = mistake(array[1], u'Возможна ошибка в знаке препинания; здесь должна быть запятая')
        if array[2] not in parts_of_speech:
            array[2] = mistake(array[2], u'Возможно, ошибка в помете')
        if array[3] != u';':
            array[3] = mistake(array[3], u'Возможна ошибка в знаке препинания; здесь должна быть точка с запятой')
        return array
    
    print 'zone 1 checked:'
    zone_1_checked_line = collecting_checked_array(check_zone1(zone1(line)[0]))
    print zone_1_checked_line

    print '\n'

    line = zone1(line)[1]    

    def zone2(line):
        


        zone_2 = u' '.join(tok(line, u','))
        zone_2 = tok(zone_2, u';')

        arr_zone_2 = []
        arr_zone_3 = []
        for i in zone_2:
            if i not in verb_perf:
                arr_zone_2.append(i)
            else:
                arr_zone_3 = zone_2[zone_2.index(i):]
                break

        
        returned = []
        returned.append(arr_zone_2)
        returned.append(arr_zone_3)
        return returned

    def check_zone_11(array):

        arr2 = []

        for i in array:
            m = re.search(u'[А-Я]+', i)
            if m != None:
                if i not in syntactic_marks:
                    arr2.append(mistake(i, u'Возможно, ошибка в помете'))
                else:
                    arr2.append(i)
            else:
                arr2.append(i)

        if arr2[-1] != u';':
            arr2[-1] = mistake(arr2[-1], u'Возможно, здесь должна быть точка с запятой')

        return arr2

    zone11 = []

    zone2_unchecked = zone2(line)[0]
    zone2_unchecked = delete_empty_elements(zone2_unchecked)
        
    if zone2_unchecked[0] in syntactic_marks:
        counter = 0
        while counter <= len(zone2_unchecked):
            if zone2_unchecked[counter] == u',' or zone2_unchecked[counter] == u';' or zone2_unchecked[counter] in syntactic_marks:
                counter += 1
            else:
                break
        zone11 = zone2_unchecked[:counter]
        zone2_unchecked = zone2_unchecked[counter:]
    else:
        zone2_unchecked = zone2_unchecked

    if zone11 != []:

        zone11_checked = check_zone_11(zone11)
        zone11_existing = 1
    else:
        zone11_existing = 0

               
    def check_zone_2(array):
        
        for i in array:
            m = re.search(u'[А-Я]+', i)
            if m != None:
                if i not in grammar_forms:
                    array = replace_in_array(i, mistake(i, u'Возможно, ошибка в помете'), array)

        for i in array:
            m = re.search(u';', i)
            if m != None:
                if array.index(i) != len(array) - 1:
                    array = replace_in_array(i, mistake(i, u'Возможно, здесь должна быть запятая'), array)

        if array[-1] == u',':
            array[-1] = mistake(array[-1], u'Возможно, здесь должна быть точка с запятой')

        for i in array:
            m = re.search(u'<u>([^<]+)</u>(\.)?', i)
            if m != None:
                s = re.search(u'\.', m.group(1))
                if s == None and m.group(2) == u'.':
                    array = replace_in_array(i, mistake(i, u'Проверьте, входит ли точка в подчёркивание'), array)

        return array

    print 'zone 2 checked: '
    zone_2_checked_line = collecting_checked_array(check_zone_2(zone2_unchecked))
    print zone_2_checked_line
    for i in check_zone_2(zone2(line)[0]):
        print i

    print u'\n'

    if len(zone2(line)[1]) > 0:
        zone_3_existing = 1
        line = u' '.join(zone2(line)[1])
    else:
        zone_3_existing = 0
  

    def zone34(line):
        zone3 = []
        zone4 = []
        raw = line.split(u' ')
        if raw[0] in verb_perf:
            zone3.append(raw[0])
        if len(raw) == 1:
            returned = []
            returned.append(zone3)
            returned.append(zone4)
            return returned
        else:
            if raw[1] in [u',', u';']:
                zone3.append(raw[1])
                zone4 = raw[2:]
            else:
                zone4 = []
            returned = []
            returned.append(zone3)
            returned.append(zone4)
            return returned

        
        
    def check_zone_3(array):
        
        if array[0] not in verb_perf:
            array = replace_in_array(i, mistake(i, u'Возможно, ошибка в помете'), array)

        if array[-1] == u',':
            array[-1] = mistake(array[-1], u'Здесь должна быть точка с запятой')
        
        return array

    if zone_3_existing == 1:
        zone_3_checked_line = collecting_checked_array(check_zone_3(zone34(line)[0]))

    
    if len(zone34(line)[1]) > 0:
        zone_4_existing = 1
    else:
        zone_4_existing = 0

    print u'\n'

    def check_zone_4(array):
        if u'кроме' in array:
            zone41 = array[:array.index(u'кроме')]
            zone42 = array[array.index(u'кроме'):]
            zone42_existing = 1
        else:
            zone41 = array
            zone42_existing = 0

        if zone41[0] not in verb_perf:
            zone41[0] = mistake(zone41[0], u'Возможно, ошибка в помете')

        m = re.search(u'<u>([^<]+)</u>(\.)?', zone41[1])
        if m != None:
            s = re.search(u'\.', m.group(1))
            if s == None and m.group(2) == u'.':
                zone41[1] = mistake(zone41[1], u'Проверьте, входит ли точка в подчёркивание')


        if zone42_existing == 1:
            numbers = []
            for i in zone42:
                m = re.search(u'[0-9]+\.?[0-9]+?', i)
                if m != None:
                    numbers.append(i)

                            
            

            for element in zone42:
                zone41.append(element)

            array = zone41
            
        return array

    if zone_4_existing == 1:
        zone_4_checked_line = collecting_checked_array(check_zone_4(zone34(line)[1]))


    intro_edited = zone_1_checked_line

    if zone11_existing == 1:
        intro_edited += collecting_checked_array(zone11_checked)

    intro_edited += zone_2_checked_line

    if zone_3_existing == 1:
        intro_edited += zone_3_checked_line
    if zone_4_existing == 1:
        intro_edited += zone_4_checked_line

    if dot == 1:
        return intro_edited + u'.'
    else:
        return intro_edited + mistake(u'.', u'Проверьте, стоит ли точка в конце строки')

def intro_short(line, parts_of_speech, grammar_underlined, grammar_forms, verb_perf, syntactic_marks):
    if line[-1] == u'.':
        new_line = u''
        dot = 1
        print 'dot exists'
        for i in range(len(line) - 1):
            new_line += line[i]
        line = new_line
    else:
        dot = 0
        print 'dot does not exist'

    def zone1(line):

        zone1 = []

        m = re.search(u'(<b>[^<]+</b>)([,;]) ?([^,;]+)', line)
        if m != None:
            zone1.append(m.group(1))
            zone1.append(m.group(2))
            zone1.append(m.group(3))

        

        else:
            print u'm = none'

        
        for i in zone1:
            print i

        if zone1 != []:
            return [zone1]
        else:
            return 'zone 1 not found'

    def check_zone1(array):
        if array[1] != u',':
            array[1] = mistake(array[1], u'Возможно, ошибка в знаке препинания, здесь должна быть запятая')
        if array[2] not in parts_of_speech:
            array[2] = mistake(array[2], u'Возможно, ошибка в помете')
        return array
    

    print 'zone 1 checked:'
    zone_1_checked_line = collecting_checked_array(check_zone1(zone1(line)[0]))
    print zone_1_checked_line

    print '\n'

    intro_edited = zone_1_checked_line
    if dot == 1:
        return intro_edited + u'.'
    else:
        return intro_edited + mistake(u'.', u'Проверьте, стоит ли точка в конце строки')
