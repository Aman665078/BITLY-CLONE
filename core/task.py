from celery import shared_task
from .models import ShortURL
import logging
logger = logging.getLogger(__name__)
@shared_task
def track_click(url_id, ip_address, user_agent):
    try:
        url = ShortURL.objects.get(id=url_id)
        url.click_count += 1
        url.save()
    except Exception as e:
        logger.error(f"Error tracking click: {e}")
