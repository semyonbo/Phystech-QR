import subprocess

import PIL
import qrcode.image.svg
import io
import svgutils.transform as st
inp='лоплтглшрьбщшт  ьнт90п0ьб 9ь бщшьватрь0х вы9абрпв трг лб рапрапр апрапрар апр апр апр а пр вапрвапрапрапрапр984949 48па4р98авп4р ва4пр9 849ап8р4 в9пар ьтвыапшнвпорвапвал-п двапдвап швап ва пвап '

def qr_gen_vecotr(inp, logo_type, logo_colour, back_type):
    global back, back_width, logo
    back_const = 0.85
    code_distor = 0.0235

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
        # base64_image = base64.b64encode(image.getvalue()).decode()
        return a

    pure_code_str=create_vect(inp)
    pure_code=st.fromstring(pure_code_str)
    code_width = float(pure_code.height[:-2])

    if back_type is not None:
        if back_type=='var1':
            back=st.fromfile('code_templates/back_1.svg')
        elif back_type=='var2':
            back=st.fromfile('code_templates/back_2.svg')
        elif back_type=='var3':
            back = st.fromfile('code_templates/back_3.svg')
    elif back_type is None:
        back = st.fromfile('code_templates/white.svg')
        back_const = 1

    back_width = float(back.width)
    scale = back_width * back_const / code_width
    pure_code=pure_code.getroot()
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
        logo.moveto((back_width*(1 - scale_logo)) // 2, (back_width *(1 - scale_logo)) // 2, scale_logo)
        back.append(logo)






