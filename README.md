Разворачивание проекта на локальной машине - Linux.
1) sudo apt update && sudo apt -y upgrade
2) Установить pyenv
3) Установить версию python: pyenv install -v 3.9.6
4) Создание проекта с виртуальной средой и python определенной версии: 
pyenv virtualenv 3.9.6 fCoffee
5) Переходим в папку только что созданного проекта (путь пропишется в терминале)
так, чтобы вы находились в одном каталоге с папкой bin.
6) Активируем виртуальное окружение: source bin/activate
7) Устанавливаем python по умолчанию: pyenv local fCoffee
8) Проверяем версию python: pyenv versions && python3 -V
9) Устанавливаем postgres на систему по инструкции с официального сайта
postgresql.org
10) Ставим pgAdmin по инструкции с pgadmin.org
11) Ставим зависимости из файла requirements.txt - виртуальное окружение должно быть активно!(см.п.6)
pip install -r req.txt
12) В pycharm проверяем, чтобы в настройках проекта было выставлено правильный интерпретатор! (fCoffee)
13) Настройка postgres: djbook.ru/examples/77/ 
Логин и пароль можно взять из файла fCoffeeProject-settings.py
14) Перед работой с проектом нужно провести миграции из папки проекта:
    (в одной директории с manage.py)
python manage.py migrate
15) Запуск локального сервера: 
python manage.py runserver