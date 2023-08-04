let user_is_auth = false;

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
                setDataCurrentUser(data.data.username, data.data.avatar);
                user_is_auth = true;
            },
            function (data) {
                console.log(data);
            }
        );
        window.location = '/';
    } else {
        console.log("Всё круто!");
    }


    sendRequest(
        'GET',
        '/api/users/me',
        true,
        null,
        function (data) {
            setDataCurrentUser(data.data.username, data.data.avatar);
            user_is_auth = true;
            getAllUserData();
        },
        function (data) {
            console.log(data)
        }
    );
};

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

function getAllUserData() {
    setVolumeFromCookie();
    sendRequest(
        'GET',
        '/api/music_list_test',
        true,
        null,
        function (data) {
            console.log(data);
            InitMusic(data);
        },
        function (data) {
            console.log(data);
        }
    );
}

function getCookie(name) {
	let matches = document.cookie.match(
	    new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)")
    );
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

