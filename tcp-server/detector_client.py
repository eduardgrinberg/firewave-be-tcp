import json
from io import BytesIO

import requests as requests
import logging

class DetectorClient:
    def __init__(self):
        self.detector_url = "http://3.66.152.172:5000/upload"
        # self.detector_url = "http://localhost:5000/upload"


    def send_data(self,data: bytearray):
        file_obj = BytesIO(data)
        files = {'file_data': ('rec.raw', file_obj)}
        response = requests.post(self.detector_url, files=files)
        logging.info(response.content)

