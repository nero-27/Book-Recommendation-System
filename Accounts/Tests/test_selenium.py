# NUMBER OF TESTS = 3


import openpyxl
import unittest
from selenium import webdriver
import time


@classmethod
def setUpClass(cls):
    cls.driver = webdriver.Chrome('E:\Selenium\chromedriver.exe')
    cls.driver.get('http://127.0.0.1:8000/')
    cls.driver.maximize_window()

def test_search_by_book_name(self):
    self.driver.find_element_by_name('get_started').click()
    self.driver.find_element_by_name('Username').send_keys('richa')
    self.driver.find_element_by_name('Password').send_keys('richa1234')
    time.sleep(2)
    self.driver.find_element_by_name('SignIn').click()
    self.driver.find_element_by_name('search').send_keys('golden gate')
    time.sleep(2)
    self.driver.find_element_by_name('search_button').click()
    time.sleep(2)

def test_search_by_book_author(self):
    self.driver.find_element_by_name('get_started').click()
    self.driver.find_element_by_name('Username').send_keys('richa')
    self.driver.find_element_by_name('Password').send_keys('richa1234')
    time.sleep(2)
    self.driver.find_element_by_name('SignIn').click()
    self.driver.find_element_by_name('search').send_keys('john grisham')
    time.sleep(2)
    self.driver.find_element_by_name('search_button').click()
    time.sleep(2)

def test_rate_book_function(self):
    self.driver.get('http://127.0.0.1:8000/login/')
    self.driver.find_element_by_name('Username').send_keys('richa')
    self.driver.find_element_by_name('Password').send_keys('richa1234')
    time.sleep(2)
    self.driver.find_element_by_name('SignIn').click()
    time.sleep(2)
    self.driver.find_element_by_name('book_img').click()
    time.sleep(2)
    self.driver.find_element_by_name('rate_book').click()
    time.sleep(2)
    self.driver.find_element_by_name('rating_number').send_keys('8')
    time.sleep(2)
    self.driver.find_element_by_name('rate_it').click()
    time.sleep(2)
    self.driver.find_element_by_id('navbar-primary_dropdown_1').click()
    time.sleep(2)
    self.driver.find_element_by_name('profile').click()
    time.sleep(2)
    self.driver.find_element_by_name('brs').click()
    time.sleep(2)


@classmethod
def tearDownClass(cls):
    cls.driver.close()
    cls.driver.quit()
