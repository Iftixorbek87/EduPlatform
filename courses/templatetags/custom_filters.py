import re
from django import template

register = template.Library()

@register.filter
def extract_kinescope_id(url):
    """
    Extract Kinescope video ID from URL
    Example: 
    - Input: 'https://kinescope.io/embed/1a8b81de-197e-4d6c-9f2a-ae004934586a'
    - Output: '1a8b81de-197e-4d6c-9f2a-ae004934586a'
    """
    if not url:
        return ''
    
    # Try to extract ID from URL
    match = re.search(r'kinescope\.io/(?:embed/|player/)?([a-f0-9-]+)', url, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # If no match, return the original string (might already be an ID)
    return url
