import qrcode
inp=input()
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
    version=None,
    box_size=1,
    border=2,
)
qr.add_data(inp)
qr.make(fit=True)
img = qr.make_image(fill_color="white",back_color="black")
type(img)
img.save('qrtest.png')
