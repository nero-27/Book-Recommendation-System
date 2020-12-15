# NUMBER OF TESTS = 5


from django.test import TestCase, Client
from django.urls import reverse
from Accounts.models import Books, Users, Ratings, Overall_Ratings
import templates

class TestViews(TestCase):

    def SetUp(self):
        self.client = Client()
        self.homepage_url = reverse('homepage')
        self.login_url = reverse('loginpage')
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')
        self.description_url = reverse('description')

        return super().SetUp()

class PageTests(TestViews):
    def test_can_view_get_started_page_correctly(self):         # test works
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)  # success code
        self.assertTemplateUsed(response, 'home.html')

    def test_can_view_description_page_correctly(self):         # test works
        response = self.client.get(reverse('description'))
        response2 = self.assertEqual(response.status_code, 302)  # redirecting to description page
        self.assertTemplateUsed(response2, 'detail.html')
        # self.assertRedirects(response, '', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_can_view_recs_page_correctly(self):         # test works
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

    def test_can_view_profile_page_correctly(self):             # test works
        response = self.client.get(reverse('profile'))
        response2 = self.assertEqual(response.status_code, 200)  # success code
        self.assertTemplateUsed(response2, 'profile.html')

    def test_logout_successful(self):                       # test works
        response = self.client.get(reverse('logout'))
        response2 = self.assertEqual(response.status_code, 200)  # success code
        self.assertTemplateUsed(response2, 'login.html')

