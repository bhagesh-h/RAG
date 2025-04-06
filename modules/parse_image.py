import base64
from PIL import Image
from io import BytesIO

class parseImage:
    """
    A class to parse an image and convert it to a base64 string.
    """
    def __init__(self, image, format="JPEG"):
        self.image  = image
        self.format = format
    
    def tob64(self):
        buffered    = BytesIO()
        pil_image   = Image.open(self.image)
        pil_image.save(buffered, format=self.format)
        img_str     = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
    
    def toHTML(self):
        return f'<img src="data:image/jpeg;base64,{self.tob64()}" />'