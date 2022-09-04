import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# paginate questions
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    """
    get all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        # get all categories
        categories = Category.query.all()
        # arrange in a id:type pair
        data = {}
        for category in categories:
            data[category.id] = category.type
        
        return jsonify({
            "success": True,
            "categories": data
        })

    """
    get questions, including pagination (every 10 questions).
    """
    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        # Select all questions
        selection = Question.query.order_by(Question.id).all()
        # get the total num of questions
        total_questions = len(selection)
        # Get current page questions
        current_questions = paginate_questions(request, selection)
        # Get all categories
        categories = Category.query.order_by(Category.id).all()
        
        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": total_questions,
            "categories": {category.id: category.type for category in categories},
            "current_category": None
        })
    
    """
    delete question using a question ID
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            question.delete()
            
            if question is None:
                abort(404)
            
            return jsonify({
                "success": True,
                "deleted": question_id
            })
        except:
            abort(404)
    
    """
    create a new question
    """
    @app.route("/questions", methods=["POST"])
    def add_question():
        body = request.get_json()
        
        if not ("question" in body and "answer" in body and "category" in body and "difficulty" in body):
            abort(422)
            
        new_question = body.get("question")
        new_answer = body.get("answer")
        new_category = body.get("category")
        new_difficulty = body.get("difficulty")
        
        try:
            question = Question(
                question=new_question, answer=new_answer, 
                category=new_category, difficulty=new_difficulty
            )
            question.insert()
            
            return jsonify({
                "success": True,
                "created": question.id
            })
        except:
            abort(422)
    
    """
    get questions with a search term.
    """
    @app.route("/questions/filters", methods=["POST"])
    def search_questions():
        body = request.get_json()
        
        search = body.get("searchTerm", None)
        
        try:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))
            ).all()
            
            questions = paginate_questions(request, selection)
            
            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(selection),
                "current_category": None
            })
        except:
            abort(422)
    
    """
    questions based on category
    """
    @app.route("/categories/<int:category_id>/questions")
    def retrieve_questions_by_categories(category_id):
        try:
            # Retrieve category by id
            category = Category.query.filter(Category.id == category_id).first()
            
            if category:
                # Retrieve all questions by category id
                selection = Question.query.filter(Question.category == category_id).all()
                questions = paginate_questions(request, selection)
                
                if len(questions) == 0:
                    abort(404)
                
                return jsonify({
                    "success": True,
                    "questions": questions,
                    "total_questions": len(selection),
                    "current_category": category.type
                })
            else:
                abort(404)
        except:
            abort(404)
    
    """
    get questions to play the quiz
    """
    @app.route("/quizzes", methods=["POST"])
    def retrieve_quizzes():
        # Get data
        body = request.get_json()
        
        quiz_category = body.get("quiz_category", None)
        previous_ids = body.get("previous_questions", None)
        category_id = quiz_category.get("id")
        
        try:
            # Check category
            if category_id == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == category_id).all()
            
            questions_formatted = [q.format() for q in questions]
            current_ids = [q.get("id") for q in questions_formatted]
            ids = list(set(current_ids).difference(previous_ids))
            
            if len(ids) == 0:
                # If the list is empty return no question
                return jsonify({
                    "success": True,
                    "question": None
                })
            else:
                # Choice a random id
                random_id = random.choice(ids)

                # Get the question
                question = Question.query.get(random_id)
                
                return jsonify({
                    "success": True,
                    "question": question.format()
                })
            return jsonify({
                "success": True,
                "question": None
            })
        except:
            abort(422)
    
    """
    error handlers for all expected errors
    """
    # error 400 - bad request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    # error 404 - resource not found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    # error 405 - method not allowed
    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    # error 422 - unprocessable
    @app.errorhandler(422)
    def unprocessable(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    # error 500 - internal server error
    @app.errorhandler(500)
    def internal_server_error(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
    
    
    return app

