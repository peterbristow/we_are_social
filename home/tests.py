"""
NOTES
The main things you can do to think of tests to perform are to look at your system and ask:
    What should happen when this succeeds?
    What should happen when this fails?
    Are there any if or elses that need special conditions to be tested?

unittest.TestCase class, the most basic test class. It provides these assert functions to check if the values were
equal or not equal, in addition to a few others.
More advanced classes:
    django.test.SimpleTestCase - Provides assert functions for checking form field validation, HTML assert functions, and
        also loads in your Django settings.py.
    django.test.TestCase - Loads in fixtures into a the testing database before running tests. Creates a 'Test Client'
        called self.client, which can be used to fetch web pages and resolve urls. Adds in various additional Django
        specific asserts.
    django.test.TransactionTestCase - Loads in fixtures into the testing database before running tests. Creates a
        'Test Client' called self.client which can be used to fetch web pages and resolve urls. Adds in various
        additional Django specific asserts. Additionally allows for testing database transactions and automatically
        resets your database at the end of the test run.
    django.test.LiveServerTest - Does the same thing as TransactionTestCase, but also starts a proper webserver when
        performing testing instead of the 'Test Client'.

How to load test data with fixtures:
    How to dump the data out of the development database.
        mkdir threads/fixtures
        python manage.py dumpdata --indent 4 threads > threads/fixtures/subjects.json
    To tell the test class to load that file, we add the following:
        class HomePageTest(TestCase):
            fixtures = ['subjects']

One-off objects: The 'setUp' method. Like this:
    from accounts.models import User
    class HomePageTest(TestCase):

        def setUp(self):
            super(HomePageTest, self).setUp()
            self.user = User.objects.create(username='testuser')
            self.user.set_password('letmein')
            self.user.save()
            self.login = self.client.login(username='testuser',
                                           password='letmein')
            self.assertEqual(self.login, True)

        ...

        def test_check_content_is_correct(self):
            home_page = self.client.get('/')
            self.assertTemplateUsed(home_page, "index.html")
            home_page_template_output = render_to_response("index.html", {'user':self.user}).content
            self.assertEquals(home_page.content, home_page_template_output)

Testing Models:  (Also test all IF statements)

Testing Forms:
    Things to test for:
        Does it validate properly when correct data is supplied?
        Does it validate properly when incorrect supplied data?
        Does the form clean properly?
"""
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from django.test import TestCase

from home.views import get_index


# Testing URLs
# TestCase class enables a testing web server.
class HomePageTest(TestCase):
    def test_home_page_resolvers(self):
        # Use resolve() to feed in the URL for the home page.
        # This gives us the internal representation of the home page and also
        # a handle to the function that would be used to process the request
        # in the home_page.func member variable.
        home_page = resolve('/')
        # So then we make sure that when we call that function, it matches
        # the view function we have declared in our views.py.
        # If it doesnt match, then there's something wrong with our urls.py
        # file that needs fixing!
        self.assertEqual(home_page.func, get_index)  # (url, function)

    # Testing Views
    # Things that could be checked are:
    # Does it return the correct status code?
    # Does it return the right content?
    # Does it use the correct template?
    # Does it show the correct success/fail messages?
    def test_home_page_status_code_is_ok(self):
        # self.client, which is used to visit the url in our test web server and
        # grab the content and HTTP headers, etc.
        # Returns a Python object back containing all the information relating
        # to what happened when it visited the URL.
        home_page = self.client.get('/')
        # Check the status_code, so that we can be certain that the page returns
        # the actual page and not a 404 or 500 error page.
        self.assertEquals(home_page.status_code, 200)

    # Testing Views
    # Do checks on the content and the template that was used:
    def test_check_content_is_correct(self):
        home_page = self.client.get('/')
        # By passing in the home_page response object and the name of the template
        # we can check if the correct template was used.
        # This protects against changing to an incorrect template.
        self.assertTemplateUsed(home_page, "index.html")

        # Check that the output of the template from the URL
        # (using self.client.get('/')) is the same as what we expect when we
        # use render_to_response to directly render its output locally. This
        # ensures that there are no extra stages affecting our page
        # rendering without us knowing about it.
        home_page_template_output = render_to_response("index.html").content
        self.assertEquals(home_page.content, home_page_template_output)
