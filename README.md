# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

<!-- API Documentation -->

## API Reference

### Introduction
The Trivia API uses resource-oriented URLs, accepts JSON formatted, form encoded request bodies and returns **JSON-encoded** responses, using correct HTTP response status codes.

Trivia API was created using ***Test Driven Development*** (TDD), hence you can also use this API in test mode without interacting with your main development database


### Getting Started
#### Base URL
` http://127.0.0.1:5000 `

#### API keys / Authentication
None

### Errors
Trivia uses some of the standard HTTP status codes to indicate the success or failure of an API request.
Codes in the category of `2xx` represent `Success`. Codes in the category of `3xx` represent `Redirection`. Codes in the category of `4xx` represent ` Client Error `(i.e error causes by input data). Codes in the category of `5xx` represent `Server Error` (i.e error with Trivia servers)

#### Status codes and messages 
`200` - **OK**   --> Everything went as expected\
`400` - **Bad Request**    --> The request was unacceptable\
`404`  -  **Not Found**    --> Request resouce not found\
`405`  -  **Method Not Allowed**    --> Incorrect HTTP method used for endpoint\
`422`  -  **Unprocessable Entity**   --> Request argument/body syntax is correct, but unable to process it\
`500`  -  **Internal Server Error**   --> Something went wrong with Trivia server

### Resource Endpoint Library
`GET '/api/v1.0/' `
- Welcome Page
- Request Arguments: None
- Returns: An object with a welcome message
#### Sample

URL\
`curl http://127.0.0.1:5000/api/v1.0/`

Response 
```
    {
        "message": "Welcome to Trivia API Home Page"
    }
```
---

`GET '/api/v1.0/categories' `
- This fetches a dictionary of all the categories from the database in which the keys are the ids and the values are the types.
- Request Arguments: None
- Returns: An object with a single key, `categories` that maps to an object of `id: category_type` pairs.

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/categories`

Response
```
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }
    }
```
---
`POST '/api/v1.0/categories' `
- This creates a new category provided it does not alraedy exist
- Request Arguments: An object with a single key `"type" : "type_value"` 
- Returns: An object with a single key of the new category id.

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/categories -X POST -H "Content-Type:application/json" -d "{\"new_category\" : \"Fashion\"}"`

Response\
`{"category_id": 8}`

---
`GET '/api/v1.0/categories/${category_id}/questions'`
- This fetches all the questions of a particular category. The route variable `category_id` represents the id of the category.
- Request Argument(s): `category_id` - integer
- Returns: An object of three keys. `questions` which maps to the array of all the questions that have a `category` which is equal of `category_id`. `totalQuestions` which maps to the number of items in the `questions` array. `currentCategory` maps to .

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/categories/2/questions`

Response
```
    {
        "currentCategory": "Art",
        "questions": [
            {
                "answer": "Escher",
                "category": 2,
                "difficulty": 1,
                "id": 16,
                "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?",
                "rating": 1
            },
            {
                "answer": "Mona Lisa",
                "category": 2,
                "difficulty": 3,
                "id": 17,
                "question": "La Giaconda is better known as what?",
                "rating": 1
            },
            {
                "answer": "One",
                "category": 2,
                "difficulty": 4,
                "id": 18,
                "question": "How many paintings did Van Gogh sell in his lifetime?",
                "rating": 1
            },
            {
                "answer": "Jackson Pollock",
                "category": 2,
                "difficulty": 2,
                "id": 19,
                "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
                "rating": 1
            }
        ],
        "totalQuestions": 4
    }
```
---
`GET '/api/v1.0/questions?page=${page_no}' `
- This fetches a dictionary of `questions` maps to an array of objects of 10 paginated questions. `categories` maps to an object of all the categories present in the `questions` array. `totalQuestions` maps to the count of all the questions.
- Request Argument(s): `page_no` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string 

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/questions?page=1`

Response
```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "currentCategory": "",
        "questions": [
            {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                "rating": 1
            },
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?",
                "rating": 1
            },
            {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
                "rating": 1
            },
            {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
                "rating": 1
            },
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
                "rating": 1
            },
            {
                "answer": "Brazil",
                "category": 6,
                "difficulty": 3,
                "id": 10,
                "question": "Which is the only team to play in every soccer World Cup tournament?",
                "rating": 1
            },
            {
                "answer": "Uruguay",
                "category": 6,
                "difficulty": 4,
                "id": 11,
                "question": "Which country won the first ever soccer World Cup in 1930?",
                "rating": 1
            },
            {
                "answer": "George Washington Carver",
                "category": 4,
                "difficulty": 2,
                "id": 12,
                "question": "Who invented Peanut Butter?",
                "rating": 1
            },
            {
                "answer": "Lake Victoria",
                "category": 3,
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?",
                "rating": 1
            },
            {
                "answer": "The Palace of Versailles",
                "category": 3,
                "difficulty": 3,
                "id": 14,
                "question": "In which royal palace would you find the Hall of Mirrors?",
                "rating": 1
            }
        ],
        "totalQuestions": 19
    }
```
---
`POST '/api/v1.0/questions'`
- Sends a request to create a new question.
- Request Body: An object of question with `"question": "question_value"` key:value pairs
- Returns: An object with a single value of the question id

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/questions -X POST -H "Content-Type:application/json" -d "{\"question\": \"What is the capital of Finland\",\"answer\": \"Helsinki\",\"category\": 3,\"difficulty\": 2,\"rating\":4}"`

Response\
`{"question_id": 24}`

---
`POST '/api/v1.0/questions'`
- Sends a request to search for a question.
- Request Body: An object with `"searchTerm": "searchTerm_value"`  key:value pair
- Returns: An object with a current category, an array of questions that matched the search term (case insensitive), current category string and total number of questions returned

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/questions -X POST -H "Content-Type:application/json" -d "{\"searchTerm\": \"title of the 1990 fantasy\"}"`

Response
```
    {
        "currentCategory": "",
        "questions": [
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
                "rating": 1
            }
        ],
        "totalQuestions": 1
    }
```
---
`POST '/api/v1.0/quizzes'`
- Fetches a random question from a given category provided it is not part of the previous three questions
- Request Body:  An object of the quiz category and an array of the previous three questions
- Returns: An single object of a random question in the given category

#### Sample
URL\
`curl http://127.0.0.1:5000/api/v1.0/quizzes -X POST -H "Content-Type: application/json" -d "{\"previous_questions\" : [4, 6, 12],\"quiz_category\" : \"Science\"}"`

Response 
```
   {
        "question": {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?",
            "rating": 1
        }
    }
```

### Deployment
None

### Authors
Udacity\
Ibeh Esther

### New Game Mechanics
I added more questions to the `backend/triva.psql`, so that each category has enough questions to run through atleast one quiz session.


