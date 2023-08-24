let main_friend = document.getElementById('friends'),
    list_friends = document.getElementById('list_friends');

function generateFriendsList(data_friends) {
    main_friend.style.display = 'block';
    list_friends.innerHTML = '';
    if (!data_friends) {
        /*
        <div>
            <img src="../static/img/default_img.jpg" alt="#">
            <div>
                <span style="display: flex;align-content: center;align-items: center;">
                    <img src="../static/img/gem_green.png" alt="" style="width: 12px; height: 12px;">
                    <span>UserLogin_Name</span>
                </span>
                <span>1337 аудиозаписи</span>
            </div>
        </div>
        */
        console.log(data_friends);
    } else {
        list_friends.innerHTML = '<p>У вас пока нет друзей(</p>';
    }
}


function getFriends() {
    sendRequest(
        'GET',
        '/api/friends',
        true,
        null,
        function (data) {
            console.log(data);
            generateFriendsList(data.data.friends);
        },
        function (data) {
            console.log(data);
        }
    );
}
