from werkzeug.exceptions import HTTPException
import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category, User

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, DELETE, PATCH")
        response.headers.add("Access-Control-Allow-Headers", 'Content-Type')
        return response

    @app.route('/api/v1.0/categories')
    def get_categories():
        try:
            all_categories = Category.query.all()
            categories = {}
            for index in range(len(all_categories)):
                category = all_categories[index]
                categories[category.id] = category.type
        except Exception:
            abort(405)
        return jsonify({"categories": categories})

    @app.route('/api/v1.0/categories', methods=['POST'])
    def create_new_category():
        new_category_id = None
        try:
            categories = Category.query.all()
            category_type = request.get_json()['new_category']
            if category_type:
                for category in categories:
                    if category_type == category.type:
                        abort(422)
                category = Category(type=category_type)
                category.insert()
                new_category_id = category.id
            else:
                abort(400)
        except Exception as e:
            db.session.rollback()
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(400)
        finally:
            db.session.close()
        return jsonify({"category_id": new_category_id})

    @app.route('/api/v1.0/questions')
    def get_questions_by_page():
        try:
            page = int(request.args.get('page', 1))
            QUESTIONS_PER_PAGE = 10
            all_questions = Question.query.all()
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            page_questions = all_questions[start: end]
            questions = []
            categories = {}
            all_categories = Category.query.all()
            if page_questions:
                for page_question in page_questions:
                    question = {
                        'id': page_question.id,
                        'question': page_question.question,
                        'answer': page_question.answer,
                        'difficulty': page_question.difficulty,
                        'category': page_question.category,
                        'rating': page_question.rating
                    }
                    questions.append(question)
            else:
                abort(404)
            for category in all_categories:
                categories[category.id] = category.type
        except Exception:
            abort(404)
        return jsonify({
            'questions': questions,
            'totalQuestions': len(all_questions),
            'categories': categories,
            'currentCategory': 'Science'
            })

    @app.route('/api/v1.0/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        res_question_id = None

        try:
            question = Question.query.get(question_id)
            res_question_id = question.id
            question.delete()
        except Exception:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

        return jsonify({'question_id': res_question_id})

    @app.route('/api/v1.0/questions', methods=['POST'])
    def create_new_question():
        res_question_id = None
        body = request.get_json()
        question=body.get('question')
        answer=body.get('answer')
        category=body.get('category')
        difficulty=body.get('difficulty')
        rating=body.get('rating')
        try:
            if question and answer and category and difficulty:
                question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty,
                    rating=rating
                    )
                question.insert()
                res_question_id = question.id
            else:
                abort(400)    
        except Exception:
            db.session.rollback()
            abort(400)
        finally:
            db.session.close()
        return jsonify({
            'question_id': res_question_id
        })

    @app.route('/api/v1.0/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body.get('searchTerm')
        questions = Question.query.filter(Question.question.ilike(
            '%'+search_term+'%')).all()
        res = []
        if questions:
            for question in questions:
                _question = {
                    'id': question.id,
                    'question': question.question,
                    'answer': question.answer,
                    'difficulty': question.difficulty,
                    'category': question.category,
                    'rating': question.rating
                }
                res.append(_question)
        else:
            abort(404)
        return jsonify({
            'questions': res,
            'totalQuestions': len(questions),
            'currentCategory': 'Science'
            })

    @app.route('/api/v1.0/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category:
            questions = Question.query.filter_by(category=category_id).all()
            res = []
            for question in questions:
                _question = {
                    'id': question.id,
                    'question': question.question,
                    'answer': question.answer,
                    'difficulty': question.difficulty,
                    'category': question.category,
                    'rating': question.rating
                }
                res.append(_question)
        else:
            abort(404)
        return jsonify({
            'questions': res,
            'totalQuestions': len(questions),
            'currentCategory': category.type
            })

    def randomChoiceNotInPrevQuestions(prevQuestions, quiz_questions):
        selected_question = random.choice(quiz_questions)
        if prevQuestions:
            res = {
                'id': selected_question.id,
                'question': selected_question.question,
                'answer': selected_question.answer,
                'difficulty': selected_question.difficulty,
                'category': selected_question.category,
                'rating': selected_question.rating
            }
            return res
        else:
            res = {
                'id': selected_question.id,
                'question': selected_question.question,
                'answer': selected_question.answer,
                'difficulty': selected_question.difficulty,
                'category': selected_question.category,
                'rating': selected_question.rating
            }
            return res

    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def get_quizzes():
        try:
            body = request.get_json()
            prev_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')
            if quiz_category == "All":
                quiz_questions = Question.query.filter(
                    ~Question.id.in_(prev_questions)).all()   
                if quiz_questions:
                    res = randomChoiceNotInPrevQuestions(prev_questions,
                        quiz_questions)
                else:
                    abort(404)
            else:
                category = Category.query.filter_by(
                    type=quiz_category).one_or_none()
                if category:
                    quiz_questions = Question.query.filter(
                        Question.category==category.id,
                        ~Question.id.in_(prev_questions)).all()
                    if quiz_questions:
                        res = randomChoiceNotInPrevQuestions(prev_questions,
                            quiz_questions)
                    else:
                        abort(404)
                else:
                    abort(404)
        except Exception:
            abort(404)
        return jsonify({'question': res})

    @app.route('/api/v1.0/users', methods=["POST"])
    def create_new_user():
        res = {}
        try:
            body = request.get_json()
            name = body.get('name', 'Anon')
            score = body.get('score', 0)
            user = User(name=name, score=score)
            user.insert()
            res['id'] = user.id
            res['name'] = user.name
            res['score'] = user.score
        except Exception:
            db.session.rollback()
            abort(400)
        finally:
            db.session.close()
        return jsonify({'user': res})

    @app.route('/api/v1.0/users', methods=["PATCH"])
    def update_user_score():
        try:
            body = request.get_json()
            id = body.get('id')
            score = body.get('score')
            user = User.query.get(id)
            user.score = score
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()
        return jsonify({'success': True})

    @app.route('/api/v1.0/')
    def index():
        return jsonify({
            'message': "Welcome to Trivia API Home Page"
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
