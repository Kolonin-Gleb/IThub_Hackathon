from flask import (
    Flask, 
    render_template, 
    request, 
    jsonify
)

from parser.parser import parse
import json


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
    ident_1    = request.form.get('ident_1')
    ident_2    = request.form.get('ident_2')
    ident_3    = request.form.get('ident_3')
    ident_4    = request.form.get('ident_4')
    ident_5    = request.form.get('ident_5')
    ident_6    = request.form.get('ident_6')
    ident_7    = request.form.get('ident_7')

    date = ".".join(date.split('-')[::-1])

    print()
    print(['eml/data.eml', sender, date, event_type])
    print()

    filename = parse('eml/data.eml', sender, date, event_type)
    data = open(filename, encoding='utf-8')
    return jsonify(json.load(data))


@app.route('/get_identificator_data', methods=['POST'])
def get_identificator_data():
    return open('eml/identificators.json', encoding='utf8')


if __name__ == "__main__":
    app.run(host="localhost", debug = True)