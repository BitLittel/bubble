/**
 * Created by BitLittel on 22.10.2022.
 **/



const theAudio = new Audio(), //document.getElementById('testAudio'),
	container_music_list_dom = document.getElementById('musics_list'),
	img_cover = document.getElementById('img_cover'),
	song_name = document.getElementById('song-name'),
	song_author = document.getElementById('song_author'),
	backward = document.getElementById('backward'),
	play = document.getElementById('play'),
	forward = document.getElementById('forward'),
	current_time_track = document.getElementById('c_time'),
	all_time_track = document.getElementById('time'),
	time_line = document.getElementById('time-line'),
	in_line = document.getElementById('in_line'),
	volume = document.getElementById('volume'),
	loop = document.getElementById('loop'),
	shuffle = document.getElementById('shuffle'),
	all_music = document.getElementsByClassName('blockMusic');

let max_track_number = 4,  // тут кароче из ответа апи выдернуть максимальный номер трека
	current_index_track = 0,
	array_index_track = [],
	current_track_number = 1,  // по дефолту всегда 1 будет
	on_loop = false,
	on_shuffle = false;


function getCookie(name) {
	let matches = document.cookie.match(
	    new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)")
    );
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setVolumeFromCookie() {
	let get_volume = getCookie("volume"),
		volume_user = 50;
	volume_user = (get_volume === undefined) ? 50 : parseInt(get_volume);
	document.cookie = "volume="+volume_user+";max-age=2629743;SameSite=Strict";
	volume.value = volume_user;
    volume.style.backgroundSize = volume_user+'% 100%';
    theAudio.volume = volume_user/100;
}

window.onload = function () {
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

function generateRandomInteger(min, max) {return Math.floor(min + Math.random()*(max - min + 1))}

function createDomTrack(index_track, data_track_src, data_track_id, data_track_number, data_track_name, data_track_author, data_track_duration, data_track_cover) {
	let div_blockMusic = document.createElement('div'),
		div_with_img_name_author = document.createElement('div'),
		img_cover_track = document.createElement('img'),
		div_with_name_author = document.createElement('div'),
		span_name = document.createElement('span'),
		span_author = document.createElement('span'),
		span_duration = document.createElement('span'),
		div_on_play = document.createElement('div');

	div_blockMusic.className = "blockMusic";
	div_blockMusic.setAttribute("data-track-src", data_track_src);
	div_blockMusic.setAttribute("data-track-id", data_track_id);
	div_blockMusic.setAttribute("data-track-number", data_track_number);
	div_blockMusic.setAttribute("data-track-name", data_track_name);
	div_blockMusic.setAttribute("data-track-author", data_track_author);
	div_blockMusic.setAttribute("data-track-duration", data_track_duration);
	div_blockMusic.setAttribute("data-track-cover", data_track_cover);
	div_blockMusic.onclick = function () {Play(index_track);};
	div_blockMusic.appendChild(div_with_img_name_author);
		div_with_img_name_author.appendChild(img_cover_track);
			img_cover_track.src = data_track_cover;
			img_cover_track.alt = data_track_author + " - " + data_track_name;
		div_with_img_name_author.appendChild(div_with_name_author);
			div_with_name_author.appendChild(span_name);
				span_name.innerText = data_track_name;
			div_with_name_author.appendChild(span_author);
				span_author.innerText = data_track_author;
	div_blockMusic.appendChild(span_duration);
		span_duration.innerText = data_track_duration;
	div_blockMusic.appendChild(div_on_play);
		div_on_play.className = "blockMusic_on_play";
		div_on_play.id = "blockMusic_on_play_"+index_track;
		div_on_play.style.display = "none";

	container_music_list_dom.appendChild(div_blockMusic);
	// return div_blockMusic;
}

function getMusicOnIndex(index) {
	return all_music[array_index_track[index]];
}

function generateDefaultIndexArrayTrack(max_number) {
	for (let i = 0; i < max_number; i++) {
		array_index_track.push(i);
	}
}

function generateShuffledIndexArrayTrack() {
	array_index_track.sort(() => Math.random() - 0.5);
}

function initMainPlayer(index, track_path, track_name, track_author, track_cover) {
	theAudio.src = track_path;
	theAudio.load();
	play.onclick = function(){Play(index);};
	song_name.innerText = track_name;
	song_author.innerText = track_author;
	img_cover.src = track_cover;
}

// вот в этот инит мы передадим response data
function InitMusic(objects_musics) {
	current_track_number = objects_musics.first_track_number;
	max_track_number = objects_musics.last_track_number;
	console.log(objects_musics.track_list, objects_musics.track_list.length);
	for (let i = 0; i < objects_musics.track_list.length; i++) {
		console.log(objects_musics.track_list[i]);
		createDomTrack(
			i,
			objects_musics.track_list[i].track_path,
			objects_musics.track_list[i].track_id,
			objects_musics.track_list[i].track_number,
			objects_musics.track_list[i].track_name,
			objects_musics.track_list[i].track_author,
			objects_musics.track_list[i].track_duration,
			objects_musics.track_list[i].track_cover,
		);
		if (objects_musics.track_list[i].track_number === current_track_number) {
			initMainPlayer(
				i,
				objects_musics.track_list[i].track_path,
				objects_musics.track_list[i].track_name,
				objects_musics.track_list[i].track_author,
				objects_musics.track_list[i].track_cover
			);
		}
	}
	generateDefaultIndexArrayTrack(max_track_number);
}

/**
 * Play - Just Play Track
 * @param {Number} index - index track on dom blockMusic
**/

function Play(index) {
	let get_cur_track_dom = getMusicOnIndex(current_index_track), //all_music[current_index_track],
		get_next_track_dom = getMusicOnIndex(index); //all_music[index];

    if (theAudio.src === '') {
		theAudio.src = get_cur_track_dom.getAttribute('data-track-src');
		theAudio.load();
	}
    if (current_index_track === index) {
		document.getElementById('blockMusic_on_play_'+index).style.display = theAudio.paused ? 'block' : 'none';
        get_cur_track_dom.style.background = '#0000003d';
    } else {
        document.getElementById('blockMusic_on_play_'+current_index_track).style.display = 'none';
        get_cur_track_dom.style.background = 'none';
        document.getElementById('blockMusic_on_play_'+index).style.display = 'block';
        get_next_track_dom.style.background = '#0000003d';
        theAudio.src = get_next_track_dom.getAttribute('data-track-src');
		// theAudio.load();
		current_index_track = index;
    }
    play.onclick = function(){Play(index);};
    if (theAudio.paused) {theAudio.play();} else {theAudio.pause();}
    play.src = theAudio.paused ? '../static/img/play.png' : '../static/img/pause.png';
    img_cover.src = get_next_track_dom.getAttribute('data-track-cover');
    song_name.innerText = get_next_track_dom.getAttribute('data-track-name');
    song_author.innerText = get_next_track_dom.getAttribute('data-track-author');
}


theAudio.addEventListener('ended', function (){
    if (on_loop) {
        theAudio.currentTime = 0;
        theAudio.play();
    } else if (on_shuffle) {
		// todo: переписать на индексы
		let random_number_track = generateRandomInteger(1, max_track_number);
		while (random_number_track === current_track_number) {
			random_number_track = generateRandomInteger(1, max_track_number);
		}
        Play(random_number_track);
	} else {
        Play(((current_index_track+1) === max_track_number) ? 0 : (current_index_track+1));
    }
});

theAudio.addEventListener('loadedmetadata', function(){
    all_time_track.innerHTML=''+(theAudio.duration/60>>0)+':'+(theAudio.duration%60>>0);
});

theAudio.addEventListener('timeupdate', function(){
    current_time_track.innerHTML=(theAudio.currentTime/60>>0)+':'+((theAudio.currentTime%60>>0)<10?'0'+(theAudio.currentTime%60>>0):(theAudio.currentTime%60>>0));
    in_line.style.width=(theAudio.currentTime*100)/theAudio.duration+'%';
});

forward.onclick = function () {
    Play(((current_index_track+1) === max_track_number) ? 0 : (current_index_track+1));
}

backward.onclick = function () {
    Play(((current_index_track-1) < 0) ? (max_track_number-1) : (current_index_track-1));
}

// вешаем на полосу громкости эвент, на изменение громкости и сохранение звука в куки
// todo: сделать логорифмическое изменение громкости, иногда так хочется чтобы было намного потише
volume.addEventListener('change', function () {
    document.cookie = "volume="+volume.value+";max-age=2629743;SameSite=Strict";
    volume.style.backgroundSize = volume.value+'% 100%';
    theAudio.volume = volume.value/100;
});

//theAudio.onplay = function () {console.log(theAudio.currentTime)};

// вешаем обработку на тайм-лайн

// theAudio.addEventListener('canplay', function () {console.log("canplay");})
// theAudio.addEventListener('loadedmetadata',()=>{console.log("metadataloaded");});
// theAudio.addEventListener('loadeddata',()=>{console.log("dataloaded");});
// theAudio.addEventListener('canplaythrough',()=>{console.log("canplaythrough");});

function changeProgress() {
	const cur_time = theAudio.currentTime,
		duration = theAudio.duration,
		buff_ = ((event.clientX-time_line.getBoundingClientRect().x)*100)/time_line.clientWidth;
	current_time_track.innerHTML=(cur_time/60>>0)+':'+((cur_time%60>>0)<10?'0'+(cur_time%60>>0):(cur_time%60>>0));
	in_line.style.width=buff_+'%';
    // in_line.style.width=(cur_time*100)/duration+'%';
	theAudio.currentTime = (duration*buff_)/100;
}

time_line.addEventListener('click', function () {
	changeProgress();
});

// time_line.addEventListener('click', function () {
//     //console.log(audio.currentTime, audio.duration, event.clientX, time_line.getBoundingClientRect().x, time_line.clientWidth);
//     //console.log((audio.duration*(((event.clientX-time_line.getBoundingClientRect().x)*100)/time_line.clientWidth))/100);
//     //in_line.style.width=(((event.clientX-time_line.getBoundingClientRect().x)*100)/time_line.clientWidth)+'%';
//     //let set_time = ((audio.duration*(((event.clientX-time_line.getBoundingClientRect().x)*100)/time_line.clientWidth))/100);
//     //console.log(set_time, isFinite(set_time));
//     //audio.currentTime=Math.floor(set_time);
// 	console.log(audio.currentTime);
//     audio.currentTime=5;
// 	console.log(audio.currentTime);
// 	//audio.duration = 10;
// });

loop.onclick = function () {
    on_loop = !on_loop;
    loop.src = on_loop ? '../static/img/loop_active.png' : '../static/img/loop.png';
}
//
// shuffle_button.onclick = function () {
//     play_random = !play_random;
//     shuffle_button.src = play_random ? '../static/img/shuffle_active.png' : '../static/img/shuffle.png';
//     if (play_random) {
//         shuffle_array(list_playing_music);
//     } else {
//         list_playing_music = [];
//         for (let i = 0; i <= all_music.length; i++) {list_playing_music.push(all_music[i]);}
//     }
// }
