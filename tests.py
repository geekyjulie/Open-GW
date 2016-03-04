#Unit testing

import unittest

from flask.ext.login import current_user
from flask import request

from app import BaseTestCase
from models import User, Post, Comment

__author__ = 'reham'



class TestUser(BaseTestCase):

# Ensure user can register
    def test_user_registeration(self):
        with self.client:
            response = self.client.post('register/', data=dict(
                username='athoug', email='athoug@gwu.edu',  #test user
                password='password', password2='password',department='CS' 
            ), follow_redirects=True)
            self.assertIn(b'You\'ve been registered!', response.data)
            self.assertTrue(current_user.name == "athoug")
            self.assertTrue(current_user.is_active())
            user = User.query.filter_by(email='athoug@gwu.edu').first()
            self.assertTrue(str(user) == '<name - athoug>')


# Ensure errors are thrown during an incorrect user registration if uername is already taken
    def test_incorrect_username_registeration(self):
        with self.client:
            response = self.client.post('register/', data=dict(
                username='athoug', email='athoug@gwu.edu',
                password='password', password2='password',department='CS'
            ), follow_redirects=True)
            self.assertIn(b'User with that username already exitst.', response.data)
            self.assertIn(b'/register/', request.url)

 # Ensure errors are thrown during an incorrect user registration if email is already exist
    def test_incorrect_email_registeration(self):
        with self.client:
            response = self.client.post('register/', data=dict(
                username='athoug', email='athoug@gwu.edu',
                password='password', password2='password',department='CS'
            ), follow_redirects=True)
            self.assertIn(b'User with that email already exitst', response.data)
            self.assertIn(b'/register/', request.url)


# Ensure id is correct for the current/logged in user
    def test_get_by_id(self):
        with self.client:
            self.client.post('/login', data=dict(
                username="athoug", password='password'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)



class UserViewsTests(BaseTestCase):

# Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)


# Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            self.assertIn(b'You were logged in', response.data)
            self.assertTrue(current_user.name == "athoug")
            self.assertTrue(current_user.is_active())


# Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )

    self.assertIn(b'Your email or password doen't match!', response.data)


# Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You've been logged out! Come back soon.', response.data)
            self.assertFalse(current_user.is_active())



class PostTests(BaseTestCase):

# Ensure a logged in user can add a new post
    def test_user_can_add_post(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            response = self.client.post(
                '/post/',  #'/post/<int:postid>'
                data=dict(content="test"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Comment posted!',
                          response.data)


# Ensure a logged in user can edit post
    def test_user_can_edit_post(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            response = self.client.post(
                '/edit/<int:postid>',
                data=dict(content="test2"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Post edited successfuly!',
                          response.data)


# Ensure a logged in user can delete post
    def test_user_can_delete_post(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            response = self.client.post(
                'delete_post/<int:postid>',
                data=dict(content="test2"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your post has been deleted!',
                          response.data)


class CommentTests(BaseTestCase):

# Ensure a logged in user can edit comment
    def test_user_can_edit_comment(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            response = self.client.comment(
                '/edit_comment/<int:commentid>',
                data=dict(content="test2"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Comment edited successfuly!',
                          response.data)

# Ensure a logged in user can delete comment
    def test_user_can_delete_comment(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            response = self.client.comment(
                '/delete_comment/<int:commentid>',
                data=dict(content="test2"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Your comment has been deleted!',
                          response.data)



 class FollowUnFollowTests(BaseTestCase):

# Ensure a logged in user can follow 
    def test_follow_user(self):
        with self.client:
            self.client.Relationship.to_user(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            response = self.client.Relationship.to_user(
                '/follow/<username>',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You are now following {}!',
                          response.data)


# Ensure a logged in user can unfollow 
    def test_unfollow_user(self):
        with self.client:
            self.client.Relationship.to_user(
                '/login',
                data=dict(username="athoug", password="password"),
                follow_redirects=True
            )
            response = self.client.Relationship.to_user(
                '/unfollow/<username>',
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have unfollowing {}!',
                          response.data)


	if __name__ == '__main__':
    unittest.main()