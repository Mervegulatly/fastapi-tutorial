from fastapi import FastAPI, Body

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



#Both Query and Path are provided
@app.get("/course/{course_instructor}/")
async def get_instructor_category_by_query(course_instructor: str, category: str):
    courses_to_return = []
    for course in courses_db:
        if course.get('instructor').casefold() == course_instructor.casefold() and course.get('category').casefold() == category.casefold():
            courses_to_return.append(course)
    return courses_to_return


@app.post("/course/{create_course}")
async def create_course(new_course = Body()):
    courses_db.append(new_course)


@app.put("/course/update_course")
async def update_course(updated_course = Body()):
    for index in range(len(courses_db)):
        if courses_db[index].get("id") == updated_course.get("id"):
            courses_db[index] = updated_course


@app.delete("/course/delete_course/{course_id}")
async def delete_course(course_id: int):
    for index in range(len(courses_db)):
        if courses_db[index].get("id") == course_id:
            courses_db.pop(index)
            break