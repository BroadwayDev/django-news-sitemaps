from django.conf.urls import url

from google_sitemaps import registry

from . import views

urlpatterns = [
    url(r'^index\.xml$',
        views.index,
        {'sitemaps': registry},
        name='google_sitemaps_index'),

    url(r'^(?P<section>.+)\.xml',
        views.google_sitemap,
        {'sitemaps': registry},
        name='google_sitemaps_sitemap'),
]
