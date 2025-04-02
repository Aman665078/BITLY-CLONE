import random
import logging
import redis
import string
from django.db import models
from django.core.validators import URLValidator
from django.contrib.auth import get_user_model
from django.utils.timezone import now

# Configure logging
logger = logging.getLogger(__name__)

User = get_user_model()

# Connect to Redis
db_cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_short_code(length=6):
    """Generate a unique short code using base62 encoding."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class ShortURL(models.Model):
    """Model to store original and shortened URLs."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    original_url = models.URLField(validators=[URLValidator()])
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    click_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)
        db_cache.set(self.short_code, self.original_url, ex=60*60*24*7)  # Cache for 7 days

    def is_expired(self):
        return self.expires_at and now() > self.expires_at

class ClickAnalytics(models.Model):
    """Track click analytics."""
    url = models.ForeignKey(ShortURL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)