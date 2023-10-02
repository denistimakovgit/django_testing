import pytest
from rest_framework.test import APIClient
from students.models import Course, Student
from model_bakery import baker

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    """
    проверка получения первого курса (retrieve-логика)
    """

    # Arrange
    courses = course_factory(_quantity=1)
    course_id = courses[0].id

    #Act
    response = client.get(f'/api/v1/courses/{course_id}/')

    #Assert
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_courses_list(client, course_factory):
    """
    проверка получения списка курсов (list-логика)
    """

    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    for key, value in enumerate(data):
        assert value['name'] ==  courses[key].name

@pytest.mark.django_db
def test_get_courses_filter_id(client, course_factory):
    """
    проверка фильтрации списка курсов по id
    """

    # Arrange
    courses = course_factory(_quantity=5)
    course_id = courses[0].id

    # Act
    response = client.get('/api/v1/courses/', data={'id': course_id})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course_id

@pytest.mark.django_db
def test_get_courses_filter_name(client, course_factory):
    """
    проверка фильтрации списка курсов по name
    """

    # Arrange
    courses = course_factory(_quantity=5)
    course_name = courses[0].name

    # Act
    response = client.get('/api/v1/courses/', data={'name': course_name})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course_name

@pytest.mark.django_db
def test_create_course(client):
    """
    Тест успешного создания курса:
    """

    # Arrange
    studet_1 = Student.objects.create(name='Alexander Petrov', birth_date='2000-01-02')

    # Act
    response = client.post('/api/v1/courses/', data= {
        'id': 1,
        'name': 'Python',
        'students': [studet_1.id]
    })

    # Assert
    assert response.status_code == 201

@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    """
    тест успешного обновления курса
    """

    # Arrange
    students = student_factory(_quantity=2)
    courses = course_factory(_quantity=5)
    course_id = courses[0].id

    # Act
    response = client.patch(f'/api/v1/courses/{course_id}/', data = {
        'name': 'Python',
        'students': [student.id for student in students]
    } )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['students'] == [student.id for student in students]

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    """
    тест успешного удаления курса
    """

    # Arrange
    courses = course_factory(_quantity=5)
    course_id = courses[0].id

    # Act
    response = client.delete(f'/api/v1/courses/{course_id}/')

    # Assert
    assert response.status_code == 204