from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class newVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #User opens the homepage of the app
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Renew Driver\'s License' for row in rows)
        )

        #The user still has a text box that allows them to add another item. The user wants to enter "Do Laundry"
        self.fail('Finish the test!')

        #The page updates, and shows both items

        #The site creates a unique URL for the user for them to remember the list that they created

        #Visiting the unique URL will bring the user to their to-do list

        #After the user has finished interacting with the page, they close the page

if __name__ == '__main__':
    unittest.main(warnings='ignore')
