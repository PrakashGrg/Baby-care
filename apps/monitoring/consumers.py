import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.detection.motion import MotionDetector
from apps.detection.models import MotionEvent
from apps.audio.cry_detector import CryDetector
from apps.audio.models import CryEvent
from apps.users.push import send_push_to_user


class MonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'monitor_{self.room_name}'
        self.motion_detector = MotionDetector()
        self.cry_detector = CryDetector()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected to monitor room {self.room_name}'
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get('type')

        if event_type == 'video_frame':
            await self.handle_video_frame(data)
        elif event_type == 'audio_chunk':
            await self.handle_audio_chunk(data)
        elif event_type == 'parent_voice':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'monitor_event',
                    'event': {
                        'type': 'parent_voice',
                        'audio': data.get('audio'),
                        'room': self.room_name,
                    }
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'monitor_event',
                    'event': data
                }
            )

    async def handle_video_frame(self, data):
        frame_b64 = data.get('frame')
        if not frame_b64:
            return

        result = self.motion_detector.detect(frame_b64)

        if result['motion_detected']:
            await self.save_motion_event(result['score'])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'monitor_event',
                    'event': {
                        'type': 'motion_alert',
                        'score': result['score'],
                        'intensity': result['intensity'],
                        'annotated_frame': result['annotated_frame'],
                        'room': self.room_name
                    }
                }
            )
            await database_sync_to_async(send_push_to_user)(
                self.scope['user'],
                'Motion detected',
                f'Motion in {self.room_name}',
                {'type': 'motion_alert', 'room': self.room_name},
            )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'monitor_event',
                'event': {
                    'type': 'frame_broadcast',
                    'frame': frame_b64,
                    'sender': self.channel_name,
                }
            }
        )

    async def handle_audio_chunk(self, data):
        audio_b64 = data.get('audio')
        client_loud = data.get('client_loud', False)

        if not audio_b64 and not client_loud:
            return

        result = (
            self.cry_detector.detect(audio_b64)
            if audio_b64
            else {'cry_detected': False, 'volume': 0}
        )

        if client_loud or result.get('cry_detected'):
            volume = result.get('volume') or 5000
            await self.save_cry_event(volume)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'monitor_event',
                    'event': {
                        'type': 'cry_alert',
                        'volume': volume,
                        'room': self.room_name
                    }
                }
            )
            await database_sync_to_async(send_push_to_user)(
                self.scope['user'],
                'Baby crying',
                f'Cry detected in {self.room_name}',
                {'type': 'cry_alert', 'room': self.room_name},
            )

    @database_sync_to_async
    def save_motion_event(self, score):
        MotionEvent.objects.create(
            user=self.scope['user'],
            room_name=self.room_name,
            motion_score=score
        )

    @database_sync_to_async
    def save_cry_event(self, volume):
        CryEvent.objects.create(
            user=self.scope['user'],
            room_name=self.room_name,
            volume_level=volume
        )

    async def monitor_event(self, event):
        payload = event['event']
        # Don't echo frames back to the camera (Child Mode) device
        if (
            payload.get('type') == 'frame_broadcast'
            and payload.get('sender') == self.channel_name
        ):
            return
        await self.send(text_data=json.dumps(payload))