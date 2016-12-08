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
            role: 'student'
        },
        methods: {
            login: function () {
                if (this.username == '') {
                    return showError('Please enter username');
                }
                if (this.password == '') {
                    return showError('Please enter password');
                }

                postApi('/api/user', {
                    username: this.username,
                    password: this.password,
                    role: this.role
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