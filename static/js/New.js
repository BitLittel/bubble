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
                unAuthContent();
            }
        );
    }
    setVolumeFromCookie();
};

function changeNavBar() {
    let friend_link = document.getElementById('friend_link'),
        upload_link = document.getElementById('upload_link'),
        message_link = document.getElementById('message_link'),
        profile_link = document.getElementById('profile_link'),
        profile_avatar = document.getElementById('profile_avatar'),
        user_login = document.getElementById('profile_login'),
        activiti_link = document.getElementById('activiti_link'),
        question_link = document.getElementById('question_link');
    friend_link.style.display = 'block'
    upload_link.style.display = 'block';
    message_link.style.display = 'block';
    activiti_link.style.display = 'block';
    question_link.style.display = 'block';
    profile_link.onclick = function(){createPopUp('profile');};
    profile_avatar.className = 'profile';
    user_login.innerText = user_data.username;
    profile_avatar.src = user_data.avatar;
}

function generatePlayLists(playlists) {
    let main_playlist = document.getElementById('playlists');

    main_playlist.style.display = 'flex';

    for (let i = 0; i < playlists.length; i++) {
        let div_blockPlayList = document.createElement('div'),
            img_cover = document.createElement('img'),
            span_name = document.createElement('span');
        div_blockPlayList.className = 'block_playlist';
        div_blockPlayList.onclick = function () {getMusicFromPlayList(playlists[i].id);};
        div_blockPlayList.appendChild(img_cover);
        img_cover.src = playlists[i].cover;
        img_cover.className = 'cover_playlist';
        img_cover.id = 'cover_playlist_' + playlists[i].id;
        div_blockPlayList.appendChild(span_name);
        span_name.className = 'title_playlist';
        span_name.innerText = playlists[i].name;
        main_playlist.firstChild.before(div_blockPlayList);

        if (i === 0) {
            getMusicFromPlayList(playlists[i].id);
        }
    }
}

function getMusicFromPlayList(playlist_id= 0) {
    let cover_playlist = document.getElementById('cover_playlist_'+playlist_id);
    // todo: Потом не забудь у предыдущего плейлиста убрать boxShadow
    cover_playlist.style.boxShadow = '0 0 10px';

    sendRequest(
        'GET',
        '/api/playlist/'+playlist_id,
        true,
        null,
        function (data) {
            console.log(data);
            InitMusic(data.data);
        },
        function (data) {
            console.log(data);
        }
    );
}

function getPlayLists() {
    sendRequest(
        'GET',
        '/api/playlist',
        true,
        null,
        function (data) {
            console.log(data);
            generatePlayLists(data.data);
        },
        function (data) {
            console.log(data);
        }
    );
}

function AuthContent() {
    changeNavBar();
    getPlayLists();
}

function unAuthContent() {
    getUnAuthMusics();
}

function getUnAuthMusics() {
    sendRequest(
        'GET',
        '/api/un_auth_playlist',
        true,
        null,
        function (data) {
            console.log(data);
            InitMusic(data.data);
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

function showPopUp(id_pop_up = 'pop_up') {
    let popup = document.getElementById(id_pop_up),
        body = document.getElementsByTagName('body')[0];
    popup.style.display = 'block';
    body.style.overflow = 'hidden';
}

function closePopUp(id_pop_up = 'pop_up') {
    let popup = document.getElementById(id_pop_up),
        body = document.getElementsByTagName('body')[0],
        all_pop_up = document.getElementsByClassName('background_pop_up'),
        check = false;
    popup.style.display = 'none';

    for (let i = 0; i < all_pop_up.length; i++) {
        if (all_pop_up[i].style.display === 'block') {
            check = false;
            break;
        } else {
            check = true;
        }
    }

    body.style.overflow = (check) ? 'auto' : 'hidden';
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
    info_reg_log.innerHTML = (login)
        ?  'Нет аккаунта? <span onclick="change_to_login()">Создать сейчас!</span>'
        : 'Уже есть аккаунт? <span onclick="change_to_login()">Войти!</span>';
    login = !login
}

function show_error(error=false, message='', header_text='') {
    let notification_pop_up = document.getElementById('notification_pop_up'),
        header_notification = document.getElementById('header_notification'),
        body_notification = document.getElementById('body_notification'),
        body = document.getElementsByTagName('body')[0];
    notification_pop_up.style.display = 'block';
    header_notification.innerText = header_text;
    body_notification.innerText = message;
    header_notification.style.color = (error) ? '#00c93e' : '#ff3a3a';
    body.style.overflow = 'hidden';
}

function createPopUp(type = 'profile') {
    if (type === 'login') {
        login_PopUp();
    }
    if (type === 'profile') {
        profile_PopUp();
    }
    if (type === 'upload') {
        upload_PopUp();
    }
}

function upload_PopUp(){
    // todo: закончить upload
    let pop_up_header = document.getElementById('pop_up_header'),
        pop_up_body = document.getElementById('pop_up_body');
    //pop_up_header.innerHTML = '';
    //pop_up_body.innerHTML = '';
    showPopUp('pop_up_upload');


    // let span_header = document.createElement('span');
    // pop_up_header.appendChild(span_header);
    // span_header.innerText = 'Загрузка треков';
    // span_header.style.fontSize = '2rem';
    //
    // let div_main_upload = document.createElement('div'),
    //     p_annotation = document.createElement('p'),
    //     input_upload = document.createElement('input'),
    //     button_upload = document.createElement('button'),
    //     div_list_uploaded = document.createElement('div');
    //
    // pop_up_body.appendChild(div_main_upload);
    //
    //     div_main_upload.appendChild(p_annotation);
    //     p_annotation.innerText = 'Выберите музыку которую необходимо загрузить. После начала загрузки, пожалуйста не закрывайте текущее окно, дождитесь полного окончания';
    //     div_main_upload.appendChild(input_upload);
    //         input_upload.name = 'music_file';
    //         input_upload.type = 'file';
    //         input_upload.accept = 'audio/*';
    //         input_upload.multiple = true;
    //         input_upload.id = 'music_file';
    //         input_upload.style = 'display: block; opacity: 0; position: absolute; z-index: -1; width: 0; height: 0;';
    //     div_main_upload.appendChild(button_upload);
    //         button_upload.onclick = function (){PrepareUpload();};
    //         button_upload.innerText = 'Выберите файлы';
    //     div_main_upload.appendChild(div_list_uploaded);
    //         div_list_uploaded.id = 'list_uploaded_music';
}

function LogSign() {
    let input_login_login = document.getElementById('login'),
        input_password_login = document.getElementById('password'),
        input_email = document.getElementById('email'),
        input_password_repeat = document.getElementById('password_repeat');

    if (!login) {
        sendRequest(
            'POST',
            '/api/login',
            true,
            {"username": input_login_login.value, "password": input_password_login.value},
            function (data) {
                is_auth = true;
                user_data = data.data;
                AuthContent();
                closePopUp('login_pop_up');
            },
            function (data) {
                show_error(false, data.detail, 'Ошибка');
            }
        );
    } else {
        if (input_password_repeat.value !== input_password_login.value) {
            show_error(false, 'Пароли не совпадают', 'Ошибка');
        } else {
            sendRequest(
                'POST',
                '/api/signup',
                true,
                {"username": input_login_login.value, "password": input_password_login.value, "email": input_email.value},
                function (data) {
                    show_error(true, data.message, 'Успех');
                },
                function (data) {
                    show_error(false, data.detail, 'Ошибка');
                }
            );
        }
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
