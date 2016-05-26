from django.test import TestCase
from django.shortcuts import render_to_response
from .models import Subject


# Testing views
class SubjectPageTest(TestCase):
    """
    Like the 'render' function used in view functions, render_to_response
    can take arguments to render other pages like the forums subjects or threads.
    So when rendering this view, we need to supply this test with some
    subjects like the real view would have - or else our template would fail
    to render.
    """
    def test_check_content_is_correct(self):
        subject_page = self.client.get('/forum/')
        self.assertTemplateUsed(subject_page, "forum/forum.html")
        subject_page_template_output = render_to_response("forum/forum.html",
                                                          {'subjects': Subject.objects.all()}).content
        self.assertEquals(subject_page.content, subject_page_template_output)
