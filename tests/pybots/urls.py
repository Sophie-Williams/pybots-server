from pybots.urls import urls
from tests.test_case import TestCase


class TestUrls(TestCase):
    def test_urls(self):
        try:
            iter(urls)
        except TypeError:
            raise self.failureException('Urls is not iterable.')

        for url in urls:
            self.assertTrue(len(url) == 2, 'Url pattern and view.')
            self.assertTrue(callable(url[1]), 'Callable view in url')