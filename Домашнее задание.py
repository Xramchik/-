import json
# Значения баллов для оценок 2, 3, 4, 5 "от"

ball_3 = 50
ball_4 = 70
ball_5 = 90

# Вспомогательные функции

def read_file(filename):
    out = {}
    try:
        array_string_file = open(filename, 'r+t').readlines()[1:]
        for i in array_string_file:
            i = i.replace('\n','').replace('\r','')
            if len(i) > 0:
                i = i.split(';')
                data_in_string = i[1:]
                if len(data_in_string) > 0:
                    out[i[0]] = []
                    out[i[0]] = data_in_string
                else:
                    out[i[0]] = ['']
    except:
        print("Ошибка, невозможно открыть файл", array_string_file)
    return out

def teacher_groups(data_results):
    out = {}
    for i in data_results:
        i = data_results[i]
        teacher = i[2]
        student = i[1]
        group = data_students[student][2]
        if teacher in out:
            if group not in out[teacher]: out[teacher].append(group)
        else:
            out[teacher] = []
            out[teacher].append(group)
    return out


def ball_students(ball):
    try:
        if int(ball) < int(ball_3):
            out = 2
        elif int(ball) < int(ball_4):
            out = 3
        elif int(ball) < int(ball_5):
            out = 4
        else:
            out = 5
    except:
        print("Ошибка вычисления балла", ball)
    return str(out)

def count_students_balls(id_group):
    out = {}
    for i in data_results.keys():
        i = data_results[i]
        subject = str(data_subjects[i[0]][0])
        result_students = ball_students(int(i[6]))
        #print(id_group, data_students[i[1]][2])
        if str(id_group) == str(data_students[i[1]][2]):
            if subject not in out:
                out[subject] = {}
                out[subject]["5"] = 0
                out[subject]["4"] = 0
                out[subject]["3"] = 0
                out[subject]["2"] = 0
            out[subject][str(result_students)] = int(out[subject][str(result_students)]) + 1
    return out

def in_file(to_json, data):
    if to_json != False:
        out = True
        try:
            open(to_json, 'w').write(str(data))
        except:
            print("Ошибка, не могу записать файл", to_json)
    else:
        out = data
    return out


def students_in_groups(id_group):
    out = []
    for i in data_students.keys():
        if id_group == data_students[i][2]: out.append(i)
    return out

def get_subject_id(subject_name):
    out = ''
    for i in data_subjects.keys():
        if data_subjects[i][0] == subject_name:
            out = i
    return out
    

# Задания

# Написать функцию, которая принимает id преподавателя и id группы.
# Функция возвращает False, если данный преподаватель не преподавал у данной группы,
# None, если такого прподавателя не существует,
# иначе возвращается словарь, в котором ключами являются наименования предметов, а значениями словари, которые хранят в себе информации о количестве студентов, сдавших на 5, 4, 3 и 2 по данному предмету.


def ret_data_teacher(id_teacher, id_group):
    if id_teacher in data_teachers:
        if id_group in teacher_to_groups[id_teacher]:
            out = count_students_balls(id_group)
        else:
            out = False
    else:
        out = None
    return out


# Написать функцию, которая принимает ФИО преподавателя и необязательный параметр to_json, который по умолчанию равен False и принимает имя файла.
# Если указан параметр to_json, то он должен сохранить итоговый результат в данный файл и вернуть значение True,
# иначе просто вернуть словарь. В словаре ключами являются наименования групп, в которых он преподавал, а значениям - результат выполнения первой функции.


def ret_json_teacher(fio_teacher, to_json=False):
    try:
        out = {}
        (last_name, first_name, middle_name) = fio_teacher.split(' ')
        id_teacher = ''
        for i in data_teachers.keys():
            if last_name == data_teachers[i][0] and first_name == data_teachers[i][1] and middle_name == data_teachers[i][2]:
                id_teacher = str(i)
                break
        if id_teacher == '':
            print("Ошибка, учитель не найден")
        else:
            for id_group in teacher_to_groups[id_teacher]:
                if id_group not in out:
                    out[id_group] = {}
                out[id_group] = ret_data_teacher(id_teacher, id_group)
        out = in_file(to_json, out)
    except:
        out = ''
        print("Ошибка, ФИО учителя не соответствует шаблону", fio_teacher)
    return out


# Реализовать функцию, которая принимает параметры entry_year - год поступления, subject_name - наименование предмета и необязаиельный параметр to_json, по умолчанию равный False.
# Функция должна возвращать словарь со статистикой по группам по данному предмету.
# Ключами словаря являются id группы, а значениями словари. Внутренний словарь имеет ключи group_name (наименование группы), stats (статистика).
# Значением ключа статистика является словарь, который возвращает количество студентов получившие оценку 5, количество студентов получившие оценку 4, количество студентов получившие оценку 3,
# количество студентов получившие оценку 2.
# Если параметр to_json указан, то сохраняет полученный словарь в указанный файл и возвращает True, иначе просто возвращает словарь.        


def group_stat(entry_year, subject_name, to_json=False):
    out = {}
    array_groups = []
    for i in data_groups.keys():
        arr_groups = data_groups[i]
        year = arr_groups[1]
        name = arr_groups[0]
        if year == entry_year:
            array_groups.append(i)
    for i in array_groups:
        out[i] = {}
        out[i]['group_name'] = data_groups[i][0]
        out[i]['stats'] = count_students_balls(i)[subject_name]
    out = in_file(to_json, out)
    return out


# Реализовать функцию, которая по уникальному идентификатору студента возвращает его сумму баллов по каждому из контрольных мероприятий, в том числе total
def summ_ball_student(id_student, test='all'):
    out = {'att1':0, 'att2':0, 'exam':0, 'total':0}
    for i in data_results.keys():
        i = data_results[i]
        if str(i[1]) == str(id_student):
            out['att1'] = out['att1'] + int(i[3])
            out['att2'] = out['att2'] + int(i[4])
            out['exam'] = out['exam'] + int(i[5])
            out['total'] = out['total'] + int(i[6])
    if test == 'att1':
        out = out['att1']
    elif test == 'att2':
        out = out['att2']
    elif test == 'exam':
        out = out['exam']
    elif test == 'total':
        out = out['total']
    return out


# Реализовать функцию, которая принимает параметры thread - поток в виде (ПИ2018), где буквами является наименование направления, а число - год поступления,
# необязательный параметр test, который по умолчанию равен total (список возможных значений att1, att2, exam, total), а также необязательный параметр to_json=False.
# Если параметр указан, то результат выполнения функции должен записываться в файл и функция возвращает True, если такого потока не существует, то возвращает None, иначе возвращает результат функции.
# Результатом выполнения функции является словарь с рейтингом студентов по указанному из периодов в параметре test. Ключом словаря является место студента в рейтинге, значением - словарь с информацией из файла students.csv,
# а также информацию, которая возвращается после выполнения первой функции.
def rating_students(thread, test='total', to_json=False):
    out = 'None'
    for i in data_groups.keys():
        tmp_thread = str(data_groups[i][0] + data_groups[i][1])
        if tmp_thread == thread:
            out = {}
            if test in ['att1', 'att2', 'exam', 'total']:
                id_group = i
                array_students = students_in_groups(id_group)
                tmp_rait = []
                for id_student in array_students:
                    in_array = [summ_ball_student(id_student, test), id_student]
                    tmp_rait.append(in_array)
                tmp_rait.sort(reverse=True)
                position_in_rait = 1
                for rait in tmp_rait:
                    id_student = rait[1]
                    out[str(position_in_rait)] = {'id': id_student, 'last_name':data_students[id_student][0], 'first_name':data_students[id_student][1], 'group_id':data_students[id_student][2]}
                    position_in_rait = int(position_in_rait) + 1
            else:
                print("Ошибка, параметр test не находится в списке допустимых значений")
            break
    out = in_file(to_json, out)
    return out
        

# Написать функцию, которая принимает имя группы, год поступления и наименование предмета.
# Также функция принимает необязательный параметр to_json, который по умолчанию равен False и принимает имя файла.
# Функция должна вернуть словарь, которая содержит оценки всех студентов данной группы по данному предмету.
# Ключом является id студента, значением словарь, который содержит полное имя студента и итоговый балл.
# Если to_json указывает имя файла, то сохранить результаты в файл и функция возвращает значение True, иначе возвращает получившийся словарь.

def stat_group_subject(group_name, year, subject_name, to_json=False):
    out = {}
    for i in data_groups.keys():
        if str(data_groups[i][0]) == str(group_name) and str(data_groups[i][1]) == str(year):    
            arr_students = students_in_groups(i)
            id_subject = get_subject_id(subject_name)
            for result in data_results.values():
                if result[0] == id_subject and result[1] in arr_students:
                    id_student = result[1]
                    out[str(id_student)] = {'name': str(data_students[id_student][0] + ' ' + data_students[id_student][1]), 'total':result[6]}
                
            break
    out = in_file(to_json, out)
    return out





data_students = read_file("students.csv")
data_results = read_file("results.csv")
data_groups = read_file("groups.csv")
data_teachers = read_file("teachers.csv")
data_subjects = read_file("subjects.csv")
teacher_to_groups = teacher_groups(data_results)





# Проверки

#print(ret_data_teacher('22222222222222', '23'))
#print(ret_data_teacher('1', '8'))
#print(ret_data_teacher('1', '6'))
#print(ret_json_teacher("Милованов Даниил Михайлович", to_json=False))
#print(ret_json_teacher("Милованов Даниил Михайлович", to_json='milovanov.json'))
#print(group_stat('2017', 'Web-программирование', to_json=False))
#print(group_stat('2017', 'Web-программирование', to_json='2017-web.json'))
#print(summ_ball_student('180101'))
#print(rating_students('ПИ2-22017', test='total', to_json=False))
#print(stat_group_subject('ПИ2-2', '2017', 'Web-программирование', to_json=False))
