import io
import sqlite3
from base64 import b64encode
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from hashids import Hashids
from generator import qr_gen
from flask_assets import Environment, Bundle


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
    return render_template('main.html')


@app.route('/code', methods=['GET', 'POST'])
def get_code():
    conn = get_db_connection()
    if request.method == 'POST':
        form_type = request.form.get('inp_radio')
        if form_type == '1':
            inp = request.form.get('link_inp')
            code_type = request.form.get('code_back_enable')
            if request.form.get('stats_option') == "on":
                url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)', (inp,))
                conn.commit()
                conn.close()
                url_id = url_data.lastrowid
                hashid = hashids.encode(url_id)
                short_url = request.host_url + hashid
                imag = qr_gen(short_url, code_type)
                data = io.BytesIO()
                imag.save(data, 'PNG')
                encoded_img_data = b64encode(data.getvalue())
                return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='',
                                       shorten_url=short_url)
            else:
                imag = qr_gen(inp, code_type)
                data = io.BytesIO()
                imag.save(data, 'PNG')
                encoded_img_data = b64encode(data.getvalue())
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
        code_type = request.form.get('code_back_enable')
        print(code_type)
        imag = qr_gen(inp, code_type)
        data = io.BytesIO()
        imag.save(data, 'PNG')
        encoded_img_data = b64encode(data.getvalue())
        return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='')
    else:
        return render_template('code.html', hidden='hidden', disp='')


@app.route('/stats', methods=['GET', 'POST'])
def get_stats():
    if request.method == 'POST':
        conn = get_db_connection()
        inp_code = request.form.get('stats_code_inp')
        print(inp_code)
        link_id = hashids.decode(inp_code)
        if link_id:
            link_id = link_id[0]
            link_data = conn.execute('SELECT original_url, clicks, daily, weekly, monthly, last_use FROM urls'
                                     ' WHERE id = (?)', (link_id,)
                                     ).fetchone()
            clicks = int(link_data['clicks'])
            conn.commit()
            conn.close()
            return render_template('stats.html', vis='', all_clicks=clicks)
        else:
            return render_template('stats.html', vis='', all_clicks='Code is incorrect')
    else:
        return render_template('stats.html', vis='hidden', all_clicks=0)


@app.route('/')
def redirecting():
    return redirect(url_for('get_main'))


@app.route('/<link>')
def url_redirect(link):
    conn = get_db_connection()
    original_id = hashids.decode(link)
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute('SELECT original_url, clicks, daily, weekly, monthly, last_use FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']
        daily_clicks = url_data['daily']
        last_use = url_data['last_use']
        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks + 1, original_id))
        conn.execute('UPDATE urls SET last_use = ? WHERE id = ?',
                     (datetime.now(), original_id))
        last_time = datetime.strptime(last_use[:19], '%Y-%m-%d %H:%M:%S')
        if datetime.date(last_time) <= datetime.date(datetime.now()):
            daily_clicks = daily_clicks + 1
        else:
            daily_clicks = 1
        conn.execute('UPDATE urls SET daily = ? WHERE id = ?',
                     (daily_clicks, original_id))
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('get_main'))


# conn=get_db_connection()
# cur=conn.cursor()
# cur.execute("SELECT * FROM urls")
# rows = cur.fetchall()
# conn.close()
# for row in rows:
#     print(tuple(row))
