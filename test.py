import subprocess

import PIL
import qrcode.image.svg
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import io
import base64
import svgutils.transform as st
import re
inp='some data'

qrvec=qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=0
    )
qrvec.add_data(inp)
qrvec.make(fit=True)
svgqr=qrvec.make_image(image_factory=qrcode.image.svg.SvgImage)
print(type(svgqr))
stream = io.BytesIO()
svgqr.save(stream)
a=stream.getvalue().decode()
# base64_image = base64.b64encode(image.getvalue()).decode()

logo = st.fromfile('code_templates/logophysics2.svg')
scale=0.4
print(logo.height)
print(logo.get_size())
logo_width = float(re.sub("[^0-9]", '', logo.width))
logo_height = float(re.sub("[^0-9]", '', logo.width))
scaled_logo=st.SVGFigure(logo_width * scale, logo_height * scale,)
svg = logo.getroot()
svg.scale_xy(scale, scale)
scaled_logo.append(svg)
code=st.fromstring(a)
code.append(logo)
code.save('merged.svg')