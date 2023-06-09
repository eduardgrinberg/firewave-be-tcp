import threading
import logging

import detector_client
from settings import Settings


class DataCollector:
    def __init__(self, device_id):
        self.segment_lengths_bytes = Settings.bytes_per_sample * Settings.sample_rate * Settings.segment_length_sec
        self.data = bytearray()
        self.data_lock = threading.Lock()
        self.detector_client = detector_client.DetectorClient()
        self.device_id = device_id

    def add_data(self, data: bytearray):
        try:
            # logging.debug(f'Received data {len(data)}. Total data {len(self.data)}')
            self.data_lock.acquire()
            self.data += data
            if len(self.data) >= self.segment_lengths_bytes:
                # print('Segment Received')
                logging.debug(f'{self.device_id} - Segment Received')
                data_copy = self.data
                self.data = bytearray()
                threading.Thread(target=self.send_data, args=(data_copy,), daemon=True).start()

        finally:
            self.data_lock.release()

    def send_data(self, data):
        self.detector_client.send_data(data, self.device_id)
