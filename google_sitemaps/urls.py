from django.conf.urls import *

from google_sitemaps import registry
from buzz.sitemap import BuzzNewsSiteMap
from videos.sitemap import VideoGoogleSiteMap


urlpatterns = patterns('google_sitemaps.views',

	url(r'^index\.xml$',
        'index',
        {'sitemaps': registry},
        name='google_sitemaps_index'),

    url(r'^(?P<section>.+)\.xml',
        'google_sitemap',
        {'sitemaps': registry},
        name='google_sitemaps_sitemap'),
)
