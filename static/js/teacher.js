$(document).ready(loadTeacherView);

var classes = [
    {
        id: 1,
        number: 2014060104,
        course: {
            id: 23,
            student_count: 2
        },
        students: [
            {
                id: 2014060104001,
                name: 'Tom',
                gender: 1,
                major: '计算机',
                regular: 0,
                midterm: 0,
                final: 0,
                total: 0,
                grade: 0
            },
            {
                id: 2014060104002,
                name: 'Jerry',
                gender: 1,
                major: '计算机',
                regular: 0,
                midterm: 0,
                final: 0,
                total: 0,
                grade: 0
            }
        ]

    },
    {
        id: 2,
        number: 2014040203,
        course: {
            id: 24,
            student_count: 2
        },
        students: [
            {
                id: 2014040203001,
                name: 'Tom',
                gender: 1,
                major: '挖掘机',
                regular: 0,
                midterm: 0,
                final: 0,
                total: 0,
                grade: 0
            },
            {
                id: 2014040203002,
                name: 'Jerry',
                gender: 1,
                major: '挖掘机',
                regular: 0,
                midterm: 0,
                final: 0,
                total: 0,
                grade: 0
            }
        ]
    }
];

var teacher = {
    name: '杨宏春',
    id: 12345,
    level: 'Professor',
    address: '主楼A5-233',
    telephone: '13800012345',
    email: 'yhc@uestc.edu.cn',
    intro: '量子计算机'
};

function loadTeacherView () {
    gradeView(classes);
    ratingView(classes);
    infoView(teacher);
}

function gradeView (classes) {
    var vm = new Vue({
        el: '#grades',
        data: {
            classes: classes,
            my_page: 1,
            students: [],
            class: {},
            current_class: {}
        },
        computed: {
            page: {
                get: function () {
                    return this.my_page;
                },
                set: function (val) {
                    this.my_page = val;
                }
            }
        },
        methods: {
            previous: function () {
                if (this.page == 1) {
                    return;
                }
                this.page = this.page - 1;
            },
            next: function () {
                this.page = this.page + 1;
            },
            setGrade: function (class_) {
                $('#modal-set-grades').modal('show');
                this.students = class_.students;
                this.current_class = class_.course;
            },
            displayStat: function (class_) {
                $('#modal-visualize-grades').modal('show');
                this.students = class_.students;
                this.current_class = class_.course;
            },
            computeTotal: function (student) {
                var regular = parseInt($('#stu-regular-score-' + student.id).val() || '0');
                var midterm = parseInt($('#stu-midterm-score-' + student.id).val() || '0');
                var final = parseInt($('#stu-final-score-' + student.id).val() || '0');
                var total = parseInt(regular * 0.1 + midterm * 0.2 + final * 0.7);

                student.regular = regular;
                student.midterm = midterm;
                student.final = final;
                student.total = total;
            },
            editStuGrade: function () {

            },
            import: function () {

            },
            export: function () {

            }
        }
    }) 
}

function ratingView (classes) {
    var vm = new Vue({
        el: '#customer',
        data: {
            classes: classes,
            my_page: 1,
            ratings: {}
        },
        computed: {
            page: {
                get: function () {
                    return this.my_page;
                },
                set: function (val) {
                    this.my_page = val;
                }
            }
        },
        methods: {
            previous: function () {
                if (this.page == 1) {
                    return;
                }
                this.page = this.page - 1;
            },
            next: function () {
                this.page = this.page + 1;
            },
            displayRatingStat: function (class_) {
                $('#modal-visualize-ratings').modal('show');
            }
        }
    })
}

function infoView (teacher) {
    var vm = new Vue({
        el: '#info',
        data: {
            name: teacher.name,
            teacher_id: teacher.id,
            level: teacher.level,
            address: teacher.address,
            telephone: teacher.telephone,
            email: teacher.email,
            intro: teacher.intro
        },
        methods: {
            updateTeacherInfo: function () {
                alert('修改成功!');
            }
        }
    })
}