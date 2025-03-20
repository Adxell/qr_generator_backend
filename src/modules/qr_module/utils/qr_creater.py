import io
import qrcode
from PIL import Image
import base64 

class QRcreater: 
    "Tool for creation QR to personalize styles"
    @staticmethod
    def generate_qr(data: str, color: str): 
        """
        Generate a QR code with a custom color.
        
        :param data: Texto or URL to encode in the QR
        :param color: QR color with HEX format or color name (ie. 'blue', '#FF5733')
        """
        qr = qrcode.QRCode(
            version=1,  
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        buf = io.BytesIO()

        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=color, back_color="white")
        img.save(buf, format="PNG")
        base64_image = base64.b64encode(buf.getvalue()).decode("utf-8")
        return base64_image