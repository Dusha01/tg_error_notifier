# 🧩 TG Error Notifier

**TG Error Notifier** — библиотека для отправки уведомлений об ошибках и системных событиях через **Telegram** в Python-приложениях.

---

## 🌟 Особенности

- **Многоуровневое логирование** — INFO, WARNING, ERROR, CRITICAL  
- **Категоризация ошибок** — разбивка по модулям системы  
- **Telegram уведомления** — мгновенные оповещения в чат  
- **Готовые декораторы** — автоматическая обработка ошибок  
- **Шаблоны уведомлений** — стандартные сообщения для типовых событий  
- **Асинхронная архитектура** — не блокирует основное приложение  

---

## 📦 Установка

### Из исходного кода

```bash
git clone <repository-url>
cd tg-error-notifier
pip install -e .
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## 🚀 Быстрый старт

### Базовая настройка

```python
from tg_error_notifier import ErrorManager, TelegramNotifierConfig
from tg_error_notifier.models.error_models import ErrorCategory

config = TelegramNotifierConfig(
    admin_bot_token="YOUR_BOT_TOKEN",
    notification_chat_id="YOUR_CHAT_ID",
    app_name="MyAwesomeApp"
)

error_manager = ErrorManager.configure(config)

await ErrorManager.notify_info(
    ErrorCategory.SYSTEM, 
    "Приложение запущено успешно"
)
```

### Использование декораторов

```python
from tg_error_notifier.decorators import handle_database_errors, handle_telegram_errors

@handle_database_errors("создание пользователя")
async def create_user(user_data):
    pass

@handle_telegram_errors("отправка сообщения")
async def send_telegram_message(chat_id, text):
    pass
```

### Готовые шаблоны уведомлений

```python
from tg_error_notifier.templates import NotificationTemplates

await NotificationTemplates.bot_started("Мой Бот")
await NotificationTemplates.bot_stopped("Мой Бот")

await NotificationTemplates.database_connected()
await NotificationTemplates.database_slow()

await NotificationTemplates.user_registered("12345", "john_doe")
```

---

## ⚙️ Конфигурация

### Параметры конфигурации

```python
config = TelegramNotifierConfig(
    admin_bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
    notification_chat_id="-1001234567890",
    app_name="My Application",
    enable_logging=True,
    log_level="INFO",
    parse_mode="Markdown",
    disable_notifications=False,
    max_message_length=4096
)
```

### Получение Chat ID

1. Создайте бота через [@BotFather](https://t.me/BotFather)  
2. Добавьте его в нужный чат/канал  
3. Отправьте любое сообщение  
4. Выполните:
   ```bash
   curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
5. Найдите `chat.id` в ответе  

---

## 📋 Модели данных

### Уровни ошибок

```python
from tg_error_notifier.models import ErrorLevel

ErrorLevel.INFO
ErrorLevel.WARNING
ErrorLevel.ERROR
ErrorLevel.CRITICAL
```

### Категории ошибок

```python
from tg_error_notifier.models import ErrorCategory

ErrorCategory.DATABASE
ErrorCategory.TELEGRAM
ErrorCategory.API
ErrorCategory.CACHE
ErrorCategory.AUTH
ErrorCategory.SCHEDULE
ErrorCategory.SYSTEM
ErrorCategory.NETWORK
ErrorCategory.VALIDATION
ErrorCategory.EXTERNAL_SERVICE
```

---

## 🔧 Расширенное использование

### Работа с ErrorManager

```python
await ErrorManager.notify_info(ErrorCategory.SYSTEM, "Задача выполнена успешно")
await ErrorManager.notify_warning(ErrorCategory.CACHE, "Кэш почти заполнен")

try:
    ...
except Exception as e:
    await ErrorManager.notify_error(
        ErrorCategory.DATABASE,
        "Ошибка при сохранении данных",
        {"table": "users"},
        e
    )
```

### Кастомные уведомления

```python
from tg_error_notifier.models import ErrorNotification, ErrorLevel, ErrorCategory
from datetime import datetime

notification = ErrorNotification(
    level=ErrorLevel.ERROR,
    category=ErrorCategory.API,
    message="Сервис недоступен",
    details={
        "service": "payment_gateway",
        "endpoint": "/api/v1/process",
        "status_code": 503
    },
    timestamp=datetime.now()
)

await error_manager.send_notification(notification)
```

---

## 🎨 Декораторы

### Универсальный

```python
from tg_error_notifier.decorators import handle_errors

@handle_errors(ErrorCategory.API, "обработка платежа")
async def process_payment(payment_data):
    pass
```

### Специализированные

```python
from tg_error_notifier.decorators import (
    handle_database_errors,
    handle_telegram_errors,
    handle_cache_errors,
    handle_system_errors,
    handle_api_errors,
    handle_auth_errors
)
```

---

## 📊 Шаблоны уведомлений

```python
await NotificationTemplates.bot_started("Мой Telegram Бот")
await NotificationTemplates.database_connected()
await NotificationTemplates.high_load_warning("Database", 85)
```

---

## 🔒 Обработка исключений

### Глобальная обработка ошибок

```python
import asyncio
from tg_error_notifier import ErrorManager, ErrorCategory

async def main():
    try:
        await run_application()
    except Exception as e:
        await ErrorManager.notify_critical(
            ErrorCategory.SYSTEM,
            "Необработанное исключение в приложении",
            exc=e
        )
        raise

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🛠️ Разработка

### Структура проекта

```
tg_error_notifier/
├── core/
│   ├── error_manager.py
│   ├── error_notification.py
│   └── config.py
├── decorators/
│   └── error_decorators.py
├── models/
│   ├── error_models.py
│   └── notification_models.py
├── templates/
│   └── notification_templates.py
├── requirements.txt
└── setup.py
```

### Локальная разработка

```bash
git clone <repository-url>
cd tg-error-notifier
pip install -e .
python -m pytest tests/
```

---

## 📝 Пример полной интеграции

```python
import os
import asyncio
from tg_error_notifier import (
    ErrorManager, 
    TelegramNotifierConfig,
    NotificationTemplates,
    handle_database_errors,
    handle_telegram_errors
)

class MyTelegramBot:
    def __init__(self):
        self.setup_error_handling()
    
    def setup_error_handling(self):
        config = TelegramNotifierConfig(
            admin_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            notification_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            app_name="Telegram Bot",
            enable_logging=True,
            log_level="INFO"
        )
        self.error_manager = ErrorManager.configure(config)
    
    async def start(self):
        await NotificationTemplates.bot_started("Мой Бот")
        try:
            await self.run_bot()
        except Exception as e:
            await ErrorManager.notify_critical(
                ErrorCategory.SYSTEM,
                "Критическая ошибка в работе бота",
                exc=e
            )
        finally:
            await NotificationTemplates.bot_stopped("Мой Бот")
            await ErrorManager.close()
```

---

## 🐛 Поиск и устранение неисправностей

```python
# Проверка конфигурации
try:
    config.validate()
    print("✅ Конфигурация корректна")
except ValueError as e:
    print(f"❌ Ошибка конфигурации: {e}")

# Проверка инициализации
if ErrorManager.is_initialized():
    print("✅ ErrorManager готов к работе")
else:
    print("❌ ErrorManager не инициализирован")

# Тестовое уведомление
await ErrorManager.notify_info(
    ErrorCategory.SYSTEM,
    "Тестовое уведомление",
    {"status": "test"}
)
```

---

## 📄 Лицензия

Проект распространяется под лицензией **MIT**.  
Подробнее см. в файле `LICENSE`.

---

## 🤝 Вклад в проект

Мы приветствуем вклад!  
Присылайте **Pull Requests** или создавайте **Issues** для обсуждения новых функций и исправлений.

---

## 📞 Поддержка

- **Email:** Ia12Kotik@yandex.ru  
- **GitHub Issues:** https://github.com/Dusha01/tg_error_notifier  

---

**TG Error Notifier** — надежный помощник для мониторинга ваших Python-приложений! 🚀
