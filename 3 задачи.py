import json


# Значения баллов 2, 3, 4, 5

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
            print("Ошибка, не могу записать файд", to_json)
    else:
        out = data
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


def group_stat(entry_year, subject_name, to_json):
    


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
