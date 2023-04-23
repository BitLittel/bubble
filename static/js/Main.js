function api_login() {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/login?login=qwerty&password=password');
    request.setRequestHeader('token', '1234567');
    request.send();
    request.onload = function() {
        let responseObj = request.response;
        console.log(responseObj);
    };
    // AJAX(
    //     {
    //         url: '/api/login',
    //         data: {
    //             token: '1234567',
    //             login: document.getElementById('input_login_login').value,
    //             password: document.getElementById('input_password_login').value
    //         }
    //     },
    //     function (data) {
    //         console.log(data);
    //     }
    // );
}
