from fastapi import FastAPI

app = FastAPI()

courses_db = [
    {'id': 1, 'instructor': 'Merve', 'title': 'Python', 'category': 'Development'},
    {'id': 2, 'instructor': 'Ahmet', 'title': 'Java', 'category': 'Development'},
    {'id': 3, 'instructor': 'Fatma', 'title': 'Jenkins', 'category': 'Devops'},
    {'id': 4, 'instructor': 'Zeynep', 'title': 'Kubernetes', 'category': 'Devops'},
    {'id': 5, 'instructor': 'Merve', 'title': 'Machine Learning', 'category': 'AI'},
    {'id': 6, 'instructor': 'Ali', 'title': 'Deep Learning', 'category': 'AI'},
]

@app.get("/hello")
async def hello_world():
    return {"message": "Hello World!"}


@app.get("/courses")
async def get_all_courses():
    return courses_db

#Path Parameter
@app.get("/courses/{courses_title}")
async def get_course(courses_title: str):
    for course in courses_db:
        if course['title'].casefold() == courses_title.casefold():
            return course


#This function cannot work because they point to the same path.
@app.get("/courses/{courses_id}")
async def get_course_by_id(courses_id: int):
    for course in courses_db:
        if course.get('id') == courses_id:
            return course


@app.get("/course/byid/{courses_id}")
async def get_course_by_id(courses_id: int):
    for course in courses_db:
        if course.get('id') == courses_id:
            return course


@app.get("/course/")
async def get_course_by_category(category: str):
    courses_to_return = []
    for course in courses_db:
        if course.get('category').casefold() == category.casefold():
            courses_to_return.append(course)
    return courses_to_return
#http://127.0.0.1:8000/course/?category=development  There is /? symbol the reason is use to query not path