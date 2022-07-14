![CI workflow](https://github.com/gaps64/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram - Социальная сеть для обмена рецептами и поиска вкусняшек
## Доступен по адресу: http://gaps64.hopto.org/

Сервис позволяет пользователям создавать свои рецепты, делиться ими, подиписываться на рецепты других пользователей, и запоминать наиболее понравившиеся.  
Встроенный сервис продуктовой корзины позволяет сформировать список необходимых покупок на основе интересующих вас рецептов. Больше не надо запомнимать огромные списки продуктов, простов добавьте понравившийся рецепты в корзину и foodgram все сделает за Вас!

## Запуск проекта
Для начала установите репозитории Докера по данной [ссылке](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
Затем установите Docker и Docker-Compose

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Cоздать и сохраните переменные окружения в **.env** файл, пример:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```
Когда докер установлен скачайте файл docker-compose.yaml и выполните следую команду из директории с файлом
```bash
docker-compose up -d
```
Compose развернет 3 контейера
- backend собственно код foodgram
- postgres база данных постгрес
- nginx вэб сервер nginx отвественный за раздачу статики  

После запуска недобхоми провести миграции и собрать статику
```bash
sudo docker-compose exec -T backend python manage.py collectstatic --noinput
sudo docker-compose exec -T backend python manage.py makemigrations --noinput
sudo docker-compose exec -T backend python manage.py migrate --noinput
```
Закинуть тестовых данных 
```bash

docker-compose exec backend python manage.py collectstatic --noinput
```
Проект развернулся, наслаждайтесь и приятного апетита!
## Автор
- [Sergey K](https://github.com/gapa64)
