import cv2
import numpy as np
import base64


class MotionDetector:
    """
    Frame-differencing motion detector.
    Feed it consecutive frames (base64-encoded JPEG/PNG strings);
    it returns whether meaningful motion was detected between them.
    """

    def __init__(self, threshold=25, min_area=500):
        self.threshold = threshold
        self.min_area = min_area
        self.previous_frame = None

    def _decode_frame(self, base64_str):
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        img_bytes = base64.b64decode(base64_str)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return frame

    def detect(self, base64_frame):
        frame = self._decode_frame(base64_frame)
        if frame is None:
            return {'motion_detected': False, 'score': 0.0}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray
            return {'motion_detected': False, 'score': 0.0}

        frame_delta = cv2.absdiff(self.previous_frame, gray)
        thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        total_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            total_area += area
            if area >= self.min_area:
                motion_detected = True

        self.previous_frame = gray

        return {'motion_detected': motion_detected, 'score': float(total_area)}