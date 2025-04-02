from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from .models import ShortURL
from .serializers import ShortURLSerializer
from .task import track_click

def redirect_short_url(request, short_code):
    original_url = db_cache.get(short_code)
    if not original_url:
        url_object = get_object_or_404(ShortURL, short_code=short_code)
        if url_object.is_expired():
            return Response({"error": "URL expired"}, status=status.HTTP_410_GONE)
        original_url = url_object.original_url
        db_cache.set(short_code, original_url, ex=60*60*24*7)
        url_object.click_count += 1
        url_object.save()
        track_click.delay(url_object.id, request.META.get('REMOTE_ADDR'), request.META.get('HTTP_USER_AGENT'))
    return redirect(original_url)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_short_url(request):
    serializer = ShortURLSerializer(data=request.data)
    if serializer.is_valid():
        short_url = serializer.save(user=request.user)
        return Response({"short_url": f"{settings.SITE_DOMAIN}/{short_url.short_code}"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
