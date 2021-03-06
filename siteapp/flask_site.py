import base64
import io
import sqlite3
from base64 import b64encode
import datetime as dat
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from hashids import Hashids
from generator import qr_gen_vecotr
import requests as get_ip

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'ILOVW_kAn6e_W3sT_BuT_h6Ate_P8ySicZ'
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


def make_code(inp, enable_back, back_type, enable_logo, logo_type, logo_colour, code_type, stats_code):
    if enable_back is None:
        back_type = None
    if enable_logo is None:
        logo_type = None
    if logo_type == 'round':
        logo_colour = None
    return qr_gen_vecotr(inp, logo_type, logo_colour, back_type, code_type, stats_code)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/main', methods=['GET'])
def get_main():
    return render_template('main.html')


@app.route('/code', methods=['GET', 'POST'])
def get_code():
    short_url = None
    stats_code = None
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
                stats_code = hashid
                short_url = request.host_url + hashid
                inp = short_url
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
        imag = make_code(inp, request.form.get('code_back_enable'), request.form.get('back_type'),
                         request.form.get('logo'), request.form.get('logo_form'), request.form.get('color'), 'rastr',
                         stats_code)
        imag.convert("RGBA")
        data = io.BytesIO()
        svg_str = make_code(inp, request.form.get('code_back_enable'), request.form.get('back_type'),
                            request.form.get('logo'), request.form.get('logo_form'), request.form.get('color'),
                            'vector', stats_code)
        imag.save(data, 'png')
        encoded_img_data = b64encode(data.getvalue())
        encoded_svg_data = base64.b64encode(svg_str.encode('utf-8'))
        if short_url is not None:
            return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='none',
                                   shorten_url=short_url, svg_data=encoded_svg_data.decode('utf-8'),
                                   stats_code=stats_code, stats_hidden='')
        else:
            return render_template('code.html', hidden='', img_data=encoded_img_data.decode('utf-8'), disp='none',
                                   svg_data=encoded_svg_data.decode('utf-8'), stats_hidden='none')
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
            daily_timedelta = str(dat.datetime.now() - dat.timedelta(days=1))[:19]
            weekly_timedelta = str(dat.datetime.now() - dat.timedelta(days=7))[:19]
            mounthly_timedelta = str(dat.datetime.now() - dat.timedelta(days=30))[:19]
            daily = conn.execute('SELECT COUNT(*) FROM stats WHERE id =(?) and DATETIME(time_use) >= DATETIME((?))',
                                 (link_id, daily_timedelta)).fetchone()[0]
            weekly = conn.execute('SELECT COUNT(*) FROM stats WHERE id =(?) and DATETIME(time_use) >= DATETIME((?))',
                                  (link_id, weekly_timedelta)).fetchone()[0]
            mounthly = conn.execute('SELECT COUNT(*) FROM stats WHERE id =(?) and DATETIME(time_use) >= DATETIME((?))',
                                    (link_id, mounthly_timedelta)).fetchone()[0]

            cities = conn.execute('SELECT DISTINCT(city) FROM stats WHERE id=(?)', (link_id,)).fetchall()
            data = []
            for city in cities:
                nu = \
                    conn.execute('SELECT COUNT(*) FROM stats WHERE id=(?) and city=(?)', (link_id, city[0])).fetchone()[
                        0]
                country = \
                    conn.execute('SELECT country FROM stats WHERE id=(?) and city=(?)', (link_id, city[0])).fetchone()[
                        0]
                data.append([city[0], country, nu])
            dates = conn.execute(
                'SELECT DISTINCT DATE(time_use) FROM stats WHERE id=(?) and DATETIME(time_use) >= DATETIME(?)',
                (link_id, mounthly_timedelta)).fetchall()
            plot_data = []
            for date in dates:
                numb = conn.execute('SELECT COUNT(*) FROM stats WHERE id=(?) and DATE(time_use)=(?)',
                                    (link_id, date[0])).fetchone()[0]
                plot_data.append([date[0], numb])
            labels = [row[0] for row in plot_data]
            values = [row[1] for row in plot_data]
            conn.close()
            return render_template('stats.html', all_clicks=clicks, daily=daily, weekly=weekly, mounthly=mounthly,
                                   data=data, labels=labels, values=values, get='', post='none')
        else:
            return render_template('stats_error.html')
    else:
        return render_template('stats.html', post='', get='none')


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
        now = str(dat.datetime.now())[:19]
        if not request.headers.getlist("X-Forwarded-For"):
            ip = request.remote_addr
        else:
            ip = request.headers.getlist("X-Forwarded-For")[0]
        location_info = get_ip.get(
            f'http://ip-api.com/csv/{str(ip)}?fields=countryCode,city,query')
        location_info = location_info.text.split(',')
        if len(location_info) < 3:
            City = 'None'
            Counrty = 'None'
            User_ip = 'None'
        else:
            City = location_info[1]
            Counrty = location_info[0]
            User_ip = location_info[2]
        conn.execute('INSERT INTO stats (id,time_use,country,city,user_id) VALUES (?, ?, ?, ?, ?)',
                     (original_id, now, Counrty, City, User_ip))
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        return render_template('404.html')
