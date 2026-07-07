import base64
import numpy as np


class CryDetector:
    """
    Energy-based cry detector. Feed it base64-encoded raw PCM audio chunks
    (16-bit signed integers, mono). Detects sustained loud audio above
    a volume threshold, characteristic of crying/distress sounds.
    """

    def __init__(self, volume_threshold=3000, sustained_chunks_required=3):
        self.volume_threshold = volume_threshold
        self.sustained_chunks_required = sustained_chunks_required
        self.consecutive_loud_chunks = 0

    def _decode_audio(self, base64_str):
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        audio_bytes = base64.b64decode(base64_str)
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
        return audio_array

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