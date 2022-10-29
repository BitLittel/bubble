/**
 * Created by linea on 22.10.2022.
 * by BitLittel
 */

function getCookie(name) {
	let matches = document.cookie.match(
	    new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)")
    );
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

function shuffle_array(array) {array.sort(() => Math.random() - 0.5);}

window.onload = function () {
    // установка глобальных переменных
    let audio = new Audio(),
        all_music = document.getElementsByClassName('blockMusic'),
        cur_time = document.getElementById('c_time'),
        time = document.getElementById('time'),
        line = document.getElementById('in_line'),
        list_playing_music = [],
        icon_play = document.getElementById('play'),
        volume = document.getElementById('volume'),
        backward = document.getElementById('backward'),
        forward = document.getElementById('forward'),
        time_line = document.getElementById('time-line'),
        song_name_dom = document.getElementById('song-name'),
        song_author_dom = document.getElementById('song_author'),
        loop_button = document.getElementById('loop'),
        shuffle_button = document.getElementById('shuffle'),
        play_cur_song = 0,
        cookie_value = getCookie('volume'),
        play_loop = false,
        play_random = false;

    for (let i = 0; i < all_music.length; i++) {list_playing_music.push(all_music[i]);}
    audio.volume = (cookie_value === undefined) ? 1 : (cookie_value/100);
    volume.style.backgroundSize = (cookie_value === undefined) ? '100% 100%' : cookie_value+'% 100%';
    volume.value = cookie_value;

    loop_button.onclick = function () {
        play_loop = !play_loop
        loop_button.src = play_loop ? '../static/img/loop_active.png' : '../static/img/loop.png'
    }

    shuffle_button.onclick = function () {
        play_random = !play_random;
        shuffle_button.src = play_random ? '../static/img/shuffle_active.png' : '../static/img/shuffle.png';
        if (play_random) {
            shuffle_array(list_playing_music);
        } else {
            list_playing_music = [];
            for (let i = 0; i <= all_music.length; i++) {list_playing_music.push(all_music[i]);}
        }
    }

    forward.onclick = function () {
        let number = ((play_cur_song+1) === list_playing_music.length) ? 0 : (play_cur_song+1);
        Play(number);
    }

    backward.onclick = function () {
        let number = ((play_cur_song-1) < 0) ? (list_playing_music.length-1) : (play_cur_song-1);
        Play(number);
    }

    /**
     * Play - Just Play Track
     * @param {Number} number - Next object DOM with Track
    **/

    function Play(number) {
        if (audio.src === '') {audio.src = list_playing_music[number].getAttribute('data-src');}
        if (list_playing_music[play_cur_song] === list_playing_music[number]) {
            list_playing_music[play_cur_song].children[2].style.display = audio.paused ? 'block' : 'none';
            list_playing_music[play_cur_song].style.background = '#0000003d';
        } else {
            list_playing_music[play_cur_song].children[2].style.display = 'none';
            list_playing_music[play_cur_song].style.background = 'none';
            list_playing_music[number].children[2].style.display = 'block';
            list_playing_music[number].style.background = '#0000003d';
            play_cur_song = number;
            audio.src = list_playing_music[play_cur_song].getAttribute('data-src');
        }
        icon_play.onclick = function(){Play(number);};
        if (audio.paused) {audio.play();}else{audio.pause();}
        icon_play.src = audio.paused ? '../static/img/play.png' : '../static/img/pause.png';
        song_name_dom.innerText = list_playing_music[number].getAttribute('data-name');
        song_author_dom.innerText = list_playing_music[number].getAttribute('data-author');
    }

    // тут audio забиваем собития
	audio.addEventListener('loadedmetadata', function(){
		time.innerHTML=''+(audio.duration/60>>0)+':'+(audio.duration%60>>0);
	});
	audio.addEventListener('timeupdate', function(){
		cur_time.innerHTML=(audio.currentTime/60>>0)+':'+((audio.currentTime%60>>0)<10?'0'+(audio.currentTime%60>>0):(audio.currentTime%60>>0));
		line.style.width=(audio.currentTime*100)/audio.duration+'%';
	});
	audio.addEventListener('ended', function (){
	    if (play_loop) {
            audio.duration = 0;
            audio.play();
        } else {
	        let number = ((play_cur_song+1) === list_playing_music.length) ? 0 : (play_cur_song+1);
            Play(number);
        }
	});

    volume.addEventListener('change', function (){
	    document.cookie = "volume="+volume.value+";max-age=2629743;SameSite=Strict";
	    volume.style.backgroundSize = volume.value+'% 100%';
	    audio.volume = volume.value/100;
    });
    time_line.onclick = function(){
		line.style.width=(((event.clientX-time_line.getBoundingClientRect().x)*100)/time_line.clientWidth)+'%';
		audio.currentTime=(audio.duration*(((event.clientX-time_line.getBoundingClientRect().x)*100)/time_line.clientWidth))/100;
	};

    for (let i = 0; i < all_music.length; i++) {
        all_music[i].onclick = function(){Play(i);};
    }

    icon_play.onclick = function(){Play(0);};

    song_name_dom.innerText = list_playing_music[0].getAttribute('data-name');
    song_author_dom.innerText = list_playing_music[0].getAttribute('data-author');
};