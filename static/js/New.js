let is_auth = false,
    user_data = {},
    login = false;

window.onload = function () {
    const urlParams = new URLSearchParams(window.location.search),
        myParam = urlParams.get('token');

    if (myParam !== undefined && myParam !== null) {
        sendRequest(
            'POST',
            '/activate/'+myParam,
            true,
            null,
            function (data) {
                console.log(data);
                is_auth = true;
                user_data = data.data;
                AuthContent();
            },
            function (data) {
                console.log(data);
            }
        );
    }

    if (!is_auth) {
        sendRequest(
            'GET',
            '/api/users/me',
            true,
            null,
            function (data) {
                is_auth = true;
                user_data = data.data;
                AuthContent();
            },
            function (data) {
                console.log(data)
            }
        );
    }
};

function changeNavBar() {
    let friend_link = document.getElementById('friend_link'),
        upload_link = document.getElementById('upload_link'),
        message_link = document.getElementById('message_link'),
        profile_link = document.getElementById('profile_link');
    friend_link.style.display = 'block'
    upload_link.style.display = 'block';
    message_link.style.display = 'block';
    profile_link.onclick = function(){createPopUp('profile');};
}

function AuthContent() {
    changeNavBar();
}

function unAuthContent() {
    // todo: убирать блок плейлисты, выводить 20 рандомных треков, Будет доступен поиск иииии.... всё
}

function getCookie(name) {
	let matches = document.cookie.match(
	    new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)")
    );
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

function showPopUp(id_pop_up = 'pop_up') {
    let popup = document.getElementById(id_pop_up),
        body = document.getElementsByTagName('body')[0];
    popup.style.display = 'block';
    body.style.overflow = 'hidden';
}

function closePopUp(id_pop_up = 'pop_up') {
    let popup = document.getElementById(id_pop_up),
        body = document.getElementsByTagName('body')[0];
    popup.style.display = 'none';
    body.style.overflow = 'auto';
}

function profile_PopUp() {
    let pop_up_header = document.getElementById('pop_up_header'),
        pop_up_body = document.getElementById('pop_up_body')
    showPopUp('pop_up');
    pop_up_header.innerText = 'Профиль';
    pop_up_body.innerText = 'Тут типо тело';
}

function login_PopUp() {
    showPopUp('login_pop_up');
}

function change_to_login() {
    let label_on_reg_email = document.getElementById('label_on_reg_email'),
        label_on_reg_repeat_password = document.getElementById('label_on_reg_repeat_password'),
        button_submit_reg_log = document.getElementById('button_submit_reg_log'),
        info_reg_log = document.getElementById('info_reg_log'),
        header_log_reg = document.getElementById('header_log_reg');

    label_on_reg_email.style.display = (login) ? 'none' : 'flex';
    label_on_reg_repeat_password.style.display = (login) ? 'none' : 'flex';
    button_submit_reg_log.innerText = (login) ? 'Вход' : 'Регистрация';
    header_log_reg.innerText = (login) ? 'Вход' : 'Регистрация';
    // button_submit_reg_log.onclick = (login) ? function(){LogIn()} : function(){signUp()};
    info_reg_log.innerHTML = (login) ?  'Нет аккаунта? <span onclick="change_to_login()">Создать сейчас!</span>' : 'Уже есть аккаунт? <span onclick="change_to_login()">Войти!</span>';
    login = !login
}

function createPopUp(type = 'profile') {
    if (type === 'login') {
        login_PopUp();
    }
    if (type === 'profile') {
        profile_PopUp();
    }
}

function LogSign() {
    let input_login_login = document.getElementById('login'),
        input_password_login = document.getElementById('password'),
        input_email = document.getElementById('email'),
        input_password_repeat = document.getElementById('input_password_repeat_login');

    sendRequest(
        'POST',
        '/api/login',
        true,
        {"username": input_login_login.value, "password": input_password_login.value},
        function (data) {
            is_auth = true;
            user_data = data.data;
            AuthContent();
        }
    );
}

function signUp() {
    let input_password_repeat = document.getElementById('input_password_repeat_login'),
        input_email = document.getElementById('input_email_login'),
        input_login = document.getElementById('input_login_login'),
        input_password = document.getElementById('input_password_login');

    if (input_password_repeat.value !== input_password.value) {
        show_error('Пароли не совпадают', 'Ошибка');
    } else {
        sendRequest(
            'POST',
            '/api/signup',
            true,
            {"username": input_login.value, "password": input_password.value, "email": input_email.value},
            function (data) {
                let block_Login = document.getElementById('Login');
                block_Login.style.display = 'none';
                show_error(data.message,'Успех');
            }
        );
    }
}

function LogIn() {

}

function sendRequest(method, url, async=true, responses_data, onsuccess, onerror=function(){}) {
    let request = new XMLHttpRequest();
    request.open(method, url, async);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    if (responses_data != null) {
        request.send(JSON.stringify(responses_data));
    } else {
        request.send();
    }
    request.onload = function () {
        let responseObj = JSON.parse(request.response);

        if (request.status == 401) {
            console.log("Токен устарел, необходимо заново залогиниться");
            //show_error("Токен устарел, необходимо заново залогиниться", 'Ошибка');
        }

        if (request.status == 400 || request.status == 409) {
            show_error(responseObj.detail, 'Ошибка');
        }

        if (responseObj.result == true) {
            onsuccess(responseObj);
        } else {
            onerror(responseObj);
        }
    };

    request.onerror = function () {
        show_error('Не предвиденная ошибка, перезагрузите страницу', 'Ошибка');
    };

    request.ontimeout = function () {
        show_error('Не предвиденная ошибка, перезагрузите страницу', 'Ошибка');
    };

    request.onabort = function () {
        show_error('Не предвиденная ошибка, перезагрузите страницу', 'Ошибка');
    };
}
