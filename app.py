import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()
app = Flask(__name__)

url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)


#CREATE_LESSONS = "CREATE TABLE IF NOT EXISTS lessons (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL);"
#CREATE_THEMES = "CREATE TABLE IF NOT EXISTS themes (lesson_id INTEGER, theme VARCHAR(255),date TIMESTAMP, FOREIGN KEY(lesson_id) REFERENCES lessons(id) ON DELETE CASCADE);"

INSERT_LESSON_RETURN_ID = "INSERT INTO lessons (name) VALUES (%s) RETURNING id;"
INSERT_THEME = "INSERT INTO themes (lesson_id, theme) VALUES (%s, %s);"
LESSON_NAME = "SELECT name FROM lessons WHERE id = (%s);"
LESSON_THEME = "SELECT theme FROM themes WHERE lesson_id = (%s);"

@app.post("/api/lesson")
def create_lesson():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_LESSON_RETURN_ID, (name,))
            lesson_id = cursor.fetchone()[0]
    return {"id": lesson_id, "message": f"Lesson {name} created."}, 201


@app.post("/api/theme")
def create_theme():
    data = request.get_json()
    theme = data["theme"]
    lesson_id = data["lesson"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_THEME, (lesson_id, theme))
    return {"message": "Theme added."}, 201


@app.get("/api/lesson/<int:lesson_id>")
def get_lesson_theme (lesson_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(LESSON_NAME, (lesson_id,))
            name = cursor.fetchone()[0]
            cursor.execute(LESSON_THEME, (lesson_id,))
            theme = cursor.fetchone()[0]
    return {"Lesson name": name, "Lesson theme": theme}, 200
