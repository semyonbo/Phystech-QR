import qrcode.image.svg
import io
import svgutils.transform as st
from PIL import Image
import qrcode.image.svg
from io import BytesIO
import cairosvg

# def qr_gen(inp, logo_type, logo_colour, back_type):
#
#
#     # settings
#     dist_amount = 0.38
#     code_pixel_size = 20
#     qr_border_size = 0
#     code_color = 'black'
#     backgroud_color = 'white'
#     back_const = 1.18
#
#     # Рендер
#     def render(QR_rastr, type_of_render, logo_type_func, logo_colour_func, back_type_func):
#         code_with = QR_rastr.size[0]
#         code_height = QR_rastr.size[1]
#         out = BytesIO()
#         if type_of_render == 'logo':
#             width = int(code_with * dist_amount)
#             height = int(code_height * dist_amount)
#             if logo_type_func == 'round':
#                 with open("code_templates/logophysics2.svg", "rb") as file:
#                     a=file.readlines()
#
#                 cairosvg.svg2png(file_obj=open("code_templates/logophysics2.svg", "rb"), write_to=out)
#             elif logo_type_func == 'square':
#                 if logo_colour_func == 'yellow':
#                     cairosvg.svg2png(file_obj=open("code_templates/logophysics.svg", "rb"), write_to=out)
#                 elif logo_colour_func == 'black':
#                     cairosvg.svg2png(file_obj=open("code_templates/logophysics3.svg", "rb"), write_to=out)
#             pos = ((code_with - width) // 2, (code_height - height) // 2)
#         elif type_of_render == 'back':
#             width = int(code_with * back_const)
#             height = int(code_height * back_const)
#             if back_type_func == 'var1':
#                 cairosvg.svg2png(file_obj=open("code_templates/back_1.svg", "rb"), write_to=out)
#             elif back_type_func == 'var2':
#                 cairosvg.svg2png(file_obj=open("code_templates/back_2.svg", "rb"), write_to=out)
#             elif back_type_func == 'var3':
#                 cairosvg.svg2png(file_obj=open("code_templates/back_3.svg", "rb"), write_to=out)
#             pos = ((width - code_with) // 2, (height - code_height) // 2)
#         part_img = Image.open(out).convert("RGBA")
#         part_img = part_img.resize((width, height), Image.ANTIALIAS)
#         if type_of_render == 'logo':
#             QR_rastr.paste(part_img, pos, part_img)
#             return QR_rastr
#         elif type_of_render == 'back':
#             part_img.paste(QR_rastr, pos, QR_rastr)
#             return part_img
#
#     # Creating rastr QR
#     def create_qr(inp):
#         PhyQR = qrcode.QRCode(
#             error_correction=qrcode.constants.ERROR_CORRECT_H,
#             border=qr_border_size,
#             box_size=code_pixel_size
#         )
#         PhyQR.add_data(inp)
#         PhyQR.make()
#         img_PhyQR = PhyQR.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()).convert('RGBA')
#         return img_PhyQR
#
#     Pure_qr = create_qr(inp)
#     if logo_type is None:
#         if back_type is None:
#             return Pure_qr
#         else:
#             return render(QR_rastr=Pure_qr, logo_type_func=None, logo_colour_func=None , type_of_render='back', back_type_func=back_type)
#     elif logo_type is not None:
#         if back_type is None:
#             return render(QR_rastr=Pure_qr, type_of_render='logo', logo_type_func=logo_type, logo_colour_func=logo_colour, back_type_func=None)
#         if back_type is not None:
#             Qr_width_logo = render(QR_rastr=Pure_qr, type_of_render='logo', logo_type_func=logo_type, logo_colour_func=logo_colour, back_type_func=None)
#             return render(Qr_width_logo, type_of_render='back', back_type_func=back_type, logo_type_func=None, logo_colour_func=None)



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
    if back_type is None and stats_code is not None:
        stats_template = st.fromfile('code_templates/template_for_label.svg')
        stats_template = stats_template.getroot()
        back.append(stats_template)
    code_str=back.to_str()[:-1]
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
        rastr_img=Image.open(out).convert("RGBA")
        return rastr_img
    elif code_type == 'vector':
        return code_str











