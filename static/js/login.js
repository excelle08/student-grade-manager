$(document).ready(loginView);

function loginView() {
    // Redirect to home if already logged in
    getApi('/api/user', {}, function (err, r) {
        if(r.uid) {
            return location.assign('/');
        }
    });

    var vm = new Vue({
        el: "#login-form",
        data: {
            username: '',
            password: '',
            type: 'student'
        },
        methods: {
            login: function () {
                var loginUrl = {
                    student: '/api/student',
                    teacher: '/api/teacher',
                    admin: '/api/admin'
                }

                if (this.username == '') {
                    return showError('Please enter username');
                }
                if (this.password == '') {
                    return showError('Please enter password');
                }

                postApi(loginUrl[this.type], {
                    username: this.username,
                    password: this.password,
                    remember: this.remember
                }, function (err, r) {
                    if (err) {
                        return showError(err.message);
                    } else {
                        return location.assign('/');
                    }
                });
            }
        }
    })
}