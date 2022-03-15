from flask import Flask, render_template
from flask_bootstrap import Bootstrap



# registers the "top" menubar

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL']=True

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

# @app.route('/')
# def index():
#     return render_template('index.html')
#

if __name__ == '__main__':
    app.run(debug=True)
