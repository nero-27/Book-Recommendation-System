# NUMBER OF TESTS = 8


from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Accounts.views import homepage, loginpage, signup, logout, profile
from Search.views import searchn
from Rate.views import rate
from Description.views import description

class TestUrls(SimpleTestCase): #class inherits from SimpleTestCase (inbuilt class in django testing)

    def test_homepage_url_is_resolved(self):        # test works
        url = reverse('homepage')
        print(resolve(url))
        self.assertEquals(resolve(url).func, homepage)

    def test_signup_url_is_resolved(self):          # test works
        url = reverse('signup')
        print(resolve(url))
        self.assertEquals(resolve(url).func, signup)

    def test_loginpage_url_is_resolved(self):       # test works
        url = reverse('loginpage')
        print(resolve(url))
        self.assertEquals(resolve(url).func, loginpage)

    def test_logout_url_is_resolved(self):          # test works
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout)

    def test_profile_url_is_resolved(self):         # test works
        url = reverse('profile')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, profile)

    def test_searchn_url_is_resolved(self):         # test works
        url = reverse('searchn')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, searchn)

    def test_rate_url_is_resolved(self):            # test works
        url = reverse('rate')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, rate)

    def test_description_url_is_resolved(self):     # test works
        url = reverse('description')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, description)

