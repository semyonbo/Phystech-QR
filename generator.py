import qrcode.image.svg
import io
import svgutils.transform as st
from PIL import Image
import qrcode.image.svg
from io import BytesIO
import cairosvg


def qr_gen_vecotr(inp, logo_type, logo_colour, back_type, code_type, stats_code):
    global back, back_width, logo
    back_const = 0.85
    code_distor = 0.28

    def create_vect(inp):
        qrvec = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            border=0
        )
        qrvec.add_data(inp)
        qrvec.make(fit=True)
        svgqr = qrvec.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        stream = io.BytesIO()
        svgqr.save(stream)
        a = stream.getvalue().decode()
        return a

    pure_code_str = create_vect(inp)
    pure_code = st.fromstring(pure_code_str)
    code_width = float(pure_code.height[:-2])

    if back_type is not None:
        if back_type == 'var1':
            back = st.fromfile('code_templates/back_1.svg')
        elif back_type == 'var2':
            back = st.fromfile('code_templates/back_2.svg')
        elif back_type == 'var3':
            back = st.fromfile('code_templates/back_3.svg')
    elif back_type is None:
        back = st.fromfile('code_templates/white.svg')
        back_const = 1

    back_width = float(back.width)
    scale = back_width * back_const / code_width
    pure_code = pure_code.getroot()
    pure_code.moveto((back_width - code_width * scale) // 2, (back_width - code_width * scale) // 2, scale)
    back.append(pure_code)

    if logo_type is not None:
        if logo_type == 'round':
            logo = st.fromfile('code_templates/logophysics2.svg')
        elif logo_type == 'square':
            if logo_colour == 'black':
                logo = st.fromfile('code_templates/logophysics3.svg')
            elif logo_colour == 'yellow':
                logo = st.fromfile('code_templates/logophysics.svg')
        logo_width = float(logo.width)
        logo = logo.getroot()
        scale_logo = back_width * code_distor / logo_width
        logo.moveto((back_width * (1 - scale_logo)) // 2, (back_width * (1 - scale_logo)) // 2, scale_logo)
        back.append(logo)
    if back_type is None and stats_code is not None:
        stats_template = st.fromfile('code_templates/template_for_label.svg')
        stats_template = stats_template.getroot()
        back.append(stats_template)
    code_str = back.to_str()[:-1]
    if stats_code is not None:
        code_str = code_str.decode('utf-8')
        code_str = code_str.replace("CODE", stats_code)
        code_str.encode('utf-8')

    else:
        code_str = code_str.decode('utf-8')
        code_str = code_str.replace("CODE", "")
        code_str.encode('utf-8')

    if code_type == 'rastr':
        out = BytesIO()
        cairosvg.svg2png(bytestring=code_str, write_to=out)
        rastr_img = Image.open(out).convert("RGBA")
        return rastr_img
    elif code_type == 'vector':
        return code_str
