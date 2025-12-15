# CI/CD Pipeline для Docker образа

Проект демонстрирует полноценный CI/CD конвейер с комплексным тестированием Docker образа веб-приложения на FastAPI.

## Структура проекта

```
testirovanie/
├── app/                    # Исходный код приложения
│   ├── main.py            # FastAPI приложение
│   ├── models.py          # Модели данных
│   ├── routes.py          # API endpoints
│   └── services.py        # Бизнес-логика
├── tests/                 # Тесты
│   ├── unit/              # Unit тесты
│   ├── integration/       # Integration тесты
│   ├── e2e/               # End-to-end тесты
│   ├── performance/       # Performance тесты
│   └── docker/            # Docker тесты
├── .github/workflows/     # GitHub Actions workflows
└── Dockerfile             # Docker образ
```

## Возможности

- RESTful API для управления элементами
- Health check endpoints
- Полное покрытие тестами
- CI/CD конвейер с множеством этапов проверки

## Локальная разработка

### Установка зависимостей

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Запуск приложения

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

### Запуск тестов

```bash
# Все тесты
pytest

# Только unit тесты
pytest tests/unit/

# С покрытием кода
pytest --cov=app --cov-report=html
```

## Docker

### Сборка образа

```bash
docker build -t test-app:latest .
```

### Запуск контейнера

```bash
docker run -p 8000:8000 test-app:latest
```

## CI/CD Конвейер

GitHub Actions workflow включает следующие этапы:

1. **Lint и Code Quality** - проверка стиля кода (Black, Flake8, Pylint, MyPy)
2. **Unit Tests** - unit тесты с проверкой покрытия кода
3. **Security Scan** - сканирование безопасности (Safety, Bandit)
4. **Docker Build** - сборка Docker образа
5. **Docker Lint** - проверка Dockerfile (Hadolint)
6. **Docker Security** - сканирование Docker образа (Trivy)
7. **Docker Tests** - тесты Docker образа
8. **Integration Tests** - integration тесты
9. **Performance Tests** - performance тесты
10. **E2E Tests** - end-to-end тесты
11. **Deploy** - автоматический деплой при успешном прохождении всех тестов

## API Endpoints

- `GET /` - healthcheck
- `GET /health` - health status
- `GET /api/items/` - получить все элементы
- `POST /api/items/` - создать элемент
- `GET /api/items/{id}` - получить элемент по ID
- `DELETE /api/items/{id}` - удалить элемент

## Типы тестов

- **Unit тесты** - изолированные тесты функций и классов
- **Integration тесты** - тесты взаимодействия компонентов
- **E2E тесты** - полные пользовательские сценарии
- **Security тесты** - сканирование уязвимостей
- **Performance тесты** - нагрузочное тестирование
- **Docker тесты** - проверка образа и контейнера

## Требования

- Python 3.10+
- Docker
- Git