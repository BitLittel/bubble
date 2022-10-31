function SendTest() {
    AJAX(
        {
            url: '/api/v1/registration',
            data: {
                login: 'Glinomess',
                email: 'opera.operaciy@yandex.ru',
                password: 'GreenJS#1337',
                password_repeat: 'GreenJS#1337'
            }
        },
        function (data) {
            console.log(data);
        }
    );
}
