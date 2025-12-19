from django import template

register = template.Library()

@register.filter
def get_video_id(url):
    """Extract video ID from Kinescope URL or return the original string"""
    if not url:
        return ''
    
    # If it's already just an ID
    if len(url) == 22 and '/' not in url and ' ' not in url:
        return url
        
    # Extract ID from URL
    parts = url.split('/')
    for part in reversed(parts):
        if part and ' ' not in part and len(part) >= 22:
            return part[-22:]  # Return last 22 characters (Kinescope ID length)
    return url
