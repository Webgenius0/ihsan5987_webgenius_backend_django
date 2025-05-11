from datetime import datetime, timedelta

def human_readable_time(dt):
    now = datetime.now(dt.tzinfo)
    delta = now - dt

    if delta < timedelta(minutes=1):
        return "Just now"
    elif delta < timedelta(hours=1):
        return f"{int(delta.total_seconds() // 60)} minutes ago"
    elif dt.date() == now.date():
        return dt.strftime("%I:%M %p")  # Today, show time
    elif dt.date() == (now - timedelta(days=1)).date():
        return "Yesterday"
    elif delta < timedelta(days=7):
        return f"{delta.days} days ago"
    else:
        return dt.strftime("%b %d, %Y %I:%M %p")
