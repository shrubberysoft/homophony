-----
Tests
-----

This is an example Django application with a bunch of tests that are powered
by **homophony**.

The tests use ``zc.buildout`` for dependency management.  To run the tests::

    $ python bootstrap.py
    $ bin/buildout
    $ bin/sample test -v 1 website
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
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.090s
    
    OK
    Destroying test database...
