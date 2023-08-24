let main_input_music_upload = document.getElementById('music_file'),
    button_select_upload_music = document.getElementById('button_select_upload_music'),
    list_uploaded_music = document.getElementById('list_uploaded_music'),
    count_all_file = 0,
    limit_uploading_file = 10,
    count_awaited_file = 0,
    count_processed_file = 0,
    count_finish_file = 0
    queue_file = [];

main_input_music_upload.addEventListener('change', UploadFile);

function PrepareUpload() {
    main_input_music_upload.click();
}

function ProcessingFile(index_, file_) {
    let request = new XMLHttpRequest(),
        formData = new FormData;
    request.open('POST', '/api/upload_file', true);
    //request.setRequestHeader("Content-Type", "multipart/form-data");

    formData.append('action', 'music');
    formData.append('file', file_);

    request.upload.onloadstart = function () {
        document.getElementById('status_loading_track_'+index_).innerText = '0%';
    };

    request.upload.onprogress = function (event) {
        console.log(event);
        console.log(request);
        let percents = ((event.loaded/event.total)*100).toFixed(2);
        console.log('processed: ', percents);
        document.getElementById('status_loading_track_'+index_).innerText = percents+'%';
    };

    request.upload.onloadend = function () {
        document.getElementById('status_yes_track_'+index_).style.display = 'block';
        document.getElementById('status_loading_track_'+index_).style.display = 'none';
    };

    request.onload = function () {
        let responseObj = JSON.parse(request.response);

        console.log(responseObj);

        if (request.status == 400 || request.status == 409) {
            show_error(responseObj.detail, 'Ошибка');
        }

        if (responseObj.result == true) {
            console.log(responseObj);
        } else {
            show_error(responseObj.detail, 'Ошибка');
        }
    };


    request.send(formData);



    // request.addEventListener('loadstart', (event) => {
    //     document.getElementById('status_loading_track_'+index_).innerText = '0%';
    // });

    // request.addEventListener('progress', (event) => {
    //     let percents = ((event.loaded/event.total)*100).toFixed(2);
    //     console.log('processed: ', percents);
    //     document.getElementById('status_loading_track_'+index_).innerText = percents+'%';
    // });

    // request.addEventListener('loadend', (event) => {
    //     document.getElementById('status_yes_track_'+index_).style.display = 'block';
    //     document.getElementById('status_loading_track_'+index_).style.display = 'none';
    // });


}

function generateDomUploadedTrack(index, name_track) {
    let div_uploaded_track = document.createElement('div'),
        img_cover_track = document.createElement('img'),
        span_name_track = document.createElement('span'),
        div_status = document.createElement('div'),
        img_status_yes = document.createElement('img'),
        span_status_loading = document.createElement('span');

    div_uploaded_track.className = 'uploaded_track';
    div_uploaded_track.id = 'track_'+index;
    div_uploaded_track.appendChild(img_cover_track);

    img_cover_track.className = 'default_img';
    img_cover_track.id = 'cover_track_'+index;
    img_cover_track.src = 'http://192.168.0.100:8000/api/image/1';

    div_uploaded_track.appendChild(span_name_track);
    span_name_track.id = 'name_track_'+index;
    span_name_track.innerText = name_track;

    div_uploaded_track.appendChild(div_status);

    div_status.appendChild(img_status_yes);
    img_status_yes.id = 'status_yes_track_'+index;
    img_status_yes.className = 'default_img';
    img_status_yes.style.display = 'none';
    img_status_yes.style.border = 'none';
    img_status_yes.src = '../static/img/yes.png';

    div_status.appendChild(span_status_loading);
    span_status_loading.id = 'status_loading_track_'+index;
    span_status_loading.style.display = 'block';
    span_status_loading.innerText = '0%';
    return div_uploaded_track
}

function UploadFile(e) {
    let target = e.target,
        files = target.files,
        counter_to_uploading = 0;
    button_select_upload_music.style.display = 'none';
    count_all_file = files.length;
    console.log(files);


    for (let i = 0; i < files.length; i++) {
        list_uploaded_music.appendChild(
            generateDomUploadedTrack(i, files[i].name)
        );
        // todo: реализовать очередь загрузки файлов.
        //if (limit_uploading_file !== counter_to_uploading) {
            ProcessingFile(i, files[i]);
        //}
    }
}