$(document).ready(loginView);

function loginView() {
    var vm = new Vue({
        el: "#login-form",
        data: {
            username: '',
            password: '',
            type: 'student'
        },
        methods: {
            login: function () {
                if (this.username == '') {
                    return showError('Please enter username');
                }
                if (this.password == '') {
                    return showError('Please enter password');
                }

                createCookie('username', this.username);
                createCookie('password', this.password);
                createCookie('type', this.type);

                var result = auth();
                if (!result) {
                    return showError('用户名或密码错误');
                } else {
                    return location.assign(result + '.html');
                }

            }
        }
    })
}