from schedules import init, get_classroom_schedule, get_grade_schedule
from flask import Flask, render_template
from shower_thoughts import get_shower_thoughts
import random
import schedule
import time

app = Flask('app')
# init()
# classroom_schedule = get_classroom_schedule()
# grade_schedule = get_grade_schedule()
shower_thoughts = get_shower_thoughts()
shower_thought = random.choice(shower_thoughts)


def update_shower_thoughts():
    shower_thoughts = get_shower_thoughts()


def update_schedules():
    # init()
    # classroom_schedule = get_classroom_schedule()
    # grade_schedule = get_grade_schedule()
    pass


def next_thought():
    shower_thought = random.choice(shower_thoughts)


schedule.every(2).hours.at(':00').do(update_shower_thoughts)
schedule.every(5).minutes.at(':00').do(update_schedules)
schedule.every(20).seconds.do(next_thought)


'''while True:
    schedule.run_pending()
    time.sleep(1)'''


@app.route('/')  # , methods=['POST', 'GET'])
def index():
    return render_template('index.html',
                           # classroom_schedule=classroom_schedule,
                           # grade_schedule=grade_schedule,
                           shower_thought=shower_thought
                           )


if __name__ == "__main__":
    app.run(debug=True)
