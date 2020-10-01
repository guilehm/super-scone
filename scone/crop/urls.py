from django.conf.urls import url

from scone.crop import views

app_name = 'crop'


urlpatterns = [
    url(
        r'crop/'
        r'(?P<fit>smartcrop|cover|contain|fill|inside|outside)/'
        r'(?P<width>\d{1,4})x(?P<height>\d{1,4})/'
        r'(?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
        views.get_crop,
        name='get-crop'
    ),
    url(
        r'smartcrop/'
        r'(?P<width>\d{1,4})x(?P<height>\d{1,4})/'
        r'(?P<url>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
        views.get_smartcrop,
        name='get-smartcrop'
    ),
]
