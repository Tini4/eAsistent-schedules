from schedules import init, get_classroom_schedule, get_grade_schedule
from flask import Flask, render_template
from shower_thoughts import get_shower_thoughts
import random

app = Flask('app')
# init()
# classroom_schedule = get_classroom_schedule()
# grade_schedule = get_grade_schedule()
shower_thoughts = get_shower_thoughts()


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html',
                           # classroom_schedule=classroom_schedule,
                           # grade_schedule=grade_schedule,
                           shower_thought=random.choice(shower_thoughts)
                           )


if __name__ == "__main__":
    app.run(debug=True)
