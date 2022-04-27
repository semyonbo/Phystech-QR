import base64
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from generator import qr_gen
import io


app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = False

@app.route('/telegram', methods=['GET'])
def get_telegram():
    return(render_template('telegram.html'))

@app.route('/main', methods=['GET'])
def get_main():
    return(render_template('main.html'))


@app.route('/code', methods=['GET','POST'])
def get_code():
    if request.method == 'POST':
        form_type=request.form.get('inp_radio')
        if form_type=='1':
            inp = request.form.get('link_inp')
        elif form_type=='2':
            wifi_name=request.form.get('wifi_name_inp')
            wifi_pass=request.form.get('wifi_pass_inp')
            inp='WIFI:S:'+wifi_name+';T:WPA;P:'+wifi_pass+';;'
        elif form_type=="3":
            name=request.form.get('name_inp')
            phone=request.form.get('phone_inp')
            email=request.form.get('email_inp')
            inp='BEGIN:VCARD\nN:'+name+'\nTEL:'+phone+'\nEMAIL:'+email+'\nVERSION:3.0\nEND:VCARD'
        elif form_type=='4':
            inp=request.form.get('text_inp')
        elif form_type=='5':
            geo=request.form.get('geo_inp')
            inp='geo:'+geo.split(' ')[0]+''+geo.split(' ')[1]+',100'
        type = request.form.get('type')
        imag = qr_gen(inp, type)
        data = io.BytesIO()
        imag.save(data, 'PNG')
        encoded_img_data = base64.b64encode(data.getvalue())
        return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='')
    else:
        return (render_template('code.html', hidden='hidden',disp=''))


@app.route('/stats', methods=['GET'])
def get_stats():
    return(render_template('stats.html'))

@app.route('/')
def redirecting():
    return redirect(url_for('get_main'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='88', debug=True)
