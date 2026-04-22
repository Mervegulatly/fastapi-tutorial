from sys import path

from fastapi import FastAPI, Body, Query, Path, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Course:
    id: int
    title: str
    instructor: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, instructor: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.instructor = instructor
        self.rating = rating
        self.published_date = published_date

class Courses(BaseModel): # Veri Modelleme ve Doğrulama için kullanılır. Veri doğrulama tip güvenliği gibi..
    id: Optional[int] = Field(description = "The id of the course, optional." , default = None)
    title: str = Field(min_length=3, max_length=100)
    instructor: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gte=1900, lte=2100) #gte = Büyük eşit, lte= küçük eşit anlamına geliyor.

class CourseRequest(BaseModel):
    id: Optional[int] = Field(description="The id of the course, optional", default=None)
    title: str = Field(min_length=3, max_length=100)
    instructor: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1900, lt=2100)

    #Opsional
    model_config = {  #Request atılırken JSON schema'sının yani genel yapısının nasıl olacağının örneğini de vermiş oluyor burda.
        "json_schema_extra":{
            "example":{
                "title": "Example Course",
                "instructor": "Example Instructor",
                "rating": 5,
                "published_date": 1900
            }
        }
    }

courses_db = [
    Course(1, "Python", "Merve", 5, 2029),
    Course(2, "Kotlin", "Ahmet", 5, 2026),
    Course(3, "Jenkins", "Merve", 5, 2023),
    Course(4, "kubernetes", "Zeynep", 2, 2030),
    Course(5, "Machine Learning", "Ayse", 3, 2036),
    Course(6, "Deep Learning", "Atlas", 1, 2039)
]


@app.get("/courses",status_code=status.HTTP_200_OK)
async def get_all_courses():
    return courses_db


@app.get("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id: int = Path(gt=0)):  #We can use this to determine the minimum size.(gt)
    for course in courses_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


@app.get("/courses/", status_code=status.HTTP_200_OK)
async def get_courses_by_rating(course_rating: int = Query(gt=0, lt=6)):
    courses_to_return = []
    for course in courses_db:
        if course.rating == course_rating:
            courses_to_return.append(course)
    return courses_to_return


@app.get("/courses/publish/", status_code=status.HTTP_200_OK)  #publish is a "static" path in here
async def get_courses_by_publish_date(publish_date: int = Query(gt=2005, lt=20240)):
    courses_to_return = []
    for course in courses_db:
        if course.published_date == publish_date:
            courses_to_return.append(course)
    return courses_to_return


# Yardımcı fonksiyon: ID atamasını yapar ve nesneyi döner
def find_course_id(course: Course):
    # Listenin son elemanının bir nesne olduğundan emin olmalıyız
    if len(courses_db) > 0:
        course.id = courses_db[-1].id + 1
    else:
        course.id = 1
    return course


@app.post("/create-course", status_code=status.HTTP_201_CREATED)
async def create_course(course_request: CourseRequest):
    # 1. Request'ten gelen veriyi Course sınıfı nesnesine dönüştür
    new_course = Course(**course_request.model_dump())

    # 2. ID'yi otomatik belirle (Fonksiyonu çağır)
    new_course = find_course_id(new_course)

    # 3. Listeye ekle (Sadece bir kere!)
    courses_db.append(new_course)

    return {"message": "Course created successfully", "course": new_course}