
$(document).ready(loadStudentView);

var stu_info = {
    id: '2014060101011',
    name: '杨宏春',
    gender: 1,
    major: '物理专业',
    semester: 2016,
    semesters: [2014, 2015, 2016, 2017]
};

var grades = [
    {
        class_id: '23',
        class_name: '大学物理',
        teacher_name: 'TAC',
        final_grade: 120,
        point: 4.0
    },
    {
        class_id: '25',
        class_name: 'C++',
        teacher_name: 'ABC',
        final_grade: 10,
        point: 4.0
    }
];

var ratings = [
    {
        class_id: '23',
        class_name: '大学物理',
        teacher_name: 'TAC',
        rating: 5
    },
    {
        class_id: '25',
        class_name: 'C++',
        teacher_name: 'ABC',
        rating: 4
    }
];

var classes = [
    {
        course_id: '23',
        course_name: '大学物理',
        teacher: 'TAC',
        day: 1,
        start_time: 5,
        end_time: 6,
        place: '挖掘机楼B307'
    },
    {
        course_id: '25',
        course_name: 'C++',
        teacher: 'ABC',
        day: 3,
        start_time: 3,
        end_time: 4,
        place: 'A405'
    }
];

function loadStudentView() {
    navBar(stu_info);
    viewGrades(grades);
    rateCourses(ratings);
    viewClassTable(classes);
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
                var value = $('input[name="rating-' + course.class_id + '"]:checked').val();
                course.rating = value;
            }
        }
    })
}

function viewClassTable (courses) {
    // Preprocess

    var ctable = [];
    for(var i=0; i<5; i++) {
        var row = [];
        for(var j=0; j<7; j++) {
            row.push('');
        }
        ctable.push(row);
    }

    for(var i in courses) {
        ctable[courses[i].start_time - 1][courses[i].day - 1] = courses[i];
    }

    var vm = new Vue({
        el: '#group-panel',
        data: {
            courses: ctable
        },
        methods: {

        }
    });
}