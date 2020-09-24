from django.conf.urls import url

from scone.crop import views

app_name = 'crop'

urlpatterns = [
    url(r'crop/(?P<width>\d{1,4})x(?P<height>\d{1,4})/(?P<url>(.*))', views.simple_crop, name='simple-crop'),
]
