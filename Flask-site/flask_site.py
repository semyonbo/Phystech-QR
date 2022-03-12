from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img

logo=img(scr='/static/img/logophysics.svg', height="3%", width="3%", style="margin-top:-15px")
topbar = Navbar(logo,
                View('Новый физтех', 'get_main'),
                View('Генератор', 'get_code'),
                View('Телеграм бот', 'get_telegram'),
                View('Статистика', 'get_stats'),
                View('Контакты', 'get_contact'),
                )

# registers the "top" menubar
nav = Nav()
nav.register_element('top', topbar)

app = Flask(__name__)
Bootstrap(app)

@app.route('/contact', methods=['GET'])
def get_contact():
    return(render_template('contact.html'))

@app.route('/telegram', methods=['GET'])
def get_telegram():
    return(render_template('telegram.html'))

@app.route('/', methods=['GET'])
def get_main():
    return(render_template('main.html'))

@app.route('/code', methods=['GET'])
def get_code():
    return(render_template('code.html'))

@app.route('/stats', methods=['GET'])
def get_stats():
    return(render_template('stats.html'))

nav.init_app(app)
# @app.route('/')
# def index():
#     return render_template('index.html')
#

if __name__ == '__main__':
    app.run(debug=True)
