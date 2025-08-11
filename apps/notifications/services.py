from fcm_django.models import FCMDevice
from .models import Notification


def send_notification(sender, recipient, notification_type, message, related_post=None, related_comment=None):
    print(f"[SEND_NOTIFICATION] SENDER: {sender} ({type(sender)}), NAME: {getattr(sender, 'name', None)}")

    try:
        image_url = sender.profile.image_url if hasattr(sender, 'profile') else 'No profile'
    except Exception as e:
        image_url = f'Error accessing profile: {e}'

    print(f"[SEND_NOTIFICATION] IMAGE_URL: {image_url}")

    # Create a notification record in the database
    notification = Notification.objects.create(
        sender=sender,
        recipient=recipient,
        notification_type=notification_type,
        message=message,
        related_post=related_post,
        related_comment=related_comment
    )
    print("notification", notification)

    # Send the notification using FCM
    devices = FCMDevice.objects.filter(user=recipient, active=True)
    if devices.exists():
        devices.send_message(
            title=f"New {notification_type.capitalize()}", body=message,
            data={
                'notification_id': str(notification.id),
                'notification_type': notification_type,
                'related_post_id': related_post.id if related_post else None,
                'related_comment_id': related_comment.id if related_comment else None,
            }
        )


def send_system_notification(recipient, title, message, event_type):
    icon_key = event_type
    notification = Notification.objects.create(
        sender=None,
        recipient=recipient,
        category='system',
        notification_type='system',
        title=title,
        message=message,
        system_event=event_type,
        icon=icon_key
    )

    # Send to device if available
    devices = FCMDevice.objects.filter(user=recipient, active=True)
    if devices.exists():
        devices.send_message(
            title=title,
            body=message,
            data={'notification_id': str(notification.id), 'category': 'system'}
        )
