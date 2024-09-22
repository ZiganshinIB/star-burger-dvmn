# Сайт доставки еды Star Burger

Это [сайт](https://ziganshinproject.ru/), сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.


## Быстрый старт в Docker compose

### Клонируйте проект на свой локальный компьютер
```shell
git clone https://github.com/ZiganshinIB/star-burger-dvmn.git
cd star_burger_dvmn
```
### Создайте файл с переменными окружения `.env` в корневой каталог проекта
```bash
SECRET_KEY=django-insecure-0if40nf4nf93n4
YANDEX_API_KEY=610526f4-26ba-44c5-a498-a82f22d28d35
PG_USER=db_user
PG_PASSWORD=secret_password
PG_DB=db_name

```
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `YANDEX_API_KEY` — Получить токен  YANDEX_API_KEY можно получить по следующей ссылке https://developer.tech.yandex.ru/services/3
- `PG_USER` — имя пользователя базы данных (Опционально)
- `PG_PASSWORD` — пароль пользователя базы данных (Опционально)
- `PG_DB` — название базы данных (Опционально)
### Запустите проект в dev версии

```bash
docker compose -f docker-compose.dev.yaml up
```

### Запуск проекта в prod версии
Желательно добавить переменные среды в `.env`
```
ALLOWED_HOSTS=127.0.0.1,localhost
ROLLBAR_ACCESS_TOKEN=YOUR_ROLLBAR_ACCESS_TOKEN
ROLLBAR_NAME=YOUR_ROLLBAR_NAME
ROLLBAR_ENVIRONMENT=YOUR_ROLLBAR_ENVIRONMENT
```
Далее запускаем проект
```shell
docker compose -f docker-compose.prod.yaml up
```

## Быстрый старт в Docker
### Dev версия
Необходимо определить переменые среды

```
YANDEX_API_KEY=YOUR_YANDEX_API_KEY
SECRET_KEY=YOUR_SECRET_KEY
```
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `YANDEX_API_KEY` — Получить токен  YANDEX_API_KEY можно получить по следующей ссылке https://developer.tech.yandex.ru/services/3
Далее собрать образ (image) и запустить образ в контейнере:
```bash
docker build -f Dockerfile.dev -t star-burger:dev .
docker run --name star-burger-dev --env-file .env -p 8000:8000 -it star-burger:dev
```
### Prod версия
Необходимо определить переменые среды

```
YANDEX_API_KEY=YOUR_YANDEX_API_KEY
SECRET_KEY=YOUR_SECRET_KEY
ALLOWED_HOSTS=127.0.0.1,localhost
ROLLBAR_ACCESS_TOKEN=YOUR_ROLLBAR_ACCESS_TOKEN
ROLLBAR_NAME=YOUR_ROLLBAR_NAME
ROLLBAR_ENVIRONMENT=YOUR_ROLLBAR_ENVIRONMENT
```
Далее собрать образ (image) и запустить образ в контейнере:
```bash
docker build -f Dockerfile.prod -t star-burger:prod .
docker run --name star-burger-prod --env-file .env -p 80:8000 -it star-burger:prod
```
## Запуск проекта без Docker
### Как собрать бэкенд

Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger-dvmn
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv .venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\.venv\Scripts\activate`
- MacOS/Linux: `source .venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Определите переменную окружения `YANDEX_API_KEY`. Создать файл `.env` в каталоге `star_burger/` и положите туда такой код:
Для dev определите следующие переменные среды
```sh
export YANDEX_API_KEY=YOUR_YANDEX_API_KEY
```
- `YANDEX_API_KEY` — Получить токен  YANDEX_API_KEY можно получить по следующей ссылке https://developer.tech.yandex.ru/services/3


Создайте базy данных и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

### Собрать фронтенд

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver` откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что Node.js и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет их версии:

```sh
nodejs --version
# v16.16.0
# Если ошибка, попробуйте node:
node --version
# v16.16.0

npm --version
# 8.11.0
```

Версия `nodejs` должна быть не младше `10.0` и не старше `16.16`. Лучше ставьте `16.16.0`, её мы тестировали. Версия `npm` не важна. Как обновить Node.js читайте в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Перейдите в каталог проекта и установите пакеты Node.js:

```sh
cd star-burger-dvmn
npm ci --dev
```

Команда `npm ci` создаст каталог `node_modules` и установит туда пакеты Node.js. Получится аналог виртуального окружения как для Python, но для Node.js.

Помимо прочего будет установлен [Parcel](https://parceljs.org/) — это упаковщик веб-приложений, похожий на [Webpack](https://webpack.js.org/). В отличии от Webpack он прост в использовании и совсем не требует настроек.

Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Если вы на Windows, то вам нужна та же команда, только с другими слешами в путях:

```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд. О готовности вы узнаете по сообщению в консоли:

```
✨  Built in 10.89s
```

Parcel будет следить за файлами в каталоге `bundles-src`. Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует. Затем Parcel перейдёт в каждый из этих подключенных файлов и узнает что импортируют они. И так далее, пока не закончатся файлы. В итоге Parcel получит полный список зависимостей. Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`. Они полностью самодостаточны, и потому пригодны для запуска в браузере. Именно эти бандлы сервер отправит клиенту.

Зайдите на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/) вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда Parcel складывает результаты своей работы. Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория с помощью `.gitignore`.

### Запустите сайт
```shell
python manage.py runserver
```
http://127.0.0.1:8000

## Как запустить prod-версию сайта
Собрать фронтенд:
```shell
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```
Определите допольнительно следующие переменые среды
```shell
export SECRET_KEY=django-insecure
export DEBUG=false
export ALLOWED_HOSTS=HOST_NAME,HOST_IP,...
```
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `DEBUG` — дебаг-режим. Поставьте `False`.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)


# Дополнительные фичи
## Rollbar
Для отслеживание ошибок в коде веб-приложение можете использовать сервис Rollbar
Чтобы подключить его достаточно
1. Получить токен https://app.rollbar.com/
2. Вписать в переменные среды в Linux
```shell
export ROLLBAR_ACCESS_TOKEN=YOUR_ROLLBAR_ACCESS_TOKEN
```
и в файл `.env` прописать свойства среды для всех ошибок, чтобы указать, где они произошли.
```shell
export ROLLBAR_ENVIRONMENT=prod_star_burger
```

## Сервер СУБД
СУБД SQLite3 предоставляемая Django по умолчанию медленная рекомендуется подключить более быструю и надежную СУБД:
- MySQL
- PostgreSQL ([см. гайд как установить на Ubunto 20.04](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04))
Рекомендация
* Перед добовлением новой схемы выгрузите данные с текущего СУБД:
```shell
python manage.py dumpdata > data.json
```
Допишите в  файл `.env` следующую переменную среды
```shell
export DB_URL=YOUR_DB_URL
```
- `DB_URL` и как его прописат [документация](https://github.com/jazzband/dj-database-url)
Выпольните миграцию:
```shell
python manage.py migrate --run-syncdb
```

Если ранее выгружали данные в `data.json`, то загрузите их в новую СУБД:
```shell
python manage.py loaddata data.json
```
## Запуск на сервере
Для запуска серевера лучше использовать [`gunicorn`](https://gunicorn.org/#docs) и Nginx
[Гайд по установке Nginx](https://www.digitalocean.com/community/tutorials/nginx-ubuntu-18-04-ru)
Веб приложение теперь запускается следующей командой
```shell
gunicorn -b 127.0.0.1:8000
```
После запуска сконфигурируте `Nginx` в `/etc/nginx/sites-available/example.com`
```editorconfig
server {
    listen 80;
    listen [::]:80;
    location/media/ {
        alias  /opt/star-burger-dvmn/media/;
    }
    location /static/ {
        alias /opt/star-burger-dvmn/statics/;
    }
    location / {
        include '/etc/nginx/proxy_params';
        proxy_pass http://127.0.0.1:8000/;
    }
}
```
Выпольните команду:
```shell
ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
```
### Deploy (развертывавание)
Определите переменные среды, команды:
```shell
export ROLLBAR_ACCESS_TOKEN=ROLLBAR_ACCESS_TOKEN
export ROLLBAR_NAME='Ваше имя'
```
- Эти настройки необходимы что бы ввести запись в Rollbar

Сделайте файл `deploy_star_burger.sh` исполняемым, если он не является таковым
```shell
chmod ugo+x deploy_star_burger.sh
```
Запустите файл
```shell
./deploy_start_burger.sh
```
