import base64, sqlite3, io
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from generator import qr_gen
from hashids import Hashids
from datetime import timedelta, datetime

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = False
app.config['SECRET_KEY'] = 'ILOVW_kAn6e_W3sT_BuT_h6Ate_P8ySicZ'
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/main', methods=['GET'])
def get_main():
    return (render_template('main.html'))


@app.route('/code', methods=['GET', 'POST'])
def get_code():
    conn=get_db_connection()
    if request.method == 'POST':
        form_type = request.form.get('inp_radio')
        if form_type == '1':
            inp = request.form.get('link_inp')
            type = request.form.get('type')
            imag = qr_gen(inp, type)
            data = io.BytesIO()
            imag.save(data, 'PNG')
            encoded_img_data = base64.b64encode(data.getvalue())
            if request.form.get('stats_option') == "1":
                url_data=conn.execute('INSERT INTO urls (original_url) VALUES (?)',(inp,))
                conn.commit()
                conn.close()
                url_id = url_data.lastrowid
                hashid = hashids.encode(url_id)
                short_url = request.host_url + hashid
                return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='', shorten_url=short_url)
            else:
                return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='')
        if form_type == '2':
            wifi_name = request.form.get('wifi_name_inp')
            wifi_pass = request.form.get('wifi_pass_inp')
            inp = 'WIFI:S:' + wifi_name + ';T:WPA;P:' + wifi_pass + ';;'
        elif form_type == "3":
            name = request.form.get('name_inp')
            phone = request.form.get('phone_inp')
            email = request.form.get('email_inp')
            inp = 'BEGIN:VCARD\nN:' + name + '\nTEL:' + phone + '\nEMAIL:' + email + '\nVERSION:3.0\nEND:VCARD'
        elif form_type == '4':
            inp = request.form.get('text_inp')
        elif form_type == '5':
            geo = request.form.get('geo_inp')
            inp = 'geo:' + geo.split(' ')[0] + '' + geo.split(' ')[1] + ',100'
        type = request.form.get('type')
        imag = qr_gen(inp, type)
        data = io.BytesIO()
        imag.save(data, 'PNG')
        encoded_img_data = base64.b64encode(data.getvalue())
        return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='')
    else:
        return render_template('code.html', hidden='hidden', disp='')


@app.route('/stats', methods=['GET'])
def get_stats():
    return (render_template('stats.html'))


@app.route('/')
def redirecting():
    return redirect(url_for('get_main'))

@app.route('/<id>')
def url_redirect(id):
    conn=get_db_connection()
    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute('SELECT original_url, clicks, daily, weekly, monthly, last_use FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']
        # daily_clicks=url_data['daily']
        # weekly_clicks=url_data['weekly']
        # monthly_clicks=url_data['monthly']
        # last_use=url_data['last_use']
        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks + 1, original_id))
        conn.execute('UPDATE urls SET last_use = ? WHERE id = ?',
                     (datetime.now(), original_id))
        conn.commit()
        conn.close()
        # if last_use <= datetime.now() - timedelta(days=1):
        #     daily_clicks=+1
        # if last_use <= datetime.now() - timedelta(days=7):
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('get_main'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='88', debug=True)
