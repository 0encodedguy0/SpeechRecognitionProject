# Speech Recognition Project

Это проект для обработки речи с использованием **FastAPI** для бэкенда, **Celery** для асинхронной обработки задач, **Redis** в качестве брокера сообщений и **React** для фронтенда.

## Структура проекта

- **`backend/`** — папка с кодом для **FastAPI** (бэкенд).
- **`frontend/`** — папка с кодом для **React** (фронтенд).
- **`docker-compose.yml`** — конфигурация для Docker Compose, включающая все сервисы (бэкенд, фронтенд, Redis, PostgreSQL и Celery).
- **`requirements.txt`** — список зависимостей Python для проекта.
- **`Dockerfile`** — инструкции по созданию Docker образов для бэкенда и Celery.

## Установка

### 1. Клонирование репозитория

Сначала клонируйте репозиторий на вашу машину:

```bash
git clone https://your-repository-url.git
cd your-project-directory
```

### 2. Установка зависимостей

#### 2.1 Создание и активация виртуального окружения (для Python)

Для начала создайте виртуальное окружение и активируйте его:

Для Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

Для Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Затем установите все зависимости:
```bash
pip install -r requirements.txt
```

#### 2.2 Установка зависимостей для фронтенда

Перейдите в папку с фронтендом и установите зависимости:

```bash
cd frontend
npm install
```

### 3. Запуск с Docker Compose

Для запуска всех сервисов (бэкенд, фронтенд, Redis, Celery и Postgres) с использованием Docker Compose, выполните следующую команду:

```bash
docker-compose up —build
```

Эта команда создаст и запустит все контейнеры, настроит их взаимодействие и откроет порты:

 - **Бэкенд** будет доступен по адресу http://localhost:8000.
 - **Фронтенд** будет доступен по адресу http://localhost:3000.
 - **Redis** будет доступен по адресу localhost:6379.
 - **PostgreSQL** будет доступен по адресу localhost:5432.

### 4. Запуск проекта без Docker (опционально)

Если вы не хотите использовать Docker, можно запустить сервисы вручную:

#### 4.1. Запуск бэкенда (FastAPI)

Перейдите в папку с бэкендом и запустите сервер:

```bash
cd backend
uvicorn main:app —reload
```

#### 4.2. Запуск Celery

В другом терминале запустите рабочий процесс Celery:

```bash
celery -A backend.celery_worker worker —loglevel=info
```

#### 4.3. Запуск фронтенда (React)

Перейдите в папку с фронтендом и запустите приложение:

```bash
cd frontend
npm start
```

Фронтенд будет доступен по адресу http://localhost:3000.

### 5. Конфигурация .env
Для конфиденциальных данных (например, URL для Redis, настройки базы данных), можно создать файл .env в корне проекта. Пример:

```env
REDIS_URL=redis://localhost:6379/0
DB_HOST=localhost:5432
DB_USER=your_user
DB_PASSWORD=your_password
```

Загрузите эти переменные окружения с помощью python-dotenv в коде бэкенда.

## Использование

### 1. API Бэкенда
Приложение на FastAPI предоставляет несколько конечных точек для обработки запросов:

 - **POST** **`/api/speech-to-text/`** — преобразует аудиофайл в текст.
 - **GET** **`/api/status/`** — проверка статуса сервера.
Пример запроса:

```bash
curl -X 'POST' \
'http://localhost:8000/api/speech-to-text/' \
-H 'accept: application/json' \
-H 'Content-Type: multipart/form-data' \
-F 'file=@your_audio_file.wav'
```

### 2. Очередь задач с Celery
При отправке аудиофайлов на сервер, задача обработки может быть отправлена в очередь Celery, где она будет обрабатываться в фоне. Для этого контейнер Celery должен быть запущен и настроен на работу с Redis.

### 3. Структура данных
Бэкенд принимает аудиофайлы, которые могут быть в формате WAV, MP3 и других. Модель преобразует аудио в текст с использованием предобученной модели для русского языка (например, Vosk или Wav2Vec2).

## Тестирование

Для тестирования API можно использовать такие инструменты, как Postman или curl. Пример тестирования API для преобразования аудио в текст:

```bash
curl -X POST http://localhost:8000/api/speech-to-text/ -F "file=@your_audio_file.wav"
```
Для более детального тестирования, можно использовать фреймворк pytest.

## Примечания

 - Убедитесь, что у вас есть доступ к интернету для загрузки зависимостей и Docker образов.
 - В процессе работы с контейнерами Redis и PostgreSQL используйте пароли и доступы, которые определены в файле .env для большей безопасности.