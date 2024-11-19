import easyocr
from PIL import Image

class _2frame_format:

    @staticmethod
    def setup_data():
        global reader
        reader = easyocr.Reader(['en'])

    @staticmethod
    def extract_data(image, frame):

        results = reader.readtext(image)  # extract text from an image

        for result in results:
            print(result[1])