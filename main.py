from schedules import init, get_classroom_schedule, get_grade_schedule
from flask import Flask, render_template

app = Flask('app')
init()
classroom_schedule = get_classroom_schedule()
grade_schedule = get_grade_schedule()


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', classroom_schedule=classroom_schedule, grade_schedule=grade_schedule)


'''
for day in classroom_schedule:
    print(f'\n\n{day.name}\n')
    for hour in day.hours:
        print()
        print(hour.grade)
        print(hour.professor)

print('\n\n\n')

for day in grade_schedule:
    print(f'\n\n{day.name}\n')
    for hour in day.hours:
        print()
        print(hour.subject)
        print(hour.professor)
        print(hour.classroom)
'''

if __name__ == "__main__":
    app.run(debug=True)
