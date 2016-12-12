
$(document).ready(loadStudentView);

function loadStudentView() {
    params = getArgs();
    getApi('/api/user/student', {}, function (err, student_info) {
        if (err) {
            alert('加载学生信息出错');
        } else {
            getApi('/api/student/' + student_info.id.toString() + '/grades', {
            }, function (err, grades) {
                if(err) {
                    alert('Error loading student\'s grades');
                } else {
                    getApi('/api/selection/student/' + student_info.id.toString(), {
                    }, function (err, ratings) {
                        if (err) {
                            alert('Error loading rating info.'); 
                        } else {
                            getApi('/api/student/' + student_info.id.toString() + '/courses', {
                            }, function (err, courses) {
                                if (err) {
                                    alert('Error loading courses');
                                } else {
                                    navBar(student_info);
                                    viewGrades(grades);
                                    rateCourses(ratings);
                                    viewClassTable(courses);
                                }
                            });
                        }
                    });
                }
            });
        }
    });
}

function navBar(student) {
    var vm = new Vue({
        el: '#student-basic',
        data: {
            name: student.name,
            student_id: student.id,
            semester: student.semester,
            semesters: student.semesters
        },
        methods: {
            selectSemester: function (term) {
                return location.assign(window.location.pathname + '?semester=' + term)
            }
        }
    });

    var info = new Vue({
        el: '#info',
        data: {
            name: student.name,
            student_id: student.id,
            major: student.major,
            gender: (student.gender == 1) ? '男' : '女'
        }
    });
}

function viewGrades(grades) {
    var vm = new Vue({
        el: '#grades',
        data: {
            grades: grades,
            page: 1
        },
        methods: {
            previous: function () {
                /* body... */
            },

            next: function () {
                /* body... */
            }
        }
    });
}

function rateCourses(ratings) {
    var vm = new Vue({
        el: '#ratings',
        data: {
            courses: ratings,
            page: 1
        },
        methods: {
            previous: function () {
                /* body... */
            },
            next: function () {
                /* body... */
            },
            submitRating: function (course) {
                var value = $('input[name="rating-' + course.id + '"]:checked').val();
                postApi('/api/course/rating', {
                    id: course.id,
                    rating: value
                }, function (err, r) {
                    if (err) {
                        alert('Error rating: ' + err.message);
                    } else {
                        alert('评价成功！')
                    }
                })
            }
        }
    })
}

function viewClassTable (courses) {
    // Preprocess

    var table = [];
    for(var i=0; i<5; i++) {
        var row = [];
        for(var j=0; j<7; j++) {
            row.push('');
        }
        table.push(row);
    }

    for(var i in courses) {
        table[courses[i].start_time][courses[i].day] = courses;
    }

    var vm = new Vue({
        el: '#group',
        data: {
            courses: table
        },
        methods: {

        }
    });
}