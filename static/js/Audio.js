/**
 * Created by BitLittel on 22.10.2022.
 **/

const theAudio = new Audio(),
	container_music_list_dom = document.getElementById('musics'),
	img_cover = document.getElementById('img_cover'),
	song_name = document.getElementById('song_name'),
	song_author = document.getElementById('song_author'),
	backward = document.getElementById('backward'),
	play = document.getElementById('play'),
	forward = document.getElementById('forward'),
	current_time_track = document.getElementById('c_time'),
	all_time_track = document.getElementById('time'),
	time_line = document.getElementById('time_line'),
	in_line = document.getElementById('in_line'),
	volume = document.getElementById('volume'),
	loop = document.getElementById('loop'),
	shuffle = document.getElementById('shuffle'),
	all_music = document.getElementsByClassName('music'),
	block_time_line_hold = document.getElementById('block_time_line_hold');

let max_track_number = 4,  // тут короче из ответа апи выдернуть максимальный номер трека
	current_index_track = 0,
	last_index_track = 0,
	array_index_track = [],
	current_track_number = 1,  // по дефолту всегда 1 будет
	on_loop = false,
	on_shuffle = false,
	cur_track_dom_element = 0,
	next_track_dom_element = 0;

function get_slowly_volume(value) {
	return (0.01*(Math.pow(value, 2))/100).toFixed(5)
}


function setVolumeFromCookie() {
	let get_volume = getCookie("volume"),
		volume_user = 50;
	volume_user = (get_volume === undefined) ? 50 : parseInt(get_volume);
	document.cookie = "volume="+volume_user+";max-age=2629743;SameSite=Strict";
	volume.value = volume_user;
    volume.style.backgroundSize = volume_user+'% 100%';
    theAudio.volume = get_slowly_volume(volume_user);
}

function generateRandomInteger(min, max) {return Math.floor(min + Math.random()*(max - min + 1))}

function createDomTrack(index_track, data_track_src, data_track_id, data_track_number, data_track_name, data_track_author, data_track_duration, data_track_cover, can_edit) {
	let div_music = document.createElement('div'),
		dic_cover_name_container = document.createElement('div'),
		img_music_cover = document.createElement('img'),
		div_music_title = document.createElement('div'),
		span_music_name = document.createElement('span'),
		span_music_author = document.createElement('span'),
		div_functions = document.createElement('div'),
		img_add_to_playlist = document.createElement('img'),
		img_download = document.createElement('img'),
		img_delete = document.createElement('img'),
		img_edit = document.createElement('img'),
		div_music_timing = document.createElement('div'),
		span_music_timing = document.createElement('span');

	div_music.className = "music";
	div_music.setAttribute("data-track-src", data_track_src);
	div_music.setAttribute("data-track-id", data_track_id);
	div_music.setAttribute("data-track-number", data_track_number);
	div_music.setAttribute("data-track-name", data_track_name);
	div_music.setAttribute("data-track-author", data_track_author);
	div_music.setAttribute("data-track-duration", data_track_duration);
	div_music.setAttribute("data-track-cover", data_track_cover);

	div_music.appendChild(dic_cover_name_container);
		dic_cover_name_container.className = 'cover_name_container';

		dic_cover_name_container.appendChild(img_music_cover);
			img_music_cover.className = 'music_cover';
			img_music_cover.onclick = function () {Play(index_track);};
			img_music_cover.src = '/static/img/default_img.jpg';
			img_music_cover.setAttribute('data-src', data_track_cover);

		dic_cover_name_container.appendChild(div_music_title);
			div_music_title.className = 'music_title title_playlist';

			div_music_title.appendChild(span_music_name);
				span_music_name.className = 'music_name';
				span_music_name.innerText = data_track_name;

			div_music_title.appendChild(span_music_author);
				span_music_author.className = 'music_author';
				span_music_author.innerText = data_track_author;

	div_music.appendChild(div_functions);
		div_functions.className = 'functions';
		div_functions.style.display = (!can_edit) ? 'none' : 'flex';

		div_functions.appendChild(img_add_to_playlist);
			img_add_to_playlist.src = '/static/img/add_to_playlist.svg';
			img_add_to_playlist.title = 'Добавить в плейлист';

		div_functions.appendChild(img_download);
			img_download.src = '/static/img/download.svg';
			img_download.title = 'Скачать трек';

		div_functions.appendChild(img_delete);
			img_delete.src = '/static/img/delete.svg';
			img_delete.title = 'Удалить трек';

		div_functions.appendChild(img_edit);
			img_edit.src = '/static/img/edit.svg';
			img_edit.title = 'Редактировать трек';

	div_music.appendChild(div_music_timing);
		div_music_timing.className = 'music_timing';

		div_music_timing.appendChild(span_music_timing);
			span_music_timing.innerText = data_track_duration;

	// set lazy load to cover track
	imageObserver.observe(img_music_cover);

	return div_music;
}

function getMusicOnIndex(index) {
	return all_music[array_index_track[index]];
}

function generateDefaultIndexArrayTrack() {
	array_index_track = [];
	for (let i = 0; i < max_track_number; i++) {
		array_index_track.push(i);
	}
}

function generateShuffledIndexArrayTrack(){
	let j, temp;
	for(let i = array_index_track.length - 1; i > 0; i--){
		j = Math.floor(Math.random()*(i + 1));
		temp = array_index_track[j];
		array_index_track[j] = array_index_track[i];
		array_index_track[i] = temp;
	}
}

function initMainPlayer(index, track_path, track_name, track_author, track_cover) {
	theAudio.src = track_path;
	theAudio.load();
	play.onclick = function(){Play(index);};
	song_name.innerText = track_name;
	song_author.innerText = track_author;
	img_cover.src = track_cover;
	cur_track_dom_element = getMusicOnIndex(index);
}

// вот в этот инит мы передадим response data
function InitMusic(objects_musics) {
	max_track_number = objects_musics.last_track_number;
	container_music_list_dom.innerHTML = "";
	for (let i = 0; i < objects_musics.track_list.length; i++) {
		container_music_list_dom.appendChild(
			createDomTrack(
				i,
				objects_musics.track_list[i].path,
				objects_musics.track_list[i].id,
				objects_musics.track_list[i].number,
				objects_musics.track_list[i].name,
				objects_musics.track_list[i].author,
				objects_musics.track_list[i].duration,
				objects_musics.track_list[i].cover,
				objects_musics.track_list[i].can_edit
			)
		);
	}
	generateDefaultIndexArrayTrack();
	initMainPlayer(
		0,
		objects_musics.track_list[0].path,
		objects_musics.track_list[0].name,
		objects_musics.track_list[0].author,
		objects_musics.track_list[0].cover
	);
}

/**
 * Play - Just Play Track
 * @param {Number} index - index track on dom blockMusic
**/

function Play(index) {
	next_track_dom_element = getMusicOnIndex(index);

    if (current_index_track === index) {
        cur_track_dom_element.style.background = '#0000003d';
    } else {
        cur_track_dom_element.style.background = '';
        next_track_dom_element.style.background = '#0000003d';
        theAudio.src = next_track_dom_element.getAttribute('data-track-src');
		cur_track_dom_element = next_track_dom_element
		current_index_track = index;
    }
    play.onclick = function(){Play(current_index_track);};
    if (theAudio.paused) {theAudio.play();} else {theAudio.pause();}

	navigator.mediaSession.metadata = new MediaMetadata({
		title: next_track_dom_element.getAttribute('data-track-name'),
		artist: next_track_dom_element.getAttribute('data-track-author'),
		album: 'Bubble',
		artwork: [{
			src: next_track_dom_element.getAttribute('data-track-cover'),
			sizes: "300x300",
			type: "image/jpeg",
      	}]
	});

    play.src = theAudio.paused ? '/static/img/play.svg' : '/static/img/pause.svg';
    img_cover.src = next_track_dom_element.getAttribute('data-track-cover');
    song_name.innerText = next_track_dom_element.getAttribute('data-track-name');
    song_author.innerText = next_track_dom_element.getAttribute('data-track-author');
}

function ChangeTrack(forward=true) {
	let buff_ = 0;

	if (forward) {
		buff_ = ((current_index_track+1) === max_track_number) ? 0 : (current_index_track+1);
	} else {
		buff_ = ((current_index_track-1) < 0) ? (max_track_number-1) : (current_index_track-1);
	}

	last_index_track = array_index_track[buff_]

	Play(buff_);
}

forward.onclick = function () {ChangeTrack(true)};
backward.onclick = function () {ChangeTrack(false)};
navigator.mediaSession.setActionHandler('previoustrack', function() {ChangeTrack(false)});
navigator.mediaSession.setActionHandler('nexttrack', function() {ChangeTrack(true)});


theAudio.addEventListener('ended', function (){
    if (on_loop) {
        theAudio.currentTime = 0;
        theAudio.play();
	} else {
		ChangeTrack(true);
	}
});

// theAudio.addEventListener("progress", () => {
// 	const duration = theAudio.duration;
//
// 	if (duration > 0) {
// 		for (let i = 0; i < theAudio.buffered.length; i++) {
// 			if (theAudio.buffered.start(theAudio.buffered.length - 1 - i) < theAudio.currentTime) {
// 				let buffered_time = (theAudio.buffered.end(theAudio.buffered.length - 1 - i) * 100) / duration
// 				console.log(buffered_time);
// 			break;
// 			}
// 		}
// 	}
// });

block_time_line_hold.addEventListener('touchmove', function (event) {
	changeProgress(event.changedTouches[0]);
});

block_time_line_hold.addEventListener('mousedown', function (event) {
	changeProgress(event);

});

function handler(event_) {
	changeProgress(event_)
}

block_time_line_hold.addEventListener('mousedown', function (event){
	block_time_line_hold.addEventListener('mousemove', handler);
});

block_time_line_hold.addEventListener('mouseup', function (event){
	block_time_line_hold.removeEventListener('mousemove', handler);
});

block_time_line_hold.addEventListener('mouseleave', function (event){
	block_time_line_hold.removeEventListener('mousemove', handler);
});

theAudio.addEventListener('loadedmetadata', function(){
    all_time_track.innerHTML=(theAudio.duration/60>>0)+':'+((theAudio.duration%60>>0)<10?'0'+(theAudio.duration%60>>0):(theAudio.duration%60>>0));
});

theAudio.addEventListener('timeupdate', function(){
    current_time_track.innerHTML=(theAudio.currentTime/60>>0)+':'+((theAudio.currentTime%60>>0)<10?'0'+(theAudio.currentTime%60>>0):(theAudio.currentTime%60>>0));
    in_line.style.width=(theAudio.currentTime*100)/theAudio.duration+'%';
});

// вешаем на полосу громкости эвенты, на изменение громкости и сохранение звука в куки
volume.addEventListener('change', function () {
    document.cookie = "volume="+volume.value+";max-age=2629743;SameSite=Strict";
    theAudio.volume = get_slowly_volume(volume.value);
});

function handleInputChange(e) {
	let target = e.target;
	if (e.target.type !== 'range') {target = volume}
	const min = target.min;
	const max = target.max;
	const val = target.value;
	target.style.backgroundSize = (val - min) * 100 / (max - min) + '% 100%';
	theAudio.volume = get_slowly_volume(target.value);
}

volume.addEventListener('input', handleInputChange);

// вешаем обработку на тайм-лайн
function changeProgress(event) {
	const cur_time = theAudio.currentTime,
		duration = theAudio.duration,
		buff_ = ((event.clientX-time_line.getBoundingClientRect().x)*100)/time_line.clientWidth;
	current_time_track.innerHTML=(cur_time/60>>0)+':'+((cur_time%60>>0)<10?'0'+(cur_time%60>>0):(cur_time%60>>0));
	in_line.style.width=buff_+'%';
	theAudio.currentTime = (duration*buff_)/100;
}

time_line.addEventListener('click', function (event) {changeProgress(event);});

loop.onclick = function () {
    on_loop = !on_loop;
	loop.style.filter = on_loop ? 'contrast(1)' : 'contrast(0.5)';
};

shuffle.onclick = function () {
	if (on_shuffle) {
		on_shuffle = false;
		shuffle.style.filter = 'contrast(0.5)';
		generateDefaultIndexArrayTrack();
		current_index_track = last_index_track;
	} else {
		on_shuffle = true;
		shuffle.style.filter = 'contrast(1)';
		generateShuffledIndexArrayTrack();
		last_index_track = current_index_track;
	}
};
