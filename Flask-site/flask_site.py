import base64
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from generator import qr_gen
import io

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL']=False

@app.route('/contact', methods=['GET'])
def get_contact():
    return(render_template('contact.html'))

@app.route('/telegram', methods=['GET'])
def get_telegram():
    return(render_template('telegram.html'))

@app.route('/main', methods=['GET'])
def get_main():
    return(render_template('main.html'))

@app.route('/code', methods=['GET'])
def get_code():
    return(render_template('code.html'))

@app.route('/stats', methods=['GET'])
def get_stats():
    return(render_template('stats.html'))
@app.route('/img', methods=['POST'])
def serve_img():
    inp=request.form.get('QR_inp')
    imag=qr_gen(inp)
    data=io.BytesIO()
    imag.save(data,'PNG')
    encoded_img_data=base64.b64encode(data.getvalue())
    return render_template('test_img.html', img_data=encoded_img_data.decode('utf-8'))


# @app.route('/')
# def index():
#     return render_template('index.html')
#

if __name__ == '__main__':
    app.run(debug=True)
