function getCourses() {
    fetch('/api/courses/')
        .then(response => response.json())
        .then(data => {
            console.log('Курсы:', data);
        })
        .catch(error => {
            console.error('Ошибка при получении данных о курсах:', error);
        });
}


function getStudents() {
    fetch('/api/students/')
        .then(response => response.json())
        .then(data => {
            console.log('Студенты:', data);
        })
        .catch(error => {
            console.error('Ошибка при получении данных о студентах:', error);
        });
}

getCourses();
getStudents();
