from django import forms
from django.conf import settings
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from django.test import TestCase

from accounts.views import login, register, profile
from .forms import UserRegistrationForm
from .models import User


class LoginPageTest(TestCase):
    # Testing URL
    def test_login_page_resolvers(self):
        # Use resolve() to feed in the URL for the home page.
        login_page = resolve('/login/')
        self.assertEqual(login_page.func, login)  # (url, function)

    # Testing View
    # Check page was delivered successfully.
    def test_login_page_status_code_is_ok(self):
        # self.client, which is used to visit the url in our test web server and
        # grab the content and HTTP headers, etc.
        login_page = self.client.get('/')
        self.assertEquals(login_page.status_code, 200)

    # Testing View
    # Do checks on the content and the template that was used:
    def test_check_content_is_correct(self):
        login_page = self.client.get('/login/')
        self.assertTemplateUsed(login_page, "login.html")
        login_page_template_output = render_to_response("login.html").content
        self.assertEquals(login_page.content, login_page_template_output)


class RegisterPageTest(TestCase):
    # Testing URL
    def test_register_page_resolvers(self):
        # Use resolve() to feed in the URL for the home page.
        register_page = resolve('/register/')
        self.assertEqual(register_page.func, register)  # (url, function)

    # Testing View
    # Check page was delivered successfully.
    def test_register_page_status_code_is_ok(self):
        # self.client, which is used to visit the url in our test web server and
        # grab the content and HTTP headers, etc.
        register_page = self.client.get('/register/')
        self.assertEquals(register_page.status_code, 200)

    # Testing View
    # Do checks on the content and the template that was used:
    def test_check_content_is_correct(self):
        register_page = self.client.get('/register/')
        self.assertTemplateUsed(register_page, "register.html")
        # register_page_template_output = render_to_response("register.html").content
        # self.assertEquals(register_page.content, register_page_template_output)


class ProfilePageTest(TestCase):
    # Testing URL
    def test_profile_page_resolvers(self):
        profile_page = resolve('/profile/')
        self.assertEqual(profile_page.func, profile)  # (url, function)

    # Testing View
    # Check page was delivered successfully.
    def test_profile_page_status_code_is_ok(self):
        profile_page = self.client.get('/profile/')
        self.assertEquals(profile_page.status_code, 200)

    # Testing View
    # Do checks on the content and the template that was used:
    def test_check_content_is_correct(self):
        profile_page = self.client.get('/profile/')
        self.assertTemplateUsed(profile_page, "profile.html")
        # profile_page_template_output = render_to_response("profile.html").content
        # self.assertEquals(profile_page.content, profile_page_template_output)


class CustomUserTest(TestCase):
    # Testing IF
    def test_manager_create(self):
        """
        Supply a set of data to _create_user that would cause the 'if not email'
        clause to succeed and fail, to ensure it works in both directions so
        to speak.
        So for this case, our failure would be a ValueError exception that we
        can trap in our test.
        """
        user = User.objects._create_user(None, "test@test.com", "password", False, False)
        self.assertIsNotNone(user)

        with self.assertRaises(ValueError):
            user = User.objects._create_user(None, None, "password", False, False)

    # Testing forms
    def test_registration_form(self):
        """
        Check the validation works for unfilled form fields with a simple test
        to see if correct data works:
        """
        form = UserRegistrationForm({
            'email': 'test@test.com',
            'password1': 'letmein1',
            'password2': 'letmein1',
            'stripe_id': settings.STRIPE_SECRET,
            'credit_card_number': 4242424242424242,
            'cvv': 123,
            'expiry_month': 1,
            'expiry_year': 2033
        })

        self.assertTrue(form.is_valid())

    # Testing forms
    def test_registration_form_fails_with_missing_email(self):
        """
        Test with a missing value, email in this case.
        """
        form = UserRegistrationForm({
            'password1': 'letmein1',
            'password2': 'letmein1',
            'stripe_id': settings.STRIPE_SECRET,
            'credit_card_number': 4242424242424242,
            'cvv': 123,
            'expiry_month': 1,
            'expiry_year': 2033
        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Please enter your email address",
                                 form.full_clean())

    # Testing forms
    def test_registration_form_fails_with_missing_password1(self):
        """
        Test with a missing value, password1 in this case.
        """
        form = UserRegistrationForm({
            'email': 'test@test.com',
            'password2': 'letmein1',
            'stripe_id': settings.STRIPE_SECRET,
            'credit_card_number': 4242424242424242,
            'cvv': 123,
            'expiry_month': 1,
            'expiry_year': 2033
        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Passwords do not match",
                                 form.full_clean())

    # Testing forms
    def test_registration_form_fails_with_missing_password2(self):
        """
        Test with a missing value, password2 in this case.
        """
        form = UserRegistrationForm({
            'email': 'test@test.com',
            'password1': 'letmein1',
            'stripe_id': settings.STRIPE_SECRET,
            'credit_card_number': 4242424242424242,
            'cvv': 123,
            'expiry_month': 1,
            'expiry_year': 2033
        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Passwords do not match",
                                 form.full_clean())

    # Testing forms
    def test_registration_form_fails_when_passwords_that_dont_match(self):
        form = UserRegistrationForm({
            'email': 'test@test.com',
            'password1': 'letmein1',
            'password2': 'letmein3',
            'stripe_id': settings.STRIPE_SECRET,
            'credit_card_number': 4242424242424242,
            'cvv': 123,
            'expiry_month': 1,
            'expiry_year': 2033
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 "Passwords do not match",
                                 form.full_clean())
