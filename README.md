# Домашнее задание №2. Docker & docker-compose

Все сервисы соединяются по macvlan, сервис API также подключен к дефолтной bridge сети для доступа с хост машины.
Все параметры хранятся в файле .env, он используется как конфигурационный файл.
Параметры macvlan: parent=enp1s0f1, subnet="172.19.0.0/16", возможно для запуска на другой машине нужно будет их поменять в файле docker-compose.yml

Реализованы 3 сервиса:
##### 1. Сервер базы данных PostgreSQL. 
Запускается первым и ожидает запросов, запускается в macvlan сети на дефолтном порту (5432)
##### 2. Сервиc для инициализации базы данных. 
Ждет запуска БД, подключается к БД, создает в ней таблицу data и добавляет в нее данные из csv файла. Папка с файлом csv примонтированна как readonly volume.
##### 3. Сервис API.
Реализован на Flask. Ждет запуска БД, затем обслуживает запросы на 2х endpoint'ах: 
- / - отдает записанные данные из БД в JSON формате, статус ответа 200
- /health - возвращает пустой ответ со статусом 20

На всех остальных endpoint'ах возвращает ответ {"error":"Not found"} со статусом 404
Для подключения к API нужно использовать порт 1234
```
curl -v localhost:1234
```
```
*   Trying 127.0.0.1:1234...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 1234 (#0)
> GET / HTTP/1.1
> Host: localhost:1234
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 37
< Server: Werkzeug/1.0.1 Python/3.9.0
< Date: Mon, 26 Oct 2020 22:57:07 GMT
< 
[["Change",1],["from",2],["host",3]]
* Closing connection 0
```
```
curl -v localhost:1234/health
```
```
*   Trying 127.0.0.1:1234...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 1234 (#0)
> GET /health HTTP/1.1
> Host: localhost:1234
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: text/html; charset=utf-8
< Content-Length: 0
< Server: Werkzeug/1.0.1 Python/3.9.0
< Date: Mon, 26 Oct 2020 22:58:59 GMT
< 
* Closing connection 0
```
```
curl -v localhost:1234/something/else
```
```
*   Trying 127.0.0.1:1234...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 1234 (#0)
> GET /something/else HTTP/1.1
> Host: localhost:1234
> User-Agent: curl/7.68.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
* HTTP 1.0, assume close after body
< HTTP/1.0 404 NOT FOUND
< Content-Type: application/json
< Content-Length: 22
< Server: Werkzeug/1.0.1 Python/3.9.0
< Date: Mon, 26 Oct 2020 22:58:45 GMT
< 
* Closing connection 0
{"error": "Not found"}
```
