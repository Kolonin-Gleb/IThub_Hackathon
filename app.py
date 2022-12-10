from flask import (
    Flask, 
    render_template
)
import datetime


app = Flask(__name__, static_folder="static")


@app.route('/')
def root():
    return render_template(
        "index.html", 
        title = "ZakupkiHack"
    )


if __name__ == "__main__":
    app.run(host="localhost", debug = True)