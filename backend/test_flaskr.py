import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'student', 
            'student', 
            'localhost:5432', 
            self.database_name
        )
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'id': 24,
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 2,
            'category': 1,
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    """ test retrieve categories """
    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    """ test retrieve questions """
    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data["current_category"], None)
    
    """ test retrieve questions 404 error """
    def test_404_sent_requesting_questions_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    """ test delete question """
    def test_delete_question(self):
        res = self.client().delete("/questions/24")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 24).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 24)
    
    """ test delete question 404 error """
    def test_404_if_question_does_not_exist(self):
        res = self.client().delete("/questions/100000")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    """ test add question """
    def test_add_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
    
    """ test add question 405 error """
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")
    
    """ test add question 422 error """
    def test_422_if_question_creation_unprocessable(self):
        res = self.client().post("/questions", json={
            'question': 'new_question', 'answer': 'new_answer', 'category': 1
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    """ test search questions with results """
    def test_search_questions_with_results(self):
        res = self.client().post("/questions/filters", json={'searchTerm': 'Africa'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], None)
    
    """ test search questions without results """
    def test_search_questions_without_results(self):
        res = self.client().post("/questions/filters", json={'searchTerm': 'aabbcc'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], None)
    
    """ test retrieve questions by category """
    def test_retrieve_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 4)
        self.assertEqual(data['total_questions'], 4)
        self.assertEqual(data['current_category'], 'Art')
    
    """ test retrieve questions by category 404 error """
    def test_404_if_questions_by_category_not_found(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    """ test retrieve quizzes with result """
    def test_retrieve_quizzes_with_result(self):
        res = self.client().post('/quizzes', json={'previous_questions': [],'quiz_category': {'id': '2', 'type': 'Art'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(len(data['question']))
    
    """ test retrieve quizzes without result """
    def test_retrieve_quizzes_without_result(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [16,17,18,19],
            'quiz_category': {'id': '2', 'type': 'Art'}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)
    
    """ test retrieve quizzes 400 error """
    def test_400_retrieve_quizzes_bad_request(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()