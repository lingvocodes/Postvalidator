import re, codecs
from basic import *

def synopsis(arr, lexeme, headings):

    def initials(line):
        initials_arr = re.findall(u'(\([А-Я]\.[А-Я]?\.?(&nbsp;| )[А-Я][а-я]+\))', line)
        if initials_arr != []:
            for i in initials_arr:
                if i[1] == u' ':
                    line = re.sub(i[0], mistake(i[0], u'Между инициалами должен быть неразрывный пробел'), line)

        return line
    
    spec_quot = [u'‘', u'’']
    lines_edited = []

    def synopsis_prepare(arr, lexeme):

        print 'synopsis preparing...'
        
        for i in arr:
            m = re.search(u'\. ?<b>' + lexeme, i)
            if m != None:
                position = arr.index(i)
                arr.pop(position)
                items = i.split(u'. <b>')
                for s in range(1, len(items)):
                    items[s] = u'<b>' + items[s]
                for item in items:
                    s = re.search(u'<p>', item)
                    if s != None:
                        arr.insert(position, item)
                    else:
                        arr.insert(position, u'<p>' + item)
                    position += 1
        print 'all synopsis elements splitted correctly'

        arr2 = []    
        marker_to_search = re.compile(u'(<b>' + lexeme +u'[0-9][0-9]?\.?[0-9]? ?</b>)')
        for i in arr:
            m = re.search(marker_to_search, i)
            if m != None:
                marker = re.sub(u' </b>', u'</b> ', m.group(1))
                i = re.sub(m.group(1), marker, i)
                arr2.append(i)
            else:
                s = re.sub(u' </b>', u'</b> ', i)
                arr2.append(s)
        arr = arr2
        print 'tags moved'

        arr2 = []
        marker_to_search = re.compile(u'((<b>' + lexeme + u')([0-9]?[0-9]\.?[0-9]?</b>))')
        for i in arr:
            m = re.search(marker_to_search, i)
            if m != None:
                s = re.sub(m.group(1), m.group(2) + u' ' + m.group(3), i)
                arr2.append(s)
            else:
                arr2.append(i)
        arr = arr2
        print 'spaces between lexeme and number inserted'

        arr2 = []
        for i in arr:
            corteages = []
            problem_fragms = re.findall(u'</i>[^<]*<i>', i)
            if len(problem_fragms) == 0:
                arr2.append(i)
            else:
                for fragm in problem_fragms:
                    m = re.search(u'(</i>([^<])*<i>)', fragm)
                    if m != None:
                        cor = (m.group(1), m.group(2))
                        corteages.append(cor)
                for cor in corteages:
                    i = re.sub(cor[0], cor[1], i)
                arr2.append(i)
        arr = arr2
        print '(service) repeating tags removed'
            
        for i in arr:
            lines_edited.append(i)

        print '---'
    
        return lines_edited

    arr = synopsis_prepare(arr, lexeme)

    print u'\n\n\nSYN'
    for i in arr:
        print i
    print u'\n\n\nHDS'
    for i in headings:
        print i
    print u'\n\n\n'

    def zone_in_synopsis(line):
        arr = []
        m = re.search(u'(<b>[^<]+</b>)(.+)?:(.*)', line)
        if m != None:
            zone1 = m.group(1)
            zone2 = m.group(2)
            zone3 = m.group(3)
        else:
            print 'm = none (symopsis ln131)'
            
        arr.append(zone1)
        arr.append(zone2)
        arr.append(zone3)
        return arr

    def check_zone1(line):
        zone = zone_in_synopsis(line)[0]
        return zone

    def check_zone2(line):
        zone = zone_in_synopsis(line)[1]
        if u'[' in zone:
            if u']' not in zone:
                m = re.search(u'([^\[]*)(\[.*)', zone)
                if m != None:
                    zone = m.group(1) + mistake(m.group(2), u'Не закрыта скобка')
            else:
                if zone[0] != u':':
                    zone = mistake(u':', u'Здесь должно быть многоточие') + zone
                    
        regexp_spec_quot = re.compile(u' (.)([а-я- \.]+)(.)')
        new_zone = u''
        m = re.search(regexp_spec_quot, zone)
        print m.group(1) + u' ' +  m.group(2) + u' '  + m.group(3)
        if m.group(1) != spec_quot[0]:
            new_zone += mistake(m.group(1), u'Кавычка неправильная или отсутствует')
        else:
            new_zone += m.group(1)
        new_zone += m.group(2)
        if m.group(3) != spec_quot[1]:
            new_zone += mistake(m.group(3), u'Кавычка неправильная или отсутствует')
        else:
            new_zone += m.group(3)
        print zone
        zone = new_zone
        return zone

    def check_zone3(line):
        zone = zone_in_synopsis(line)[2]
        zone = initials(zone)
        return zone
        
        
    arr2 = []
    for entry in arr:
        entry_edited = u'<p>'
        one = check_zone1(entry)
        print 'zone1: ' + one
        entry_edited += one
        entry_edited += u' '
        two = check_zone2(entry)
        print 'zone2: ' + two
        entry_edited += two
        entry_edited += u' '
        three = check_zone3(entry)
        print 'zone3: ' + three
        entry_edited += three
        arr2.append(entry_edited)
        print entry_edited
    arr = arr2
    print len(arr)

    if arr == []:
        print 'for some reason, this array is empty (ln 174)'
        print "it's not that bad though, if synopsis is empty, we're fine"
    else:
        print u'not empty, hurray'
        for i in arr:
            print i

    def synopsis_headings_comparison(arr_syn, arr_hds, lexeme):

        arr_temp = []
        for i in arr_hds:
            i = frnt_space_remover(i)
            i = rear_space_remover(i)
            arr_temp.append(i)
        arr_hds = arr_temp

        array = []
        check = 0
        if len(arr_syn) == len(arr_hds):
            check = 1
        else:
            print len(arr_syn)
            print len(arr_hds)
            print element_by_element_comparison(arr_syn, arr_hds)
            check = 0
        
        if check == 1:
            regexp = re.compile(u'(<p>((<b> ?' + lexeme + u') ?([0-9]?[0-9]\.?[0-9]? ?</b>)))')
            for i in range(len(arr_syn)):
                m = re.search(regexp, arr_syn[i])
                if m != None:
                    arr_hds[i] = frnt_space_remover(arr_hds[i])
                    arr_hds[i] = rear_space_remover(arr_hds[i])
                    print m.group(2)
                    print arr_hds[i]
                    if m.group(2) == arr_hds[i]:
                        print 'equal'
                        print u'---'
                        array.append(arr_syn[i])
                        continue
                    else:
                        print u'---'
                        if m.group(2) != arr_hds[i]:
                            array.append(re.sub(m.group(2), mistake(arr_hds[i], u'При лексеме стоят дополнительные пометы'), arr_syn[i]))

        return array

    print u'here nust be comparison...'
    if len(arr) > 0 and len(headings) > 0 and len(lexeme) > 0:
        print 'yall good!'
        print len(arr)
        print len(headings)
        print lexeme
        arr = synopsis_headings_comparison(arr, headings, lexeme)
    else:
        print 'if there are both synopsis and headings, something might went wrong'
        print len(arr)
        print len(headings)
        print len(lexeme)
    return arr

