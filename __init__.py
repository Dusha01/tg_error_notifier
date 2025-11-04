"""
TG Error Notifier - Библиотека для уведомлений об ошибках через Telegram
"""

from .core.error_manager import ErrorManager
from .core.config import TelegramNotifierConfig
from .decorators.error_decorators import (
    handle_errors, 
    handle_database_errors,
    handle_telegram_errors,
    handle_cache_errors,
    handle_system_errors
)
from .templates.notification_templates import NotificationTemplates
from .models.error_models import ErrorLevel, ErrorCategory
from .models.notification_models import ErrorNotification

__version__ = "1.0.0"
__author__ = "Dusha"
__email__ = "Ia12Kotik@yandex.ru"

__all__ = [
    'ErrorManager',
    'TelegramNotifierConfig',
    'handle_errors',
    'handle_database_errors',
    'handle_telegram_errors', 
    'handle_cache_errors',
    'handle_system_errors',
    'NotificationTemplates',
    'ErrorLevel',
    'ErrorCategory',
    'ErrorNotification'
]