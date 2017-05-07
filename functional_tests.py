from selenium import webdriver
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
        self.fail('Finish the test!')
        #The user should start on entering a to-do item as the first thing on the site

        #The user should be able to enter "Renew Driver's License" into a text box

        #Once the user hits enter, the page updates and displays the item in a list (i.e. "1: Renew Driver's License")

        #The user still has a text box that allows them to add another item. The user wants to enter "Do Laundry"

        #The page updates, and shows both items

        #The site creates a unique URL for the user for them to remember the list that they created

        #Visiting the unique URL will bring the user to their to-do list

        #After the user has finished interacting with the page, they close the page

if __name__ == '__main__':
    unittest.main(warnings='ignore')
