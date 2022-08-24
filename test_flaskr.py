import os
from os.path import join, dirname
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST,
            self.database_name)
        self.new_data = {
            'question': 'Where is Lekki located',
            'answer': 'Island',
            'category': 3,
            'difficulty': 1,
            'rating': 4
        }
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    # Test for get_categories pass
    def test_get_categories(self):
        res = self.client().get('/api/v1.0/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
    # Test for get_categories fail due to wrong HTTP method

    def test_405_categories(self):
        res = self.client().patch('/api/v1.0/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')
    # Test for get_questions_by_page pass

    def test_get_questions(self):
        res = self.client().get('/api/v1.0/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['totalQuestions'])
    # Test for get_questions_by_page fail due to page out of range

    def test_404_page_out_of_range(self):
        res = self.client().get('/api/v1.0/questions?page=500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
    # Test for delete_question pass

    def test_delete_question(self):
        res = self.client().delete('/api/v1.0/questions/30')
        data = json.loads(res.data)
        question_id = 30

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question_id'], question_id)

    # # Test for delete_question fail due to question not found
    def test_404_question_not_found(self):
        res = self.client().delete('/api/v1.0/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Test for create_new_question_and_search_question pass
    def test_create_new_question(self):
        res = self.client().post('/api/v1.0/questions', json=self.new_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question_id'])

    # Test for create_new_question
    # fail due to invalid input
    def test_400_bad_question_request(self):
        res = self.client().post('/api/v1.0/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Test for get_question(s)_by_search pass
    def test_get_questions_by_search(self):
        res = self.client().post(
            '/api/v1.0/questions/search', json={'searchTerm': 'discovered'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    # Test for search_question fail
    def test_404_search_term_not_found(self):
        res = self.client().post(
            '/api/v1.0/questions/search', json={'searchTerm': 'asdfg'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Test for get_questions_by_category pass
    def test_get_questions_by_category(self):
        res = self.client().get('/api/v1.0/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    # Test for get_questions_by_category fail
    # due to category questions not found
    def test_404_category_questions_not_found(self):
        res = self.client().get('/api/v1.0/categories/50/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Test for get_quizzes pass
    def test_get_quizzes(self):
        res = self.client().post('/api/v1.0/quizzes', json={
            'previous_questions': [5, 8, 20],
            'quiz_category': 'Entertainment'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue('question')

    # Test for get_quizzes fail due to quiz_category not found
    def test_404_category_not_found(self):
        res = self.client().post('/api/v1.0/quizzes',  json={
            'previous_questions': [5, 8, 20],
            'quiz_category': 'Zoolology'
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Test for create_new_category pass
    def test_create_new_category(self):
        res = self.client().post(
            '/api/v1.0/categories', json={'new_category': 'Beauty'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['category_id'])

    # Test for create_new_category fail due to bad request input
    def test_400_bad_request_parameter(self):
        res = self.client().post('/api/v1.0/categories', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Test for create_new_category fail due to category type already exists
    def test_422_category_type_already_exists(self):
        res = self.client().post(
            '/api/v1.0/categories', json={"new_category": "Entertainment"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    # Test for create_new_user pass
    def test_create_new_user(self):
        res = self.client().post(
            '/api/v1.0/users', json={"name": "Esther", "score": 0})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['user'])

    # Test for update_user_score pass
    def test_update_user_score(self):
        res = self.client().patch(
            '/api/v1.0/users', json={"id": 2, "score": 7})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Test for update_user_score fail due user not found
    def test_404_cannot_update_user_score(self):
        res = self.client().patch(
            '/api/v1.0/users', json={"id": 1000, "score": 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
