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
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=True
flask run
```
Setting the `FLASK_DEBUG` variable to `True` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.


## API Endpoints

### GET `/categories`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request arguments: None.
- Returns:  An object with these keys:
  - `success`: The success flag
  - `categories`: Contains a object of `id:category_string` and `key:value pairs`.

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
  "success": true
}
```

### GET `/questions`
- Fetches:
  - A list of questions (paginated by 10 items)
  - A dictionary of categories
  - The total of questions
  - The current category
- Request arguments:
  - `page` (integer) - The current page
- Returns: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions (paginated by 10 items)
  - `total_questions`: The total of questions
  - `categories`: A dictionary of categories
  - `current_category`: The current category

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
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### DELETE `/questions/:question_id/`
- Delete question using a question ID
- Request arguments:
  - `question_id` (integer): The question id
- Returns: An object with theses keys:
  - `success` that contains a `boolean`.
  - `deleted` that contains the ID of the question created.

```
{
  "deleted": 16,
  "success": true
}
```

### POST `/questions`
- Create a new question.
- Request arguments:
  - `question` (string) - The question
  - `answer` (string) - The answer
  - `difficulty` (string) - The question difficulty
  - `category` (string) - The question category
- Returns: An object with theses keys:
  - `success` that contains a `boolean`.
  - `created` that contains the ID of the question created.

```
{
  "created": 27,
  "success": true
}
```

### POST `/questions/filters`
- Search a question.
- Request arguments:
  - `search` (string) - The term to search
- Returns: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions
  - `total_questions`: The total of questions
  - `current_category`: The current category string

```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 3
}}
```


### GET `/categories/:category_id/questions`
- Fetches a list of questions based on category.
- Request arguments:
  - `category_id` (integer): The category id
- Returns: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions (paginated by 10 items)
  - `total_questions`: The total of questions
  - `current_category`: The current category string

```
{
  "current_category": "Geography",
  "questions": [
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### POST `/quizzes`
- Fetches a question to play the quiz.
- Request arguments:
  - `quiz_category` (dictionary): The quiz category with the `type` and the `id`.
  - `previous_ids` (list of strings): The previous questions ids
- Returns: An object with these keys:
  - `success`: The success flag
  - `question`: The question to play

```
{
  "question": {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
  "success": true
}
```

## Errors

### Error 400
- Returns an object with these keys: `success`, `error` and `message`.

```
{
  "success": false,
  "error": 400,
  "message": "bad request"
}
```

### Error 404
- Returns an object with these keys: `success`, `error` and `message`.

```
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

### Error 405
- Returns an object with these keys: `success`, `error` and `message`.

```
{
  "success": false,
  "error": 405,
  "message": "method not allowed"
}
```

### Error 422
- Returns an object with these keys: `success`, `error` and `message`.

```
{
  "success": false,
  "error": 422,
  "message": "unprocessable"
}
```

### Error 500
- Returns an object with these keys: `success`, `error` and `message`.

```
{
  "success": false,
  "error": 500,
  "message": "internal server error"
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
