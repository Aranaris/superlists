from django.test import LiveServerTestCase
from selenium import webdriver
from contextlib import contextmanager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
import unittest

class newVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
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
        
        #Once the user hits enter, the page updates and displays the item in a list (i.e. "1: Renew Driver's License")
        inputbox.send_keys(Keys.ENTER) 
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Renew Driver\'s License')
        #The user still has a text box that allows them to add another item. The user wants to enter "Do Laundry"
        inputbox = self.browser.find_element_by_id('id_new_item')
        
        inputbox.send_keys('Do Laundry')
        inputbox.send_keys(Keys.ENTER)

        #The page updates, and shows both items)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Renew Driver\'s License')
            self.check_for_row_in_list_table('2: Do Laundry')

        #The site creates a unique URL for the user for them to remember the list that they created
        self.fail('Finish the test!')
        #Visiting the unique URL will bring the user to their to-do list

        #After the user has finished interacting with the page, they close the page

