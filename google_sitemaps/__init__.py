registry = {}


def register(**kwargs):
    for name, sitemap in kwargs.items():
        registry[name] = sitemap
