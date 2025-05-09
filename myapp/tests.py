from django.test import TestCase

# Create your tests here.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class MyAppTests(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=r"D:\学术交流论坛\.venv\Scripts\msedgedriver.exe")
