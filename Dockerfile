# говорим что используем питон как базовый образ
FROM python:3.10
# подписываем(не обязательно)
LABEL authors="BitLittel"
# запускаем, тут мы создаём дерикторию внутри контейнера под наше приложение
RUN mkdir -p /bubble
# создаём дериктории под файлы пользователей
RUN mkdir -p /bubble/stored_files
RUN mkdir -p /bubble/stored_files/musics
RUN mkdir -p /bubble/stored_files/photos
# устанавливаем рабочую дерикторию только что созданную папку и как бы сразу входим в неё
WORKDIR /bubble
# копируем все файлы нашего проекта в нашё папку
COPY . /bubble
# запускаем, выдаём право на запуск баш скрипта(если не сделать то нас пошлют куда по дальше)
RUN chmod +x start.sh
# запускаем. через пип устанавливаем все пакеты которые прописаны в рекваирементс файле
RUN pip install --no-cache-dir --no-color --no-python-version-warning --disable-pip-version-check -r requirements.txt
# открываем порт 8000
# EXPOSE 8000

# CMD ["sh", "start.sh"]