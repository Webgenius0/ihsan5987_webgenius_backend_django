from firebase_admin import messaging


# from project.firebase.firebase_init import *
def send_fcm_notification(token, title, body, data=None):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data=data or {}
        )
        response = messaging.send(message)
        print(f"Notification sent: {response}")
        return response
    except Exception as e:
        print(f"FCM Error: {e}")
        return None
