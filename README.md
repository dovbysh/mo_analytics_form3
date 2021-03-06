## О сервисе

Данное приложение реализует Форму-3 аналитики для МТА (выпуск автобусов по часам).
Приложение построено на открытой библиотеке Dash (языки Python, R, Julia), которая построена поверх графической библиотеке Plotly.js, обернуто с помощью python-фреймворка для создания web-сервисов Flask.

Проект имеет следующую структуру:
Исполняемые файлы:
- run.py — файл, запускающий приложение (app). Для запуска этого файла сделан Dockerfile_1. Приложение подглужает данные при перезагрузке страницы / изменении даты в календаре / выборе среза в фильтрах. Далее будет сделано автообновление страницы по заданном расписанию.
- get_data.py — файл, запускающий цикл обновления данных (запрос по api, обновление данных на диске) по расписанию. Для запуска этого файла сделан Dockerfile_2.
На данный момент для работы сервиса нужно запустить отдельно эти 2 файла. Далее, при необходимости, запуск можно совместить в один файл.

Внутренние пакеты и файлы:
- server.py - файл сервера для настроек работы логин/пароля, endpoint'ов health / readiness
- main_config.py - файл с конфигами для настройки обновления данных и других глобальных переменных
- index.py — главная страница, с которой происходит навигация пользователя на страницы логин/пароля/выхода/дашборда
- /pages - пакет, где описываются структуры страниц (layout) и описывается логика работа callback-функций для каждого визуального элемента + для специальных невидимых элементов на странице, которые отвечают за буферизацию данных для обмена между всеми визуалами (элемент dcc.Store)
- /data_prep — пакет для предобработки данных, полученных по api
- папка assets — специальная папка для Dash, где хранятся css файлы для дополнительной кастомизации визуалов (часть кастомизации выполняется в рамках созданий layout или самого визуала (fig)) -- этот файл override встроенные стили визуалов. Однако информация по стилям хранится и при иницилизации визуалов, и в css (неудобно, но особенность Dash -- внешний css не все может "затереть")

Конфигурационные файлы:
- config.py - создание engine базы данных (стороннее решение, требует оптимизации)
- config.txt - конфигурация базы данных (стороннее решение, требует оптимизации)
- users_mgt - файл управления пользователями для блока аутентификации (стороннее решение, требует оптимизации)

Файлы с данными:
- users.db - тестовая база данных для аутентификации
- data_archive.feather - архив данных для отчета за последние 10 (по умолчанию) дней
- fresh_data_dump.feather - обновленный архив, где последние 3 (по умолчанию) дня затираются каждые 2 минуты (по умолчанию) свежими данными




