-----
About
-----

**homophony** provides ``zc.testbrowser`` integration for Django;
``zc.testbrowser`` is a lot more robust than the default functional testing
client that comes with Django.

See the introduction_ to ``zc.testbrowser`` for a better understanding
of how powerful it is.

.. _introduction: http://pypi.python.org/pypi/zc.testbrowser/1.0a1


---------------
Using homophony
---------------

First of all, you need to have **homophony** installed; for your convenience,
recent versions should be available from PyPI.

Let's say you're working on an application called ``foobar``; the tests for
this application are located in ``foobar/tests.py``.


Unit tests
==========

Use this as a starting point for ``foobar/tests.py``::

    from homophony import BrowserTestCase, Browser

    class FoobarTestCase(BrowserTestCase):

        def testHome(self):
            browser = Browser()
            browser.open('http://testserver')
            browser.getControl(name='first_name').value = 'Jim'
            browser.getForm().submit()
            self.assertEquals(browser.url, 'http://testserver/hello')
            self.assertEquals(browser.title, 'Hello Jim')


Bear in mind that implementing custom ``setUp`` and ``tearDown`` methods
should involve calling those defined in ``BrowserTestCase``.


Doctests
========

If you prefer doctests over unit tests (as we do!), use the following as a base
for ``foobar/tests.py``::

    from homophony import DocFileSuite

    def suite():
        return DocFileSuite('tests.txt')


And here is an example ``foobar/tests.txt`` file::

    The website welcomes its visitors with a form:

        >>> browser = Browser()
        >>> browser.open('http://testserver')
        >>> browser.getControl(name='first_name').value = 'Jim'
        >>> browser.getForm().submit()

    When a name is given, it echoes back with an informal greeting:

        >>> browser.title
        'Hello Jim'
        >>> print browser.contents
        <!DOCTYPE html>
        ...
        <h1>Hello Jim</h1>
        ...

    And there is a link to go back:

        >>> browser.getLink('Go back').click()
        >>> browser.title
        'Home'


Helpers
=======

There are some useful helpers on the browser class.  You can run **XPath** queries
on HTML documents using ``queryHTML``, like this:

    >>> browser.queryHTML('//h1')
    <h1>Hello Jim</h1>

When debugging tests, it is sometimes handy to open a browser at a particular
point in the test.  You can accomplish that by invoking ``serve``:

    >>> browser.serve()

This command will start an HTTP server and open a web browser with live access
to your application.  Use Ctrl-C to stop the server and continue running tests.

There is a known issue that the mini-webserver does not serve static files, so
your browser may not be able to access Javascript or CSS used by your app.


Example application
===================

There is an example Django application in the source distribution.  Let's
run the tests::

    wormhole:example admp$ ./manage.py test -v 2 website
    Creating test database...
    Creating table auth_permission
    Creating table auth_group
    Creating table auth_user
    Creating table auth_message
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Installing index for auth.Permission model
    Installing index for auth.Message model
    ...
    testHome (example.website.tests.FoobarTestCase) ... ok
    Doctest: tests.txt ... ok

    ----------------------------------------------------------------------
    Ran 2 tests in 0.102s

    OK
    Destroying test database...

The ``-v 2`` parameter is there to get the list of tests printed, and is otherwise
unnecessary.

For learning purposes, try to break the tests and witness the details in the
output of the test runner.


-----------------
How does it work?
-----------------

Custom hooks are installed for ``urllib`` to pass all requests for
``http://testserver`` to a subclass of ``WSGIHandler`` (which
exposes Django applications through WSGI_). The real heavy lifting is
performed by ``wsgi_intercept``.

.. _WSGI: http://www.wsgi.org/

--------
Feedback
--------

There is a `home page <http://github.com/shrubberysoft/homophony>`_ with
instructions on how to access the code repository.

Send feedback and suggestions to team@shrubberysoft.com.
