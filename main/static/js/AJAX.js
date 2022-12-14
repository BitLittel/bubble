/**
 * Created by linea on 12.06.2017.
 * by Vladis
 */


/**
 * Получение и отправка данных AJAX
 * @param {Object} data Параметры запроса
 *   @param {String} [data.url=document.location] URL запроса
 *   @param {String} [data.method="GET"] Метод запроса (GET или POST]
 *   @param {String} [data.dataType="json"] Формат получаемых данных
 *   @param {(Object|String)} data.data Данные запроса в виде объекта или сериализованной строки
 *   @param {Boolean} [data.async=true] Выполнить запрос асинхронно
 * @param {Function} [onsuccess] Функция, вызываемая в случае успешного запроса
 * @param {Function} [onerror] Функция, вызываемая при ошибке
 *
 * @author nomnes
 * @version 0.1
 */
var AJAX = function(data, onsuccess, onerror){
    if (!data) {
        data = {};
    }
    data.url = data.url || document.location;
    data.method = data.method || 'GET';
    data.dataType = data.dataType || 'json';
    data.data = data.data || false;
    data.async = typeof data.async == 'boolean' ? data.async : true;

    data.method = data.method.toUpperCase();

    function sender() {
        var request = new XMLHttpRequest();
        // обработка ответа
        request.onload = function() {
            if (request.status >= 200 && request.status < 400) {
                // выполнить при получении данных
                if (onsuccess) {
                    var result;
                    if (data.dataType.toLowerCase() == 'json') {
                        // парсинг JSON в объект
                        result = JSON.parse(request.responseText);
                    } else {
                        // удаление комментариев из html
                        var re = /<!--.*?-->/g;
                        result = request.responseText;
                        result = result.replace(re, '');
                    }
                    // пользовательская функция обработки данных
                    onsuccess(result);
                }
            } else {
                // выполнить при ошибке получения данных
                if (onerror) {
                    onerror(request.status);
                }
            }
        };
        var num = 0;
        request.onerror = function() {
            // выполнить при ошибке запроса
            if (onerror) {
                onerror(request.status);
            } else {
                if (num < 10) {
                    sender();
                }
            }
        };
        if (data.data) {
            // если есть данные для отправки
            var body = '';
            if (typeof(data.data) == "object") {
                // сериализация данных
                body = Object.keys(data.data).map(function(key) {
                    return key + '=' + encodeURIComponent(data.data[key]);
                }).join('&');
            } else {
                body = data.data;
            }
            if (data.method == 'POST') {
                // отправка методом POST
                request.open('POST', data.url, true);
                request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                request.send(body);
            } else {
                // отправка методом GET
                request.open('GET', data.url + '?' + body, true);
                request.send();
            }
        } else {
            // отправка пустого запроса
            request.open(data.method, data.url, data.async);
            request.send();
        }
    }
    sender();
};
