/**
 * Created by Excelle on 11/7/16.
 */

function auth() {
    var username = getCookie('username');
    var password = getCached('password');
    var userType = getCookie('type');
    
    if (!username || !password || !userType) {
        return null;
    } else {
        if (userType == 'admin') {
            if (username == 'admin' && password == 'admin') {
                return 'admin'
            }
        } else if (userType == 'teacher') {
            if (username == 'teacher' && password == 'teacher') {
                return 'teacher'
            }
        } else if (userType == 'student') {
            if (username == '2014060101001' && password == 'student') {
                return 'students'
            }
        }
    }
    return null
}

function logout() {
    deleteCookie('username');
    deleteCookie('password');
    deleteCookie('type');

    location.assign('/login.html');
}
