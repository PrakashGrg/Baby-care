from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
)
from .models import PushToken


def send_push_to_user(user, title: str, body: str, data: dict | None = None):
    tokens = list(PushToken.objects.filter(user=user).values_list('token', flat=True))
    if not tokens:
        return

    messages = [
        PushMessage(
            to=token,
            title=title,
            body=body,
            data=data or {},
            sound='default',
            priority='high',
        )
        for token in tokens
    ]

    try:
        responses = PushClient().publish_multiple(messages)
    except PushServerError:
        return

    # Drop invalid tokens
    for token, resp in zip(tokens, responses):
        try:
            resp.validate_response()
        except DeviceNotRegisteredError:
            PushToken.objects.filter(token=token).delete()
        except Exception:
            pass