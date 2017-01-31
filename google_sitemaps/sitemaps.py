from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from django.utils.html import strip_tags

import re


class GoogleSitemap(Sitemap):

    Type = 'News'

    def __strip_tags(self, text):
        single_quote = re.sub(r'(<i>)|(</i>)', "'", text, re.I)
        return strip_tags(single_quote)

    def genres(self, obj):
        """
        Returns a comma-separated list of properties characterizing the content of the article,
        such as "PressRelease" or "UserGenerated." Your content must be labeled accurately,
        in order to provide a consistent experience for our users.

        Options are:

            * PressRelease (default, visible): an official press release.
            * Satire (visible): an article which ridicules its subject for didactic purposes.
            * Blog (visible): any article published on a blog, or in a blog format.
            * OpEd: an opinion-based article which comes specifically from the Op-Ed section of your site.
            * Opinion: any other opinion-based article not appearing on an Op-Ed page, i.e., reviews, interviews, etc.
            * UserGenerated: newsworthy user-generated content which has already gone through a formal editorial review process on your site.
        """
        return 'PressRelease'

    def title(self, obj):
        """
        Returns the title of the news article.
        Note: The title may be truncated for space reasons when shown on Google News.
        """
        if hasattr(obj, 'short_title'):
            return self.__strip_tags(obj.short_title)
        elif hasattr(obj, 'title'):
            return self.__strip_tags(obj.title)
        elif hasattr(obj, 'name'):
            return self.__strip_tags(obj.name)
        elif hasattr(obj, 'headline'):
            return self.__strip_tags(obj.headline)

    def keywords(self, obj):
        """
        Returns a comma-separated list of keywords describing the topic of the article.
        Keywords may be drawn from, but are not limited to, the list of existing Google News keywords.
        """
        if hasattr(obj, 'keywords'):
            return obj.keywords

    def access(self, obj):
        """
        Returns description of the accessibility of the article.
        If the article is accessible to Google News readers without a registration or subscription,
        this function should return None

        Options are::

            * Subscription (visible): an article which prompts users to pay to view content.
            * Registration (visible): an article which prompts users to sign up for an unpaid account to view content.
        """

    def stock_tickers(self, obj):
        """
        Returns a comma-separated list of up to 5 stock tickers of the companies,
        mutual funds, or other financial entities that are the main subject of the article.
        Relevant primarily for business articles.
        Each ticker must be prefixed by the name of its stock exchange,
        and must match its entry in Google Finance.
        For example, "NASDAQ:AMAT" (but not "NASD:AMAT"), or "BOM:500325" (but not "BOM:RIL").
        """

    def pub_date(self, obj):
        """
        Returns the date in DATE/TIME format of the original posting of the object(Article/Video)
        """
        if getattr(obj, 'pub_date', None):
            return obj.pub_date
        elif getattr(obj, 'creation_date', None):
            return obj.creation_date

    def description(self, obj):
        """
        Checks the object to see if there is a short description element, and returns it,
        and if not returns the description of the object in string format.
        """
        if hasattr(obj, 'short_description'):
            return self.__strip_tags(obj.short_description)
        elif hasattr(obj, 'description'):
            return self.__strip_tags(obj.description)

    def content_loc(self, obj):
        """
        Returns the domain of the current site along with the actual path to the video file
        (As of now we don't have access to the actual video file so it instead links to the video landing page)

        Currently content location is not being used for the broadway project.
        """
        return Site.objects.get_current().domain + obj.get_absolute_url()

    def player_loc(self, obj):
        """
        Returns a link to the brightcove player using the external_id to get to the correct video.
        """
        location = 'http://players.brightcove.net/1372165866/rJCddKdV_default/index.html?videoId=%s' % (obj.external_id) \
                   if obj.external_id else ''
        return location

    def thumbnail_loc(self, obj):
        """
        Returns the location of the thumbnail for the video, using the thumbnail function in the Video class.
        """
        return obj.thumbnail

    def get_urls(self, page=1):
        from django.contrib.sites.models import Site
        domain = Site.objects.get_current().domain
        get = self._Sitemap__get
        for item in self.paginator.page(page).object_list:
            sitemapdict = {
                'location': "http://%s%s" % (domain, get('location', item)),
                'changefreq': get('changefreq', item, None),
                'priority': get('priority', item, None),
                'pub_date': get('pub_date', item, None),
            }
            if self.Type == 'News':
                # News Sitemap attrs
                sitemapdict.update({'title': get('title', item, None),
                                    'access': get('access', item, None),
                                    'keywords': get('keywords', item, None),
                                    'genres': get('genres', item, None),
                                    'stock_tickers': get('stock_tickers', item, None),
                                    })
            elif self.Type == 'Video':
                # Video Sitemap attrs
                sitemapdict.update({'title': get('title', item, None),
                                    'description': get('description', item, None),
                                    'thumbnail_loc': get('thumbnail_loc', item, None),
                                    'player_loc': get('player_loc', item, None),
                                    })
            yield sitemapdict
