import json
from io import BytesIO

import requests as requests
import logging


class DetectorClient:
    def __init__(self):
        self.detector_url = "http://3.66.152.172:5000/upload"
        # self.detector_url = "http://localhost:5000/upload"

    def send_data(self, data: bytearray, device_id):
        logging.info('sending ' + str(device_id))
        file_obj = BytesIO(data)
        files = {'file_data': ('rec.raw', file_obj)}
        data = {'device_id': device_id}
        response = requests.post(self.detector_url, files=files, data=data)
        logging.info(response.content)
