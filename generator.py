def qr_gen(inp):
    import qrcode
    from PIL import Image
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    import qrcode.image.svg
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
    import io
    import flask
    import base64

    # settings
    dist_amount = 0.3
    code_pixel_size = 20
    qr_border_size = 0
    code_color = 'black'
    backgroud_color = 'white'
    back_const = 1.24


    # Рендер логотипа
    def render_logo(code_with, code_height):
        width_logo = int(code_with * dist_amount)
        height_logo = int(code_height * dist_amount)
        drawing = svg2rlg("logophysics.svg")
        drawing.scale(width_logo / drawing.width, height_logo / drawing.height)
        drawing.height = height_logo + code_pixel_size // 10
        drawing.width = width_logo + code_pixel_size // 10
        renderPM.drawToFile(drawing, "temp/logo_rastr.png", fmt="PNG")


    # Рендер задника
    def render_back(code_with, code_height):
        with_back = int(code_with * back_const)
        height_back = int(code_height * back_const)
        backgr = svg2rlg('back.svg')
        backgr.scale(with_back / backgr.width, height_back / backgr.height)
        backgr.height = height_back
        backgr.width = with_back
        renderPM.drawToFile(backgr, "temp/back_rast.png", fmt='PNG')


    # Creating QR
    PhyQR = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=qr_border_size,
        box_size=code_pixel_size
    )
    PhyQR.add_data(inp)
    PhyQR.make()
    img_PhyQR = PhyQR.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()).convert('RGB')
    render_logo(img_PhyQR.size[0], img_PhyQR.size[1])

    # Pasting logo to QR
    logo = Image.open("temp/logo_rastr.png")
    pos = ((img_PhyQR.size[0] - logo.size[0]) // 2, (img_PhyQR.size[1] - logo.size[1]) // 2)
    img_PhyQR.paste(logo, pos)
    # img_PhyQR.save('QR.png')

    # Pasting background to QR
    render_back(img_PhyQR.size[0], img_PhyQR.size[1])
    back = Image.open('temp/back_rast.png')
    pos2 = ((back.size[0] - img_PhyQR.size[0]) // 2, (back.size[1] - img_PhyQR.size[1]) // 2)
    back.paste(img_PhyQR, pos2)
    # back.save('QR.png')

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