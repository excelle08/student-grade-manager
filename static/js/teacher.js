$(document).ready(loadTeacherView);

function loadTeacherView () {
    var params = getArgs();

    getApi('/api/teacher', {}, function (err, teacher) {
        if (err) {
            alert('Error loading teacher info. - ' + err.message);
        } else {
            getApi('/api/teacher/class', {
                page: params.page || 1
            }, function (err, classes) {
                if (err) {
                    alert('Error loading classes. - ' + err.message);
                } else {
                    gradeView(classes);
                    ratingView(classes);
                    infoView(teacher);
                }
            });
        }
    });
}

function gradeView (classes) {
    var vm = new Vue({
        el: '#grades',
        data: {
            classes: classes,
            my_page: 1,
            students: []
        },
        computed: {
            page: {
                get: function () {
                    return this.my_page;
                },
                set: function (val) {
                    this.my_page = val;
                    var _this = this;
                    getApi('/api/teacher/class', {
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
            setGrade: function (_class) {
                $('#modal-set-grade').modal('show');
                getApi('/api/grades', {

                })
            },
            displayStat: function (_class) {
                $('#modal-visualize-grade').modal('show');
            },
            editStuGrade: function (student) {
                
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
                    var _this = this;
                    getApi('/api/teacher/class', {
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
            displayRatingStat: function (_class) {
                $('#modal-visualize-ratings').modal('show');
            }
        }
    });
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
                postApi('/api/teacher', {
                    id: this.teacher_id,
                    address: this.address,
                    telephone: this.telephone,
                    email: this.email,
                    intro: this.intro
                }, function (err, r) {
                    if (err) {
                        alert('Error: ' + err.message);
                    } else {
                        alert('修改成功！');
                    }
                });
            }
        }
    })
}