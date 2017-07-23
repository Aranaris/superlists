import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from contextlib import contextmanager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
import unittest

class newVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    #use the wait_for_page_load function when we need to tell selenium to 
    #wait for a click to load/reload a page
    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        yield WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )
    
    def test_layout_and_styling(self):
        #The user goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #The user notices that the input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] / 2,
                512,
                delta=6
                )
        
        #The user starts a new list and sees that the input box remains center aligned
        inputbox.send_keys('testing styling')
        inputbox.send_keys(u'\ue007')
        with self.wait_for_page_load(timeout=10):
            inputbox = self.browser.find_element_by_id('id_new_item')
            self.assertAlmostEqual(
                    inputbox.location['x'] + inputbox.size['width'] / 2,
                    512,
                    delta = 6
                    )


    def test_can_start_a_list_and_retrieve_it_later(self):
        #User opens the homepage of the app
        self.browser.get(self.live_server_url)

        #The app should indicate that it is meant for creating to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        #The user should start on entering a to-do item as the first thing on the site
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
                )

        #The user should be able to enter "Renew Driver's License" into a text box
        inputbox.send_keys('Renew Driver\'s License')
        
        #Once the user hits enter, they are taken to a new URL, 
        #and the page updates and displays the item in a list (i.e. "1: Renew Driver's License")
        inputbox.send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            vince_list_url = self.browser.current_url
            self.assertRegex(vince_list_url, '/lists/.+') 
            self.check_for_row_in_list_table('1: Renew Driver\'s License')
        #The user still has a text box that allows them to add another item. The user wants to enter "Do Laundry"
            inputbox = self.browser.find_element_by_id('id_new_item')
        
            inputbox.send_keys('Do Laundry')
            inputbox.send_keys(Keys.ENTER)

        #The page updates, and shows both items
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Renew Driver\'s License')
            self.check_for_row_in_list_table('2: Do Laundry')

        #A new user, CS, comes to the site

        ##We use a new browser session to make sure Vince's information comes in
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #CS visits the homepage. She doesn't see Vince's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Renew Driver\'s License', page_text)
        self.assertNotIn('Do Laundry', page_text)

        #CS starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Call mom')
        inputbox.send_keys(Keys.ENTER)

        #The site creates a unique URL for CS 
        with self.wait_for_page_load(timeout=10):
            cs_list_url = self.browser.current_url
            self.assertRegex(cs_list_url, '/lists/.+')
            self.assertNotEqual(cs_list_url, vince_list_url)
        
        #There's still no trace of Vince's list
            page_text = self.browser.find_element_by_tag_name('body').text
            self.assertNotIn('Renew Driver\'s License', page_text)
            self.assertNotIn('Do Laundry', page_text)
        
        
        #Visiting the unique URL will bring the user to their to-do list
        self.browser.get(vince_list_url)

        self.check_for_row_in_list_table('1: Renew Driver\'s License')
        self.check_for_row_in_list_table('2: Do Laundry')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Call mom', page_text)

        
        #After the user has finished interacting with the page, they close the page
        self.browser.quit()
