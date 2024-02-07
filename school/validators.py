import re
from django.core.exceptions import ValidationError


def validate_youtube_link(value):
    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/.+')
    if not youtube_pattern.match(value):
        raise ValidationError("Ссылка должна вести на YouTube.")
