from flask import (
    Flask, 
    render_template, 
    request, 
    jsonify,
    send_file
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
    ident_1    = request.form.get('ident_1').replace('##(', '<').replace(')##', '>')
    ident_2    = request.form.get('ident_2').replace('##(', '<').replace(')##', '>')
    ident_3    = request.form.get('ident_3').replace('##(', '<').replace(')##', '>')
    ident_4    = request.form.get('ident_4').replace('##(', '<').replace(')##', '>')
    ident_5    = request.form.get('ident_5').replace('##(', '<').replace(')##', '>')
    ident_6    = request.form.get('ident_6').replace('##(', '<').replace(')##', '>')
    ident_7    = request.form.get('ident_7').replace('##(', '<').replace(')##', '>')

    date = ".".join(date.split('-')[::-1])

    filename = parse('eml/data.eml', sender, date, event_type, ident_1, ident_2, ident_3, ident_4, ident_5, ident_6, ident_7)
    data = open(filename, encoding='utf-8')

    

    return jsonify(json.load(data))


@app.route('/get_identificator_data', methods=['POST'])
def get_identificator_data():
    file = open('eml/identificators.json', encoding='utf8')
    data = json.load(file)
    return jsonify(data)


@app.route('/download/<name>')
def download_file(name):
    path = 'eml/'
    return send_file(path + name, as_attachment=True)


if __name__ == "__main__":
    app.run(host="localhost", debug = True)