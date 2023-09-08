let is_auth = false,
    user_data = {};

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

function showPopUp() {
    let popup = document.getElementById('pop_up'),
        body = document.getElementsByTagName('body')[0];
    popup.style.display = 'block';
    body.style.overflow = 'hidden';
}

function closePopUp() {
    let popup = document.getElementById('pop_up'),
        body = document.getElementsByTagName('body')[0];
    popup.style.display = 'none';
    body.style.overflow = 'auto';
}

function profile_PopUp() {
    let pop_up_header = document.getElementById('pop_up_header'),
        pop_up_body = document.getElementById('pop_up_body')
    showPopUp();
    pop_up_header.innerText = 'Профиль';
    pop_up_body.innerText = 'Тут типо тело';
}

function login_PopUp() {
    let login_pop_up = document.getElementById('login_pop_up');
    login_pop_up.style.display = 'block';
}

function createPopUp(type = 'profile') {
    if (type === 'login') {
        login_PopUp();
    }
    if (type === 'profile') {
        profile_PopUp();
    }
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
