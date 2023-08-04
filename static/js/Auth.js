function setDataCurrentUser(username, avatar) {
    let block_Login = document.getElementById('Login'),
        user_block = document.getElementById('user_block'),
        button_login_reg_block = document.getElementById('button_login_reg_block'),
        main_user_img = document.getElementById('main_user_img'),
        main_user_login = document.getElementById('main_user_login');
    block_Login.style.display = 'none';
    user_block.style.display = 'flex';
    button_login_reg_block.style.display = 'none';
    main_user_img.src = avatar;
    main_user_login.innerText = username;
}


function show_error(error_text, error_title) {
    let global_error_text = document.getElementById('global_error_text'),
        global_error = document.getElementById('global_error'),
        global_error_title = document.getElementById('global_error_title');

    global_error.style.display = 'block';
    global_error_title.innerText = error_title;
    global_error_text.innerText = error_text;
}

function change_to_login() {
    let pass_repeat = document.getElementById('pass_repeat_if_reg'),
        email_reg = document.getElementById('email_if_reg'),
        change_have_no_have_acc = document.getElementById('change_have_no_have_acc'),
        button_login_reg = document.getElementById('button_login_reg');

    pass_repeat.style.display = 'none';
    email_reg.style.display = 'none';
    change_have_no_have_acc.innerText = 'Нет аккаунта?';
    change_have_no_have_acc.onclick = function(){change_to_reg();};
    button_login_reg.innerText = 'Вход';
    button_login_reg.onclick = LogIn;
}

function change_to_reg() {
    let pass_repeat = document.getElementById('pass_repeat_if_reg'),
        email_reg = document.getElementById('email_if_reg'),
        change_have_no_have_acc = document.getElementById('change_have_no_have_acc'),
        button_login_reg = document.getElementById('button_login_reg');

    pass_repeat.style.display = 'flex';
    email_reg.style.display = 'flex';
    change_have_no_have_acc.innerText = 'Уже есть аккаунт?';
    change_have_no_have_acc.onclick = function(){change_to_login();};
    button_login_reg.innerText = 'Регистрация';
    button_login_reg.onclick = signUp;
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
    let input_login_login = document.getElementById('input_login_login'),
        input_password_login = document.getElementById('input_password_login');

    sendRequest(
        'POST',
        '/api/login',
        true,
        {"username": input_login_login.value, "password": input_password_login.value},
        function (data) {
            setDataCurrentUser(data.data.username, data.data.avatar);
        }
    );
}

function LogOut() {
    sendRequest(
        'POST',
        '/api/logout',
        true,
        {},
        function (data) {
            console.log(data);
            window.location.reload();
        },
        function (data) {
            console.log(data);
        }
    );
}
