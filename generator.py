def qr_gen(inp, logo_type, logo_colour, back_type):
    from PIL import Image
    import qrcode.image.svg
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
    from io import BytesIO
    import cairosvg
    import os

    # settings
    dist_amount = 0.38
    code_pixel_size = 20
    qr_border_size = 0
    code_color = 'black'
    backgroud_color = 'white'
    back_const = 1.18

    # Рендер
    def render(QR_rastr, type_of_render, logo_type_func, logo_colour_func, back_type_func):
        code_with = QR_rastr.size[0]
        code_height = QR_rastr.size[1]
        out = BytesIO()
        if type_of_render == 'logo':
            width = int(code_with * dist_amount)
            height = int(code_height * dist_amount)
            if logo_type_func == 'round':
                cairosvg.svg2png(url="logophysics2.svg", write_to=out)
            elif logo_type_func == 'square':
                if logo_colour_func == 'yellow':
                    cairosvg.svg2png(url="logophysics.svg", write_to=out)
                elif logo_colour_func == 'black':
                    cairosvg.svg2png(url="logophysics3.svg", write_to=out)
            pos = ((code_with - width) // 2, (code_height - height) // 2)
        elif type_of_render == 'back':
            width = int(code_with * back_const)
            height = int(code_height * back_const)
            if back_type_func == 'var1':
                cairosvg.svg2png(url="back_1.svg", write_to=out)
            elif back_type_func == 'var2':
                cairosvg.svg2png(url="back_2.svg", write_to=out)
            elif back_type_func == 'var3':
                cairosvg.svg2png(url="back_3.svg", write_to=out)
            pos = ((width - code_with) // 2, (height - code_height) // 2)
        part_img = Image.open(out).convert("RGBA")
        part_img = part_img.resize((width, height), Image.ANTIALIAS)
        if type_of_render == 'logo':
            QR_rastr.paste(part_img, pos, part_img)
            return QR_rastr
        elif type_of_render == 'back':
            part_img.paste(QR_rastr, pos, QR_rastr)
            return part_img

    # Creating rastr QR
    def create_qr(inp):
        PhyQR = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            border=qr_border_size,
            box_size=code_pixel_size
        )
        PhyQR.add_data(inp)
        PhyQR.make()
        img_PhyQR = PhyQR.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()).convert('RGBA')
        return img_PhyQR

    Pure_qr = create_qr(inp)
    if logo_type is None:
        return render(QR_rastr=Pure_qr, logo_type_func=None, logo_colour_func=None , type_of_render='back', back_type_func=back_type)
    elif logo_type is not None:
        if back_type is None:
            return render(QR_rastr=Pure_qr, type_of_render='logo', logo_type_func=logo_type, logo_colour_func=logo_colour, back_type_func=None)
        if back_type is not None:
            Qr_width_logo = render(QR_rastr=Pure_qr, type_of_render='logo', logo_type_func=logo_type, logo_colour_func=logo_colour, back_type_func=None)
            return render(Qr_width_logo, type_of_render='back', back_type_func=back_type, logo_type_func=None, logo_colour_func=None)


    # if type == 'on':
    #     return back
    # else:
    #     return img_PhyQR

    # Метод создания svg QR-кода
    # qrvec=qrcode.QRCode(
    #     error_correction=qrcode.constants.ERROR_CORRECT_H,
    #     border=1
    #
    # )
    # qrvec.add_data(inp)
    # qrvec.make(fit=True)
    # svgqr=qrvec.make_image(image_factory=qrcode.image.svg.SvgImage)
    # svgqr.save('testing.svg')
