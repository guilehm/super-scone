from io import BytesIO

import httpx
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files import File
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
    return HttpResponse(image_io.read(), status=response.status_code, content_type='image/png')


async def simple_crop(request, width, height, url):
    def _get_or_create_picture(uri):
        return Picture.objects.get_or_create(uri=uri)

    picture, created = await sync_to_async(_get_or_create_picture, thread_sensitive=True)(uri=url)

    def _get_or_create_crop(original_picture, _width, _height):
        return Crop.objects.get_or_create(
            original_picture=original_picture,
            width=_width,
            height=_height,
        )

    crop, _ = await sync_to_async(_get_or_create_crop, thread_sensitive=True)(
        original_picture=picture,
        _width=width,
        _height=height,
    )

    if crop.image:
        return HttpResponse(crop.image.read(), content_type='image/png')

    if created:
        image_io = BytesIO()
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream('GET', url) as response:
                    response.raise_for_status()
                    content_type = response.headers['content-type']
                    if content_type not in ACCEPTED_IMAGE_CONTENT_TYPES:
                        raise TypeError(f'The content-type {content_type} is not supported.')
                    async for chunk in response.aiter_bytes():
                        image_io.write(chunk)
                    await sync_to_async(picture.image.save, thread_sensitive=True)(
                        name=url.rsplit('/')[-1],
                        content=File(image_io)
                    )
            except (httpx.RequestError, TypeError):
                return HttpResponseBadRequest()
            except httpx.HTTPStatusError:
                return HttpResponse(status=response.status_code)

    return HttpResponse(picture.image.read(), content_type='image/png')
