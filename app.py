from flask import (
    Flask, 
    render_template, 
    request
)

from parser.parser import parse


app = Flask(__name__, static_folder="static")


@app.route('/')
def root():
    return render_template(
        "index.html", 
        title = "ООО КВТ СЕРВИС"
    )

@app.route('/get_data', methods=['POST'])
def get_data():
    sender     = request.form.get('sender')
    event_type = request.form.get('event_type')
    date       = request.form.get('date')

    # return parse('eml/data.eml', sender, date)
    return open('eml/data.json', encoding='utf8')


if __name__ == "__main__":
    app.run(host="localhost", debug = True)