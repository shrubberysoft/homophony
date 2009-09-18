"""Example tests using homophony."""

import unittest
import doctest
from homophony import BrowserTestCase, Browser, DocFileSuite

class FoobarTestCase(BrowserTestCase):

    def testHome(self):
        browser = Browser()
        browser.open('http://testserver')
        browser.getControl(name='first_name').value = 'Jim'
        browser.getForm().submit()
        self.assertEquals(browser.url, 'http://testserver/hello')
        self.assertEquals(browser.title, 'Hello Jim')
        browser.getLink('Go back').click()
        self.assertEquals(browser.title, 'Home')


def suite():
    # We want to show that both unit tests and doctests are working
    suite = unittest.TestSuite()
    suite.addTest(FoobarTestCase('testHome'))
    suite.addTest(DocFileSuite('tests.txt',
                                optionflags=doctest.NORMALIZE_WHITESPACE |
                                            doctest.REPORT_ONLY_FIRST_FAILURE |
                                            doctest.ELLIPSIS))
    return suite
