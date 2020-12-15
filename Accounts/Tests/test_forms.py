# NUMBER OF TESTS = 13


from django.test import TestCase, Client
from django.urls import reverse
from Accounts.models import Books, Users, Ratings, Overall_Ratings
from Upload.forms import login_form, registration_form
import templates

class TestForms(TestCase):
    @classmethod
    def SetUp(self):
        self.client = Client()
        self.homepage_url = reverse('homepage')
        self.login_url = reverse('loginpage')
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')
        self.description_url = reverse('description')

        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        self.short_password = {
            'Username': 'testuser',
            'Password': 'test',
            'Re_Password': 'test',
            'Age': '30'
        }
        self.unmatching_passwords = {
            'Username': 'testuser',
            'Password': 'testcase',
            'Re_Password': 'testca',
            'Age': '30'
        }
        self.same_user_pass = {
            'Username': 'testuser',
            'Password': 'testuser',
            'Re_Password': 'testuser',
            'Age': '30'
        }
        self.age_less_than_5 = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '4'
        }
        self.age_more_than_90 = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '95'
        }
        return super().SetUp()

class LoginTest(TestForms):

    def test_can_view_login_page_correctly(self):       # test works
        response = self.client.get(reverse('loginpage'))
        self.assertEqual(response.status_code, 200) #success code
        self.assertTemplateUsed(response, 'login.html')


    def test_login_of_registered_user(self):   # test works
        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        self.client.post(reverse('signup'), self.valid_user, format='text/html')
        user = Users.objects.filter(
            Username = self.valid_user['Username']
        ).first()
        user.is_active=True
        user.save()
        response = self.client.post(reverse('loginpage'), data={'Username': 'testuser', 'Password': 'secret'}, format='text/html')
        self.assertEqual(response.status_code, 302)  # check if redirected to homepage

    def test_login_with_incorrect_password(self): # test works
        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        user = Users.objects.create(
            Username=self.valid_user['Username'],
            Password=self.valid_user['Password'],
            Age=self.valid_user['Age']
        )
        user.is_active = True
        user.save()
        response = self.client.post(reverse('loginpage'), data={'Username': 'testuser', 'Password': 'password'}, format='text/html')
        self.assertEqual(response.status_code, 200)  # coz invalid leads to same page (may have to change)

    def test_user_doesnt_exist(self):   # test works
        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        user = Users.objects.create(
            Username=self.valid_user['Username'],
            Password=self.valid_user['Password'],
            Age=self.valid_user['Age']
        )
        user.is_active = True
        user.save()
        response = self.client.post(reverse('loginpage'), data={'Username': 'user', 'Password': 'password'}, format='text/html')
        self.assertEqual(response.status_code, 200)  # coz invalid leads to same page (may have to change)


class SignupTest(TestForms):

    def test_can_view_signup_page_correctly(self):         # test works
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200) #success code
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_form_valid_data(self):                  # test works
        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        form = registration_form(data=self.valid_user)
        self.assertTrue(form.is_valid())

    def test_unmatching_passwords(self):                    # test works
        self.unmatching_passwords = {
            'Username': 'testuser',
            'Password': 'testcase',
            'Re_Password': 'testca',
            'Age': '30'
        }
        form = registration_form(data=self.unmatching_passwords)
        self.assertFalse(form.is_valid())

    # def test_short_password(self):
    #     form = registration_form(data=self.short_password)
    #     self.assertFalse(form.is_valid())

    def test_user_already_exists(self):                 # test works
        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        signup_form = registration_form(data=self.valid_user)
        loginform = registration_form(data=self.valid_user)
        if signup_form == loginform:
            self.assertFalse(form.is_valid())

    def test_username_password_not_same(self):          # test works
        self.same_user_pass = {
            'Username': 'testuser',
            'Password': 'testuser',
            'Re_Password': 'testuser',
            'Age': '30'
        }


        form = registration_form(data=self.same_user_pass)
        self.assertFalse(form.is_valid())

    def test_age_less_than_5(self):                 # test works
        self.age_less_than_5 = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '4'
        }
        form = registration_form(data=self.age_less_than_5)
        self.assertFalse(form.is_valid())

    def test_age_more_than_90(self):                #test works
        self.age_more_than_90 = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '95'
        }
        form = registration_form(data=self.age_more_than_90)
        self.assertFalse(form.is_valid())

    # def test_registration_form_all_fields_required(self):
    #     form = registration_form(data={})
    #     self.assertIs(form.is_valid(), False)
    #     self.assertEquals(len(form.errors), 3) #all fields required

class integration_test(TestForms):

    def test_integration_login_module(self):
        response = self.client.get(reverse('loginpage'))
        self.assertEqual(response.status_code, 200)  # success code
        self.assertTemplateUsed(response, 'login.html')

        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        self.client.post(reverse('signup'), self.valid_user, format='text/html')
        user = Users.objects.filter(
            Username=self.valid_user['Username']
        ).first()
        user.is_active = True
        user.save()
        response = self.client.post(reverse('loginpage'), data={'Username': 'testuser', 'Password': 'secret'}, format='text/html')
        self.assertEqual(response.status_code, 302)  # check if redirected to homepage

        user = Users.objects.create(
            Username=self.valid_user['Username'],
            Password=self.valid_user['Password'],
            Age=self.valid_user['Age']
        )
        user.is_active = True
        user.save()
        response = self.client.post(reverse('loginpage'), data={'Username': 'user', 'Password': 'password'}, format='text/html')
        self.assertEqual(response.status_code, 200)  # coz invalid leads to same page (may have to change)


def test_integration_registration_module(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)  # success code
        self.assertTemplateUsed(response, 'signup.html')

        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        form = registration_form(data=self.valid_user)
        self.assertTrue(form.is_valid())

        self.unmatching_passwords = {
            'Username': 'testuser',
            'Password': 'testcase',
            'Re_Password': 'testca',
            'Age': '30'
        }
        form = registration_form(data=self.unmatching_passwords)
        self.assertFalse(form.is_valid())

        self.valid_user = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '30'
        }
        signup_form = registration_form(data=self.valid_user)
        loginform = registration_form(data=self.valid_user)
        if signup_form == loginform:
            self.assertFalse(form.is_valid())

        self.same_user_pass = {
            'Username': 'testuser',
            'Password': 'testuser',
            'Re_Password': 'testuser',
            'Age': '30'
        }

        form = registration_form(data=self.same_user_pass)
        self.assertFalse(form.is_valid())

        self.age_less_than_5 = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '4'
        }
        form = registration_form(data=self.age_less_than_5)
        self.assertFalse(form.is_valid())

        self.age_more_than_90 = {
            'Username': 'testuser',
            'Password': 'secret',
            'Re_Password': 'secret',
            'Age': '95'
        }
        form = registration_form(data=self.age_more_than_90)
        self.assertFalse(form.is_valid())
