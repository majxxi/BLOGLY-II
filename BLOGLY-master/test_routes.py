from app import app
from unittest import TestCase

class RouteTestCase(TestCase):
    """ Test cases for routes in app.py """

    def setUp(self): 
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_user_list(self):
        res = self.client.get('/users')
        html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('<h1>Blogly Users</h1>', html)
    
    def test_index_redirect(self):
        res = self.client.get('/')
        html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.location, 'http://localhost/users')

    def test_create_new(self):
        res = self.client.get('/users/new')
        html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('<h1>Create a user</h1>', html)

    def test_create_new_user(self):
        res = self.client.post('/users/new', data={'first_name': 'felix', 'last_name': 'miroh', 'image_url': 'google.com'})
        html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.location, 'http://localhost/users')


class PostTestCase(TestCase):

    def setUp(self): 
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_create_new_post(self):

        response = self.client.post('/users/1/posts/new', data = {'title': 'Peach-Pear', 'content': 'blah, blah, blah'})
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/users/1')

    def test_new_post(self):
        response = self.client.get('/posts/1')
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1></h1>', html)

    def test_posts_list(self):
        response = self.client.get('/users/1')
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Peach-Pear', html)

    def test_post_edit(self):
        response = self.client.get('/posts/1/edit')
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit post', html)