from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/info_browse')
def browseInfo():
    return render_template("browseInfo.html")


if __name__ == '__main__':
    app.run()
