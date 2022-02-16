import qrcode
from PIL import Image
import math
inp=input()
# qr = qrcode.QRCode(
#     error_correction=qrcode.constants.ERROR_CORRECT_Q,
#     version=None,
#     box_size=1,
#     border=2,
# )
# qr.add_data(inp)
# qr.make(fit=True)
# img = qr.make_image(fill_color="black",back_color="white")
# type(img)
# img.save('qrtest.png')

logo=Image.open("logo.jpg")
qr_big = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr_big.add_data(inp)
qr_big.make()
img_qr_big = qr_big.make_image(fill_color="black",back_color="white").convert('RGB')
new_width  = int(img_qr_big.size[0]*0.3)
new_height = int(img_qr_big.size[1]*0.3)
logo = logo.resize((new_width, new_height), Image.ANTIALIAS)
pos = ((img_qr_big.size[0] - logo.size[0]) // 2, (img_qr_big.size[1] - logo.size[1]) // 2)

img_qr_big.paste(logo, pos)
img_qr_big.save('qr_red.png')
