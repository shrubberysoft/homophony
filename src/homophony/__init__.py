# Copyright (c) 2009 Gintautas Miliauskas, Adomas Paltanavicius
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import unittest
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import got_request_exception
import django.test._doctest as doctest
try:
    from lxml import etree
except ImportError:
    etree = None
import wsgi_intercept
import wsgi_intercept.mechanize_intercept
from wsgiref.simple_server import make_server
import webbrowser
import zc.testbrowser.browser


__all__ = ['Browser', 'DocFileSuite', 'BrowserTestCase']


class LoudWSGIHandler(WSGIHandler):
    """Extension of WSGIHandler that reraises exceptions without displaying
    the useless Django error page."""

    def __init__(self, *args, **kwargs):
        super(LoudWSGIHandler, self).__init__(*args, **kwargs)
        got_request_exception.connect(self.store_exc_info)

    def __call__(self, environ, start_response):
        self._stored = None
        # zc.testbrowser is serious about the robots exclusion standard,
        # but we don't want to pass these down to Django applications.
        if environ['PATH_INFO'] == '/robots.txt':
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return ["No robots.txt"]
        try:
            return super(LoudWSGIHandler, self).__call__(environ, start_response)
        finally:
            if self._stored is not None:
                raise self._stored[0], self._stored[1],self._stored[2]

    def store_exc_info(self, **kwargs):
        self._stored = sys.exc_info()


class Browser(zc.testbrowser.browser.Browser):
    """Extension of the Browser that interacts well with wsgi_intercept."""

    def __init__(self, *args, **kwargs):
        kwargs['mech_browser'] = wsgi_intercept.mechanize_intercept.Browser()
        browser = super(Browser, self).__init__(*args, **kwargs)

    def queryHTML(self, path):
        """Run an XPath query on the HTML document and print matches."""
        if etree is None:
            raise Exception("lxml not available")
        document = etree.HTML(self.contents)
        for node in document.xpath(path):
            if isinstance(node, basestring):
                print node
            else:
                print etree.tostring(node, pretty_print=True).strip()

    def serve(self):
        # Credit: Ignas Mikalajunas.
        # TODO: This setup does not serve static files.  It would be nice to
        # fire up a more complete publisher.
        try:
            print >> sys.stderr, 'Starting HTTP server on localhost:5001...'
            srv = make_server('localhost', 5001, LoudWSGIHandler())
            url = self.url.replace('http://testserver', 'http://localhost:5001')
            # We rely on the browser being slower to start than the server.
            print >> sys.stderr, 'Opening web browser: %s' % url
            webbrowser.open(url)
            srv.serve_forever()
        except KeyboardInterrupt:
            print >> sys.stderr, 'Stopped HTTP server.'


class BrowserTestCase(unittest.TestCase):
    """Base class for test cases that make use of the Browser."""

    def setUp(self):
        setUpBrowser()

    def tearDown(self):
        tearDownBrowser()


def DocFileSuite(*paths, **kwargs):
    """Extension of the standard DocFileSuite that sets up test browser for
    use in doctests."""
    kwargs.setdefault('setUp', setUpBrowser)
    kwargs.setdefault('tearDown', tearDownBrowser)
    kwargs.setdefault('globs', {}).update(Browser=Browser)
    kwargs.setdefault('optionflags', doctest.NORMALIZE_WHITESPACE |
                                     doctest.REPORT_ONLY_FIRST_FAILURE |
                                     doctest.ELLIPSIS)
    if 'package' not in kwargs:
        # Resolve relative names based on the caller's module
        kwargs['package'] = doctest._normalize_module(None)
        kwargs['module_relative'] = True
    return doctest.DocFileSuite(*paths, **kwargs)


def setUpBrowser(*args):
    wsgi_intercept.urllib2_intercept.install_opener()
    wsgi_intercept.add_wsgi_intercept('testserver', 80, LoudWSGIHandler)
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        from django.contrib.sites.models import Site
        Site.objects.get_current().domain = 'testserver'


def tearDownBrowser(*args):
    wsgi_intercept.remove_wsgi_intercept()
    wsgi_intercept.urllib2_intercept.uninstall_opener()
