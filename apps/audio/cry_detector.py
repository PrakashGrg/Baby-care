import base64
import numpy as np


class CryDetector:
    """
    Energy-based detector. Works best with raw PCM, but also tolerates
    compressed audio bytes by falling back to byte-energy heuristics.
    """

    def __init__(self, volume_threshold=3000, sustained_chunks_required=2):
        self.volume_threshold = volume_threshold
        self.sustained_chunks_required = sustained_chunks_required
        self.consecutive_loud_chunks = 0

    def _decode_audio(self, base64_str):
        if not base64_str:
            return np.array([], dtype=np.int16)
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        try:
            audio_bytes = base64.b64decode(base64_str)
        except Exception:
            return np.array([], dtype=np.int16)

        # Prefer int16 PCM interpretation
        if len(audio_bytes) >= 2 and len(audio_bytes) % 2 == 0:
            return np.frombuffer(audio_bytes, dtype=np.int16)

        # Fallback: treat bytes as rough energy signal
        return np.frombuffer(audio_bytes, dtype=np.uint8).astype(np.int16) - 128

    def detect(self, base64_audio):
        audio = self._decode_audio(base64_audio)
        if audio.size == 0:
            return {'cry_detected': False, 'volume': 0.0}

        rms = float(np.sqrt(np.mean(audio.astype(np.float64) ** 2)))

        if rms >= self.volume_threshold:
            self.consecutive_loud_chunks += 1
        else:
            self.consecutive_loud_chunks = 0

        cry_detected = self.consecutive_loud_chunks >= self.sustained_chunks_required
        return {'cry_detected': cry_detected, 'volume': rms}