def qr_gen(inp, type):
    from PIL import Image
    import qrcode.image.svg
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
    from io import BytesIO
    import cairosvg

    # settings
    dist_amount = 0.3
    code_pixel_size = 20
    qr_border_size = 0
    code_color = 'black'
    backgroud_color = 'white'
    back_const = 1.24


    # Рендер логотипа
    def render_logo(code_with, code_height, type):
        width_logo = int(code_with * dist_amount)
        height_logo = int(code_height * dist_amount)
        out1=BytesIO()
        cairosvg.svg2png(url="logophysics2.svg", write_to=out1)
        img_logo=Image.open(out1)
        img_logo.convert("RGBA")
        img_logo=img_logo.resize((width_logo,height_logo), Image.ANTIALIAS)
        if type==1:
            return img_logo
        if type==2:
            pos=((code_with - width_logo) // 2, (code_height - height_logo) // 2)
            return pos

    # Рендер задника
    def render_back(code_with, code_height,type):
        with_back = int(code_with * back_const)
        height_back = int(code_height * back_const)
        out2 = BytesIO()
        cairosvg.svg2png(url="back.svg", write_to=out2)
        img_back = Image.open(out2)
        img_back.convert("RGBA")
        img_back = img_back.resize((with_back, height_back), Image.ANTIALIAS)
        if type==1:
            return img_back
        if type==2:
            pos=((with_back - code_with) // 2, (height_back - code_height) // 2)
            return pos

    # Creating QR
    PhyQR = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=qr_border_size,
        box_size=code_pixel_size
    )
    PhyQR.add_data(inp)
    PhyQR.make()
    img_PhyQR = PhyQR.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()).convert('RGBA')

    # Pasting logo to QR
    img_PhyQR.paste(render_logo(img_PhyQR.size[0], img_PhyQR.size[1],type=1), render_logo(img_PhyQR.size[0], img_PhyQR.size[1],type=2), render_logo(img_PhyQR.size[0], img_PhyQR.size[1],type=1))

    # Pasting background to QR
    back = render_back(img_PhyQR.size[0], img_PhyQR.size[1],type=1)
    back.paste(img_PhyQR, render_back(img_PhyQR.size[0], img_PhyQR.size[1],type=2), img_PhyQR)
    #back.save('QR.png')
    if type == 'default':
        return back
    elif type == 'noback':
        return img_PhyQR
    else:
        return back
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
