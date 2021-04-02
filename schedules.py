import json
import time
import requests
from bs4 import BeautifulSoup

# če maš vč razredu naenktat v učilnc se ti sesuje get_schedule_grade() ker mas 'razded, razded' namest sam 'razred'

classrooms = {}
grades = {}
days = {'0': 'Mon', '1': 'Tue', '2': 'Wed', '3': 'Thu', '4': 'Fri'}  # , '5': 'Sat', '6': 'Sun'}
classroom_schedule = []
grade_schedule = []
hours_schedule = []


class Day:
    def __init__(self, name):
        self.name = name
        self.hours = []


class HourClassroom:
    def __init__(self, hour, year, month, day, grade='vacant', professor='/'):
        self.grade = grade
        self.professor = professor
        self.hour = hour
        self.year = year
        self.month = month
        self.day = day


class HourGrade:
    def __init__(self, hour, year, month, day, subject='vacant', professor='/', classroom='/'):
        self.subject = subject
        self.professor = professor
        self.classroom = classroom
        self.hour = hour
        self.year = year
        self.month = month
        self.day = day


def init():
    global school, obj
    classrooms = {}
    grades = {}
    classroom_schedule = []
    grade_schedule = []
    hours_schedule = []
    # read file
    with open('info.json', 'r') as my_file:
        data = my_file.read()
    # parse file
    obj = json.loads(data)
    school = str(obj['school_id'])
    for day_name in days:
        classroom_schedule.append(Day(name=days[day_name]))
    for day_name in days:
        grade_schedule.append(Day(name=days[day_name]))


def get_now_hour():
    date_time = time.asctime()
    # split hh:mm:ss into array [hh, mm, ss]
    now_time = date_time.split()[3].split(':')
    # calculate how many minutes passed today
    minutes = int(now_time[0]) * 60 + int(now_time[1])
    for i, hour_end in enumerate(hours_schedule):
        # if the our hasn't ended yet return it's index
        if minutes < hour_end:
            return i
    # if there are no more hours in a day return -1
    return -1


def get_classrooms():
    global classroom
    # get code from website of chosen school
    response_cl = requests.get(f'https://www.easistent.com/urniki/{school}/ucilnice/')
    soup_cl = BeautifulSoup(response_cl.text, features='html.parser')
    # extract the parameters
    classrooms_raw = soup_cl.find('select', attrs={'id': 'id_parameter'})
    # extract the options
    classrooms_raw_list = classrooms_raw.find_all('option')
    # save into list classrooms [room name] = ID
    for c in classrooms_raw_list:
        classrooms[c.get_text()] = c.attrs['value']
    classroom = classrooms[str(obj['classroom_name'])]
    return


def get_grades():
    global grade
    date_time = time.asctime()
    # get the day of the week
    now_day = date_time.split()[0]
    now_hour = get_now_hour()
    # if there are no more hours return
    if now_hour == -1:
        grade = None
        return
    # get code from website of chosen school
    response_cl = requests.get(f'https://www.easistent.com/urniki/{school}/razredi/')
    soup_cl = BeautifulSoup(response_cl.text, features='html.parser')
    # extract the parameters
    grades_raw = soup_cl.find('select', attrs={'id': 'id_parameter'})
    # extract the options
    grades_raw_list = grades_raw.find_all('option')
    # save into list grades [grade name] = ID
    for g in grades_raw_list:
        grades[g.get_text()] = g.attrs['value']
    for day in days:
        # find witch day is today and grab the grade witch has lessons now
        if days[day] == now_day:
            grade_name = classroom_schedule[int(day)].hours[now_hour].grade
            if grade_name == 'vacant':
                grade = None
                return
            grade = grades[grade_name]
            break
    return


def get_classroom_schedule():
    get_classrooms()
    # get code from website of chosen school and classroom
    response = requests.get(f'https://www.easistent.com/urniki/{school}/ucilnice/{classroom}')
    soup = BeautifulSoup(response.text, features='html.parser')
    # get the schedule
    table = soup.find('table', attrs={'class': 'ednevnik-seznam_ur_teden'})
    # extract the rows
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        # extract the columns
        columns = row.find_all('td', attrs={'class': 'ednevnik-seznam_ur_teden-td'})
        for j, column in enumerate(columns):
            tmp = None
            # skip the 1st row (has hours) and go over the work week only
            if j == 0:
                hour_end_raw = column.find('div', attrs={'class': 'text10 gray'}).get_text().split(' - ')[1]
                hour_end = int(hour_end_raw.split(':')[0]) * 60 + int(hour_end_raw.split(':')[1])
                hours_schedule.append(hour_end)
                continue
            if j > 5:
                break
            # get the grades and professors that teach them
            grade_raw = column.find('td', attrs={'class': 'text14 bold'})
            professor_raw = column.find('div', attrs={'class': 'text11'})
            # try to modify grade_raw and professors_raw
            try:
                tmp = HourClassroom(
                    column.attrs['id'].split('-')[3],
                    column.attrs['id'].split('-')[4],
                    column.attrs['id'].split('-')[5],
                    column.attrs['id'].split('-')[6],
                    grade_raw.get_text().strip().replace(' ', ''),
                    professor_raw.get_text().strip()
                )
            # if they are empty and you fail, leave them out
            except AttributeError:
                tmp = HourClassroom(
                    column.attrs['id'].split('-')[3],
                    column.attrs['id'].split('-')[4],
                    column.attrs['id'].split('-')[5],
                    column.attrs['id'].split('-')[6]
                )
            # save into schedule[day].hours
            classroom_schedule[j - 1].hours.append(tmp)
            # extract the the double hours
            not_first = column.find('div', attrs={'class': 'ni_prvi'})
            if not_first:
                blocks = not_first.find_all('div', attrs={'class': 'ednevnik-seznam_ur_teden-urnik'})
                for block in blocks:
                    # get the grades and professors that teach them
                    grade_raw = block.find('td', attrs={'class': 'text14 bold'})
                    professor_raw = block.find('div', attrs={'class': 'text11'})
                    # get the place where the schedule is saved
                    tmp = classroom_schedule[j - 1].hours
                    l_t = len(tmp)
                    grade_new = f'{tmp[l_t - 1].grade}, {grade_raw.get_text().strip().replace(" ", "")}' if \
                        tmp[l_t - 1].grade != grade_raw.get_text().strip().replace(" ", "") else tmp[l_t - 1].grade
                    professor_new = f'{tmp[l_t - 1].professor}, {professor_raw.get_text().strip()}' if \
                        tmp[l_t - 1].professor != professor_raw.get_text().strip() else tmp[l_t - 1].professor
                    # make new tmp
                    tmp_new = HourClassroom(
                        # keep the times the same
                        tmp[l_t - 1].hour,
                        tmp[l_t - 1].year,
                        tmp[l_t - 1].month,
                        tmp[l_t - 1].day,
                        # add grades and professors
                        grade_new,
                        professor_new
                    )
                    # save into schedule[day].hours[last_hour_saved]
                    classroom_schedule[j - 1].hours[l_t - 1] = tmp_new
    return classroom_schedule


def get_grade_schedule():
    get_grades()
    if grade is None:
        return None
    # get code from website of chosen school and classroom
    response = requests.get(f'https://www.easistent.com/urniki/{school}/razredi/{grade}')
    soup = BeautifulSoup(response.text, features='html.parser')
    # get the schedule
    table = soup.find('table', attrs={'class': 'ednevnik-seznam_ur_teden'})
    # extract the rows
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        # extract the columns
        columns = row.find_all('td', attrs={'class': 'ednevnik-seznam_ur_teden-td'})
        for j, column in enumerate(columns):
            tmp = None
            # skip the 1st row (has hours) and go over the work week only
            if j == 0:
                continue
            if j > 5:
                break
            # get the subjects and professors that teach them, and rooms they are in
            subject_raw = column.find('td', attrs={'class': 'text14 bold'})
            info_raw = column.find('div', attrs={'class': 'text11'})
            # try to modify grade_raw and professors_raw
            try:
                tmp = HourGrade(
                    column.attrs['id'].split('-')[3],
                    column.attrs['id'].split('-')[4],
                    column.attrs['id'].split('-')[5],
                    column.attrs['id'].split('-')[6],
                    subject_raw.get_text().strip().replace(' ', ''),
                    info_raw.get_text().strip().split(', ')[0],
                    info_raw.get_text().strip().split(', ')[1]
                )
            # if they are empty and you fail, leave them out
            except AttributeError:
                tmp = HourGrade(
                    column.attrs['id'].split('-')[3],
                    column.attrs['id'].split('-')[4],
                    column.attrs['id'].split('-')[5],
                    column.attrs['id'].split('-')[6]
                )
            # save into schedule[day].hours
            grade_schedule[j - 1].hours.append(tmp)
            # extract the the double hours
            not_first = column.find('div', attrs={'class': 'ni_prvi'})
            if not_first:
                blocks = not_first.find_all('div', attrs={'class': 'ednevnik-seznam_ur_teden-urnik'})
                for block in blocks:
                    # get the subjects and professors that teach them, and rooms they are in
                    subject_raw = block.find('td', attrs={'class': 'text14 bold'})
                    info_raw = block.find('div', attrs={'class': 'text11'})
                    professor = info_raw.get_text().strip().split(', ')[0]
                    classroom = info_raw.get_text().strip().split(', ')[1]
                    # get the place where the schedule is saved
                    tmp = grade_schedule[j - 1].hours
                    l_t = len(tmp)
                    # if content is the same leave as is, else put together new content
                    subject_new = f'{tmp[l_t - 1].subject}, {subject_raw.get_text().strip().replace(" ", "")}' if \
                        tmp[l_t - 1].subject != subject_raw.get_text().strip().replace(" ", "") else tmp[l_t - 1].subject
                    professor_new = f'{tmp[l_t - 1].professor}, {professor}' if \
                        tmp[l_t - 1].professor != professor else tmp[l_t - 1].professor
                    classroom_new = f'{tmp[l_t - 1].classroom}, {classroom}' if \
                        tmp[l_t - 1].classroom != classroom else tmp[l_t - 1].classroom
                    # make new tmp
                    tmp_new = HourGrade(
                        # keep the times the same
                        tmp[l_t - 1].hour,
                        tmp[l_t - 1].year,
                        tmp[l_t - 1].month,
                        tmp[l_t - 1].day,
                        # add grades, professors and classrooms
                        subject_new,
                        professor_new,
                        classroom_new
                    )
                    # save into schedule[day].hours[last_hour_saved]
                    grade_schedule[j - 1].hours[l_t - 1] = tmp_new
    return grade_schedule
