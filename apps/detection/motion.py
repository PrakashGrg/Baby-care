import cv2
import numpy as np
import base64
import time


class MotionDetector:
    """
    Frame-differencing motion detector with cooldown, intensity scoring,
    and annotated frame output (bounding boxes drawn around motion regions).
    """

    def __init__(self, threshold=25, min_area=500, cooldown_seconds=3):
        self.threshold = threshold
        self.min_area = min_area
        self.cooldown_seconds = cooldown_seconds
        self.previous_frame = None
        self.last_alert_time = 0

    def _decode_frame(self, base64_str):
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        img_bytes = base64.b64decode(base64_str)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return frame

    def _encode_frame(self, frame):
        success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        if not success:
            return None
        return base64.b64encode(buffer).decode('utf-8')

    def _classify_intensity(self, score):
        if score < 5000:
            return 'low'
        elif score < 50000:
            return 'medium'
        else:
            return 'high'

    def detect(self, base64_frame):
        frame = self._decode_frame(base64_frame)
        if frame is None:
            return {'motion_detected': False, 'score': 0.0, 'intensity': 'none', 'annotated_frame': None, 'on_cooldown': False}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None or self.previous_frame.shape != gray.shape:
            self.previous_frame = gray
            return {'motion_detected': False, 'score': 0.0, 'intensity': 'none', 'annotated_frame': None, 'on_cooldown': False}

        frame_delta = cv2.absdiff(self.previous_frame, gray)
        thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        total_area = 0
        boxes = []

        for contour in contours:
            area = cv2.contourArea(contour)
            total_area += area
            if area >= self.min_area:
                motion_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                boxes.append((x, y, w, h))

        self.previous_frame = gray

        now = time.time()
        on_cooldown = (now - self.last_alert_time) < self.cooldown_seconds

        annotated_frame = None
        if motion_detected and not on_cooldown:
            annotated = frame.copy()
            for (x, y, w, h) in boxes:
                cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
            annotated_frame = self._encode_frame(annotated)
            self.last_alert_time = now

        should_alert = motion_detected and not on_cooldown

        return {
            'motion_detected': should_alert,
            'score': float(total_area),
            'intensity': self._classify_intensity(total_area) if motion_detected else 'none',
            'annotated_frame': annotated_frame,
            'on_cooldown': motion_detected and on_cooldown,
        }