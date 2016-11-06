$(document).ready();

function loadAdminView() {
    params = getArgs();

    getApi('/api/students', {
        page: params.page || 1
    }, function (err, students) {
        if (err) {
            alert('Error loading student ' + err.message); 
        } else {
            studentView(students);

            getApi('/api/teachers', {
                page: params.page || 1
            }, function (err, teachers) {
                if (err) {
                    alert('error loading teacher - ' + err.message);
                } else {
                    teacherView(teachers);

                    getApi('/api/courses', {
                        page: params.page || 1
                    }, function (err, courses) {
                        if (err) {
                            alert('error loading courses - ' + err.message);
                        } else {
                            courseView(courses);

                            getApi('/api/selections', {
                                page: params.page || 1
                            }, function (err, selections) {
                                if (err) {
                                    alert('error loading selections - ' + err.message); 
                                } else {
                                    selectionView(selections);

                                    getApi('/api/grades', {
                                        page: params.page || 1
                                    }, function (err, grades) {
                                        if (err) {
                                            alert('error loading grades - ' + err.message);
                                        }
                                        gradeView(grades);
                                    });
                                }
                            });
                        }
                    });
                }
            }) ;
        }
    });
}

function studentView (students) {
    var vm = new Vue({
        el: '#students',
        data: {
            students: students,
            my_page: 1,
            query: '',
            criteria: 'id',
            current_name: '',
            current_id: '',
            current_level: '',
            current_new_password: '',
            current_address: '',
            current_tel: '',
            current_email: '',
            current_intro: ''
        },
        computed: {
            page: {
                get: function () {
                    return this.my_page;
                },
                set: function (val) {
                    this.my_page = val;
                    var _this = this;
                    getApi('/api/teachers', {
                        page: this.my_page
                    }, function (err, r) {
                        if (err) {
                            alert('Error paging: ' + err.message);
                        } else {
                            reloadArray(_this.classes, r);
                        }
                    });
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
            queryStudent: function (argument) {
                var _this = this;
                getApi('/api/students', {
                    page: this.page,
                    query: this.query,
                    criteria: this.criteria
                }, function (err, r) {
                    if (err) {
                        alert('Error query: ' + err.message);
                    } else {
                        reloadArray(_this.students, r);
                    }
                });
            },
            updateStuInfo: function () {
                var _this = this;
                postApi('/api/admin/student', {
                    id: this.current_stu_id,
                    name: this.current_name,
                    gender: this.current_gender,
                    password: this.current_password,
                    major: this.current_major
                }, function (err, r) {
                    if (err) {
                        alert('update error: ' + err.message);
                    } else {
                        _this.page = _this.page;
                    }
                });
            },
            showEditStuInfo: function (student) {
                if (student) {
                    this.current_name = student.name;
                    this.current_major = student.major;
                    this.current_gender = student.gender;
                    this.current_stu_id = student.id;
                } else {
                    this.current_name = '';
                    this.current_major = '';
                    this.current_gender = '';
                    this.current_stu_id = '';
                }
                $('#edit-students').modal('show');
            }
        }
    });
}

function teacherView(teachers) {
    var vm = new Vue({
        el: '#teachers',
        data: {
            teachers: teachers,
            my_page: 1
        },
        computed: {
            page: {
                get: function () {
                    return this.my_page;
                },
                set: function (val) {
                    this.my_page = val;
                    var _this = this;
                    getApi('/api/teachers', {
                        page: this.my_page
                    }, function (err, r) {
                        if (err) {
                            alert('Error paging: ' + err.message);
                        } else {
                            reloadArray(_this.classes, r);
                        }
                    });
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
            queryTeacher: function () {
                var _this = this;
                getApi('/api/teachers', {
                    page: this.page,
                    query: this.query,
                    criteria: this.criteria
                }, function (err, r) {
                    if (err) {
                        alert('Error query: ' + err.message);
                    } else {
                        reloadArray(_this.teachers, r);
                    }
                });
            },
            updateTeacherInfo: function () {
                var _this = this;
                postApi('/api/admin/teacher', {
                    id: this.current_id,
                    name: this.current_name,
                    password: this.current_password,
                    level: this.current_level,
                    address: this.current_address,
                    telephone: this.current_tel,
                    email: this.current_email,
                    intro: this.current_intro
                }, function (err, r) {
                    if (err) {
                        alert('update error: ' + err.message);
                    } else {
                        _this.page = _this.page;
                    }
                });
            },
            showEditTeacherInfo: function (teacher) {
                if (student) {
                    this.current_name = teacher.name;
                    this.current_id = teacher.id;
                    this.current_level = teacher.level;
                    this.current_new_password = '';
                    this.current_address = teacher.address;
                    this.current_tel = teacher.telephone;
                    this.current_email = teacher.email;
                    this.current_intro = teacher.intro;
                } else {
                    this.current_name = '';
                    this.current_id = '';
                    this.current_level = '';
                    this.current_new_password = '';
                    this.current_address = '';
                    this.current_tel = '';
                    this.current_email = '';
                    this.current_intro = '';
                }
                $('#edit-teachers').modal('show');
            }
        }
    });
}

function courseView (courses) {
    var vm = new Vue({
        el: '#courses',
        data: {
            courses: courses,
            my_page: 1,
            current_id: '',
            current_name: '',
            current_teacher_name: '',
            current_place: '',
            current_start_week: '',
            current_end_week: '',
            current_day: '',
            current_start_time: '',
            current_end_time: '',
            current_credit: ''
        },
        computed: {
            page: {
                get: function () {
                    return this.my_page;
                },
                set: function (val) {
                    this.my_page = val;
                    var _this = this;
                    getApi('/api/courses', {
                        page: this.my_page
                    }, function (err, r) {
                        if (err) {
                            alert('Error paging: ' + err.message);
                        } else {
                            reloadArray(_this.classes, r);
                        }
                    });
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
            queryCourse: function () {
                var _this = this;
                getApi('/api/courses', {
                    page: this.page,
                    query: this.query,
                    criteria: this.criteria
                }, function (err, r) {
                    if (err) {
                        alert('Error query: ' + err.message);
                    } else {
                        reloadArray(_this.teachers, r);
                    }
                });
            },
            updateCourseInfo: function () {
                var _this = this;
                postApi('/api/admin/course', {
                    id: this.current_id,
                    name: this.current_name,
                    teacher: this.current_teacher_name,
                    place: this.current_place,
                    start_week: this.current_start_week,
                    end_week: this.current_end_week,
                    day: this.current_day,
                    start_time: this.current_start_time,
                    end_time: this.current_end_time,
                    credit: this.current_credit
                }, function (err, r) {
                    if (err) {
                        alert('update error: ' + err.message);
                    } else {
                        _this.page = _this.page;
                    }
                });
            },
            showEditCourseInfo: function (course) {
                if (student) {
                    this.current_name = course.name;
                    this.current_id = course.id;
                    this.current_teacher_name = course.teacher;
                    this.current_place = course.place;
                    this.current_start_week = course.start_week;
                    this.current_end_week = course.end_week;
                    this.current_day = course.day;
                    this.current_start_time = course.start_time;
                    this.current_end_time = course.end_time;
                    this.current_credit = course.credit
                } else {
                    this.current_name = '';
                    this.current_id = '';
                    this.current_teacher_name = '';
                    this.current_place = '';
                    this.current_start_week = '';
                    this.current_end_week = '';
                    this.current_day = '';
                    this.current_start_time = '';
                    this.current_end_time = '';
                    this.current_credit = '';
                }
                $('#edit-courses').modal('show');
            }
        }
    });
}

function selectionView(selections) {
    var vm = new Vue({
        el: '#group',
        data: {
            selections: selections,
            my_page: 1
        },
        computed: {
            page: {
                get: function () {
                    return this.my_page;
                },
                set: function (val) {
                    this.my_page = val;
                    var _this = this;
                    getApi('/api/selections', {
                        page: this.my_page
                    }, function (err, r) {
                        if (err) {
                            alert('Error paging: ' + err.message);
                        } else {
                            reloadArray(_this.classes, r);
                        }
                    });
                }
            }
        },
        methods: {

        }
    });
}

function gradeView(grades) {
    var vm = new Vue({
        el: '#grades',
        data: {
            grades: grades,
            my_page: 1,
            current_stu_id: '',
            current_stu_name: '',
            current_course_id: '',
            current_course_name: '',
            current_teacher_name: '',
            current_credit: '',
            current_regular: '',
            current_midterm: '',
            current_final: '',
            current_total: ''
        },
        computed: {
            page: {
                get: function () {
                    return this.my_page;
                },
                set: function (val) {
                    this.my_page = val;
                    var _this = this;
                    getApi('/api/grades', {
                        page: this.my_page
                    }, function (err, r) {
                        if (err) {
                            alert('Error paging: ' + err.message);
                        } else {
                            reloadArray(_this.classes, r);
                        }
                    });
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
            queryGrade: function () {
                var _this = this;
                getApi('/api/grades', {
                    page: this.page,
                    query: this.query,
                    criteria: this.criteria
                }, function (err, r) {
                    if (err) {
                        alert('Error query: ' + err.message);
                    } else {
                        reloadArray(_this.students, r);
                    }
                });
            },
            updateGradeInfo: function () {
                var _this = this;
                postApi('/api/admin/student', {
                    id: this.current_stu_id,
                    course_id: this.current_course_id,
                    regular: this.current_regular,
                    midterm: this.current_midterm,
                    final: this.current_final,
                    total: this.current_total
                }, function (err, r) {
                    if (err) {
                        alert('update error: ' + err.message);
                    } else {
                        _this.page = _this.page;
                    }
                });
            },
            showEditGradeInfo: function (grade) {
                if (grade) {
                    this.current_name = student.name;
                    this.current_major = student.major;
                    this.current_gender = student.gender;
                    this.current_stu_id = student.id;
                } else {
                    this.current_name = '';
                    this.current_major = '';
                    this.current_gender = '';
                    this.current_stu_id = '';
                }
                $('#edit-students').modal('show');
            }
        }
    });
}