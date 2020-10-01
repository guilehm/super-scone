import asyncio
from io import BytesIO

import httpx
from asgiref.sync import sync_to_async
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse, HttpResponseBadRequest

from scone.crop.models import Crop, Picture

ACCEPTED_IMAGE_CONTENT_TYPES = (
    'image/bmp',
    'image/jpeg',
    'image/png',
)

WIDTH_LIMIT = 3840
HEIGHT_LIMIT = 2160


async def get_crop(request, width, height, fit, url):
    if int(width) > WIDTH_LIMIT or int(height) > HEIGHT_LIMIT:
        return HttpResponseBadRequest()

    endpoint = f'{settings.CROP_API_ENDPOINT}/crop/'
    params = dict(
        url=url,
        width=width,
        height=height,
        fit=fit,
    )

    @sync_to_async
    def _get_or_create_picture():
        instance, _ = Picture.objects.get_or_create(uri=url)
        return instance

    @sync_to_async
    def _get_or_create_crop(original_picture):
        instance, _ = Crop.objects.get_or_create(
            original_picture=original_picture,
            width=width,
            height=height,
        )
        return instance

    @sync_to_async
    def _increment_request_count(instance):
        instance.request_count = F('request_count') + 1
        instance.save(update_fields=['request_count'])
        return instance

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(endpoint, params=params)
        try:
            response.raise_for_status()
        except (httpx.RequestError, httpx.HTTPStatusError):
            return HttpResponseBadRequest()
        image_io = BytesIO()
        async for chunk in response.aiter_bytes():
            image_io.write(chunk)
        image_io.seek(0)

    picture = await _get_or_create_picture()
    crop, *_ = await asyncio.gather(_get_or_create_crop(picture), _increment_request_count(picture))
    await _increment_request_count(crop)
    return HttpResponse(image_io.read(), content_type='image/png')
