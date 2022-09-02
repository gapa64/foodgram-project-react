![CI workflow](https://github.com/gapa64/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram - The social media for the recipes exchange and yummies searching.
## The project currently deployed [here](http://foodgram-gapa.ddns.net/)

Table of contents
- [Project Description](#project-description)
- [Project Installation](#install)
  - [Traditional Installation](#traditional-installation)
  - [CI/CD Installation](#ci-cd-installation)
    - [Ci/CD Prerequisites](#prerequisites)
    - [Configure Github Secrets](#configure-github-secrets)
    - [CI/CD Jobbs](#jobs)
- [Rest Api Examples](#rest-api-examples)
  - [Get list of Recipes](#get-list-of-recipes)
  - [Get list of recipes](#get-list-of-recipes)
  - [Get a single recipe](#get-a-single-recipe)
  - [Get list of users](#get-list-of-users)
  - [Register a new User](#register-a-new-user)
  - [Get Authentication Token](#get-authentication-token)

The project includes React JS frontend delivered by Yandex Practicum team and backend implemented by student.
Backend is developed with Django Rest Framework, so it also provides API interface for any third-party service integration.

##Project Description
Users may perform the following actions:
- Browse published recipes, filter by tag
- Create their own recipes
- Subscribe for recipes of particular Author
- add recipes to favorite.
- add recipes to the list of purchases.
- Download list of purchases grouped by ingredients

The solution consist of 3 running docker containers and one temproary container used with delpoyment
- db. Postgresql database
- backend. DRF backend with all the bussines logic
- nginx. Web servers responsible for requests handling
- frontend. The temproary container with React JS frontend delivered by yandex practicum team. All the data is copied to the nginx container during deployment.


## Install
Project requires Docker Engine and Docker compose plugin to be installed on server.
More details about Docker Instalation process [Here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
The instruction above was working at the moment of this document editing Aug 2022 for Ubuntu 18.04 LTS.
### Traditional Installation
1. Clone repository from github
```bash
git clone https://github.com/gapa64/foodgram-project-react
```
2. Create .env file with the following template in `foodgram-project-react` directory
```bash
cd foodgram-project-react
```
.env file template
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
INTERNAL_SUBNET=172.28.0.0/29
NGINX_IP=172.28.0.4
BACKEND_IP=172.28.0.3
DB_HOST=172.28.0.2
DB_PORT=5432
```
3. Start the project from foodgram-project-react/infra directory 
```bash
cd infra
sudo docker compose --env-file ../.env up -d
```
4. Setup project.  Run this command from `foodgram-project-react/infra` directory. 
   - Perform Database migrations
   - Collect static
   - Load fixtures if test data required
   - Create Django Admin SuperUser
```bash
sudo docker compose exec -T backend python manage.py makemigrations
sudo docker compose exec -T backend python manage.py migrate
sudo docker compose exec -T backend python manage.py collectstatic --no-input
sudo docker compose exec -T backend python manage.py loaddata fixtures/recipes.json
sudo docker compose exec -T backend python manage.py load_ingredients fixtures/ingredients.json
sudo docker exec -it backend python manage.py createsuperuser
```

### CI CD Installation
Github Actions provides an extensive toolset for a CI\CD  model impplementation.
#### Prerequisites
- Deploy VM in any public cloud provider
- Create [DockerHub](https://hub.docker.com/) Account
- [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) Foodgram, or [create a new repository from foodgram](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
- Generate RSA key for Github-Actions - VM communication. [How to example for Ubuntu](https://phoenixnap.com/kb/generate-setup-ssh-key-ubuntu)
- propagate public key to VM. Normally it's done during VM creation. If it's not done use the [following utility](https://www.ssh.com/academy/ssh/copy-id)
- [Create telegram bot](https://core.telegram.org/bots), and [telegram](https://telegram.org/) account If you need notifications of deployment process, otherwise remove send_message from github workflow.
- Figure out your chat id. E.g. use [get my id bot](https://t.me/getmyid_bot) 

#### Configure Github Secrets
Configure the following Secret attributes populated to the project during build, deployment and starting.  
More information about Github Secrets could be found  [Here](https://docs.github.com/en/rest/actions/secrets)

Parameter | Description
--- | --- 
HOST | Remote server where the project should be deployed
USER | User used by Github actions to deploy the project on a remote server
SSH_KEY | Copy private key of the USER
DB_ENGINE | django.db.backends.postgresql
INTERNAL_SUBNET | Subnet for inter container communication, 172.28.0.0/29
NGINX_IP | IP address for NGINX container, 172.28.0.4
BACKEND_IP | IP address for Container with Backend and django APP, 172.28.0.2
DB_HOST | IP address of github container 
DB_NAME | postgres by default 
DB_PORT | 5432 by default 
POSTGRES_PASSWORD | postgres by default 
POSTGRES_USER | postgres by default
DOCKER_USERNAME | username for an account at docker hub
DOCKER_PASSWORD | password for an account at docker hub
TELEGRAM_TO | Chat id to send notification
TELEGRAM_TOKEN | token of the bot which sends notifications

#### Jobs
Upon commit to master branch, the Github Actions run the following jobs:
- Tests. Performs Autotests for a backend code.
- build_and_push_to_docker_hub
  - Build Frontend image and push  it to Docker Hub
  - Build Backend image and push it to Docker Hub
- Deploy. Deploys the project on a server.
  - Copy infra directory with nginx configuration and docker-compose.yaml  to remote server
  - Populate .env file
  - Start the project with Docker Compose
  - Make and Apply migrations
  - Collect Static
  - Load Fixtures and test data
- send_message. Sends notification to telegram

### Rest API Calls example
[Entire API specification](#(http://foodgram-gapa.ddns.net/api/docs/))

Several examples:
- [Get list of recipes](#get-list-of-recipes)
- [Get a single recipe](#get-a-single-recipe)
- [Get list of users](#get-list-of-users)
- [Register a new User](#register-a-new-user)
- [Get Authentication Token](#get-authentication-token)
#### Get List of Recipes
`GET /api/recipes/`
```bash
Accept: application/json
```
Response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Thu, 25 Aug 2022 20:41:16 GMT
Content-Type: application/json
Content-Length: 6507
Connection: keep-alive
Vary: Accept, Origin
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "count": 10,
  "next": "http://gaps64.hopto.org/api/recipes/?page=2",
  "previous": null,
  "results": [
    {
      "id": 60,
      "author": {
        "first_name": "Ksenia",
        "last_name": "Ksyuhinovsky",
        "username": "Ksenich",
        "email": "deprof@rambler.ru",
        "id": 9
      },
      "ingredients": [
        {
          "id": 1927,
          "amount": 1000,
          "measurement_unit": "г",
          "name": "фарш (баранина и говядина)"
        },
        {
          "id": 1756,
          "amount": 250,
          "measurement_unit": "г",
          "name": "сухари панировочные"
        }
      ],
      "tags": [
        {
          "id": 3,
          "name": "dinner",
          "color": "00FF00",
          "slug": "dinner"
        },
        {
          "id": 2,
          "name": "lunch",
          "color": "FFFF00",
          "slug": "lunch"
        }
      ],
      "is_favorited": false,
      "is_in_shopping_cart": false,
      "name": "Homemade cutlets",
      "text": "Смешать в миске фарш, хлебные крошки, мелко нарезанные лук и чеснок. Добавить соль, перец по вкусу. Влить полстакана воды. Руками перемешать. Сформировать котлеты. Обжарить на растительном масле с даух сторон. Дать потушиться под крышкой на медленном огне 15 минут.",
      "cooking_time": 45,
      "pub_date": "2022-08-12T16:16:23.488741Z",
      "image": "http://gaps64.hopto.org/media/recipes_images/195fb1d7-6e96-4efc-a973-f3e28ca2309f.jpg"
    },
    {
      "id": 59,
      "author": {
        "first_name": "Ksenia",
        "last_name": "Ksyuhinovsky",
        "username": "Ksenich",
        "email": "deprof@rambler.ru",
        "id": 9
      },
      "ingredients": [
        {
          "id": 1068,
          "amount": 100,
          "measurement_unit": "г",
          "name": "морковь вареная"
        },
        {
          "id": 1440,
          "amount": 200,
          "measurement_unit": "г",
          "name": "редис"
        },
        {
          "id": 1152,
          "amount": 300,
          "measurement_unit": "г",
          "name": "огурцы"
        }
      ],
      "tags": [
        {
          "id": 3,
          "name": "dinner",
          "color": "00FF00",
          "slug": "dinner"
        },
        {
          "id": 2,
          "name": "lunch",
          "color": "FFFF00",
          "slug": "lunch"
        }
      ],
      "is_favorited": false,
      "is_in_shopping_cart": false,
      "name": "Okroshka",
      "text": "Отварить картошку, морковь и яйца, остудить. Нарезать все ингредиенты на мелкие кубики. Добавить мелко нарезанную зелень, соль и перец по вкусу. Заправить полученный салат сметаной и капелькой горчицы по вкусу. Залить квасом.",
      "cooking_time": 40,
      "pub_date": "2022-08-12T16:07:39.306641Z",
      "image": "http://gaps64.hopto.org/media/recipes_images/0c53c331-33e3-40ac-bdae-672a91690e08.jpg"
    }
  ]
}
```
#### Get a single recipe
`GET /api/recipes/60/`
```bash
Accept: application/json
```
Response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Tue, 30 Aug 2022 20:35:02 GMT
Content-Type: application/json
Content-Length: 1345
Connection: keep-alive
Vary: Accept, Origin
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "id": 60,
    "author": {
      "first_name": "Ksenia",
      "last_name": "Ksyuhinovsky",
      "username": "Ksenich",
      "email": "deprof@rambler.ru",
      "id": 9
    },
    "ingredients": [
      {
        "id": 1927,
        "amount": 1000,
        "measurement_unit": "г",
        "name": "фарш (баранина и говядина)"
      },
      {
        "id": 1756,
        "amount": 250,
        "measurement_unit": "г",
        "name": "сухари панировочные"
      },
      {
        "id": 892,
        "amount": 150,
        "measurement_unit": "по вкусу",
        "name": "лук белый"
      },
      {
        "id": 2069,
        "amount": 10,
        "measurement_unit": "г",
        "name": "чеснок"
      }
    ],
    "tags": [
      {
        "id": 3,
        "name": "dinner",
        "color": "00FF00",
        "slug": "dinner"
      },
      {
        "id": 2,
        "name": "lunch",
        "color": "FFFF00",
        "slug": "lunch"
      }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Homemade cutlets",
    "text": "Смешать в миске фарш, хлебные крошки, мелко нарезанные лук и чеснок. Добавить соль, перец по вкусу. Влить полстакана воды. Руками перемешать. Сформировать котлеты. Обжарить на растительном масле с даух сторон. Дать потушиться под крышкой на медленном огне 15 минут.",
    "cooking_time": 45,
    "pub_date": "2022-08-12T16:16:23.488741Z",
    "image": "http://gaps64.hopto.org/media/recipes_images/195fb1d7-6e96-4efc-a973-f3e28ca2309f.jpg"
}
```
#### Get list of users
`GET /api/users/`
```bash
Accept: application/json
```
Response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Fri, 02 Sep 2022 14:42:05 GMT
Content-Type: application/json
Content-Length: 771
Connection: keep-alive
Vary: Accept, Origin
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
```
Body
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "first_name": "Povareshka",
      "last_name": "Povarov",
      "username": "povar",
      "email": "povar@yamdb.ru",
      "id": 4,
      "is_subscribed": false
    },
    {
      "first_name": "Monika",
      "last_name": "Geller",
      "username": "chef",
      "email": "chef@yamdb.ru",
      "id": 5,
      "is_subscribed": false
    }
  ]
}
```
#### Register a new User
`POST /api/users/`
```bash
Content-Type: application/json
```
Body
```json
{
  "email": "user@yamdb.ru",
  "username": "user",
  "first_name": "User",
  "last_name": "Userberg",
  "password": "user123"
}
```
Response
```bash
HTTP/1.1 201 Created
Server: nginx
Date: Tue, 30 Aug 2022 21:32:30 GMT
Content-Type: application/json
Content-Length: 186
Connection: keep-alive
Vary: Accept, Origin
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "id":10,
  "first_name":"User",
  "last_name":"Userberg",
  "username":"user",
  "email":"user@yamdb.ru",
  "password":"pbkdf2_sha256$150000$BTl14W01af6Q$TWSCVaDQMYo2mmPsyyE7TNfT0l9C4ZKOGKRtkNO6lPM="
}
```
#### Get Authentication Token
`POST /api/auth/token/login/`
```bash
Content-Type: application/json
```
Body
```json
{
  "email": "user@yamdb.ru",
  "password": "user123"
}
```
Response
```bash
HTTP/1.1 200 OK
Server: nginx
Date: Tue, 30 Aug 2022 21:41:46 GMT
Content-Type: application/json
Content-Length: 57
Connection: keep-alive
Vary: Accept, Origin
Allow: POST, OPTIONS
X-Frame-Options: SAMEORIGIN
```
Body
```json
{
  "auth_token": "84ac97bd8bc864ea6c73e802178092b116a3777b"
}
```