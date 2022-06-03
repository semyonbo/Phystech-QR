import io
import sqlite3
from base64 import b64encode
import datetime as dat
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from hashids import Hashids
from generator import qr_gen
import requests as get_ip


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ILOVW_kAn6e_W3sT_BuT_h6Ate_P8ySicZ'
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

def make_code(inp, enable_back, back_type, enable_logo, logo_type, logo_colour):
    if enable_back is None:
        back_type = None
    if enable_logo is None:
        logo_type = None
    if logo_type == 'round':
        logo_colour = None
    return qr_gen(inp, logo_type, logo_colour, back_type)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/main', methods=['GET'])
def get_main():
    return render_template('main.html')


@app.route('/code', methods=['GET', 'POST'])
def get_code():
    global short_url
    short_url = None
    conn = get_db_connection()
    if request.method == 'POST':
        form_type = request.form.get('inp_radio')
        if form_type == '1':
            inp = request.form.get('link_inp')
            if request.form.get('stats_option') == "on":
                url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)', (inp,))
                conn.commit()
                conn.close()
                url_id = url_data.lastrowid
                hashid = hashids.encode(url_id)
                short_url = request.host_url + hashid
                inp=short_url
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
        imag = make_code(inp, request.form.get('code_back_enable'), request.form.get('back_type'), request.form.get('logo'), request.form.get('logo_form'), request.form.get('color'))
        imag.convert("RGBA")
        data = io.BytesIO()
        imag.save(data, 'png')
        encoded_img_data = b64encode(data.getvalue())
        if short_url is not None:
            return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='none', shorten_url=short_url)
        else:
            return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='none')
    else:
        return render_template('code.html', hidden='none', disp='')


@app.route('/stats', methods=['GET', 'POST'])
def get_stats():
    if request.method == 'POST':
        conn = get_db_connection()
        inp_code = request.form.get('stats_code_inp')
        link_id = hashids.decode(inp_code)
        if link_id:
            link_id = link_id[0]
            link_data = conn.execute('SELECT original_url, clicks FROM urls'
                                     ' WHERE id = (?)', (link_id,)
                                     ).fetchone()
            clicks = int(link_data['clicks'])
            daily_timedelta=str(dat.datetime.now() - dat.timedelta(days=1))[:19]
            weekly_timedelta=str(dat.datetime.now() - dat.timedelta(days=7))[:19]
            mounthly_timedelta=str(dat.datetime.now() - dat.timedelta(days=30))[:19]
            daily = conn.execute('SELECT COUNT(*) FROM stats WHERE id =(?) and DATETIME(time_use) >= DATETIME((?))', (link_id, daily_timedelta)).fetchone()[0]
            weekly = conn.execute('SELECT COUNT(*) FROM stats WHERE id =(?) and DATETIME(time_use) >= DATETIME((?))',
                                 (link_id, weekly_timedelta)).fetchone()[0]
            mounthly = conn.execute('SELECT COUNT(*) FROM stats WHERE id =(?) and DATETIME(time_use) >= DATETIME((?))',
                                 (link_id, mounthly_timedelta)).fetchone()[0]
            conn.close()
            return render_template('stats.html', vis='', all_clicks=clicks, daily=daily, weekly=weekly, mounthly=mounthly)
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
        url_data = conn.execute('SELECT original_url, clicks FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']
        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks + 1, original_id))
        conn.execute('UPDATE urls SET last_use = ? WHERE id = ?',
                     (str(dat.datetime.now())[:19], original_id))
        now=str(dat.datetime.now())[:19]
        conn.execute('INSERT INTO stats (id,time_use) VALUES (?, ?)', (original_id, now))
        location_info=get_ip.get(f'http://ip-api.com/csv/{request.remote_addr}?fields=country,countryCode,city,query').text
        # locat=location_info.split(",")
        # City=locat[2]
        # Counrty=locat[1]
        # User_ip=locat[3]
        # #request.remote_addr
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        return redirect(url_for('get_main'))


# conn=get_db_connection()
# cur=conn.cursor()
# cur.execute("SELECT * FROM urls")
# rows = cur.fetchall()
# conn.close()
# for row in rows:
#     print(tuple(row))
