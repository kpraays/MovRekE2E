import unittest
import app
import json

class AppTestCase(unittest.TestCase):
    def test_home_endpoint(self):
        response = app.welcome_return()
        self.assertEqual(response, {'Welcome': 'This is the stable API'})
        # self.assertEqual(response.status_code, 200)
        # self.assertIn('Welcome', data)

    def test_valid_user_recommend_route(self):
        user_id = 3  # valid user ID
        API_response = app.get_user_details(user_id)

        self.assertEqual(API_response['user_id'],3)
        self.assertEqual(API_response['age'],29)
        self.assertEqual(API_response['occupation'],'scientist')
        self.assertEqual(API_response['gender'],'M')

    def test_invalid_user_recommend_route(self):
        user_id = '99999999999999'  # An invalid user ID
        API_response = app.get_user_details(user_id)
        self.assertEqual(API_response,"Response not successful")

    def test_invalid_input(self):
        user_id = 'g9f'  # An invalid user ID
        API_response = app.get_user_details(user_id)
        self.assertEqual(API_response,"Response not successful")

if __name__ == '__main__':
    unittest.main()

