import base64
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from generator import qr_gen
import io

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = False

@app.route('/contact', methods=['GET'])
def get_contact():
    return(render_template('contact.html'))

@app.route('/telegram', methods=['GET'])
def get_telegram():
    return(render_template('telegram.html'))

@app.route('/main', methods=['GET'])
def get_main():
    return(render_template('main.html'))

@app.route('/code', methods=['GET','POST'])
def get_code():
    if request.method == 'POST':
        inp = request.form.get('QR_inp')
        type=request.form.get('type')
        imag = qr_gen(inp, type)
        data = io.BytesIO()
        imag.save(data, 'PNG')
        encoded_img_data = base64.b64encode(data.getvalue())
        return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'))
    else:
        return(render_template('code.html', hidden='hidden'))


@app.route('/stats', methods=['GET'])
def get_stats():
    return(render_template('stats.html'))

@app.route('/')
def redirecting():
    return redirect(url_for('get_main'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='88', debug=True)
