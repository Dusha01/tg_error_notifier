import logging
from typing import Optional, Dict, Any

from ..models.error_models import ErrorLevel, ErrorCategory
from .error_notification import ErrorNotifier
from .config import TelegramNotifierConfig

logger = logging.getLogger(__name__)


class ErrorManager:
    """
    Главный менеджер ошибок для приложения
    """
    
    _instance: Optional['ErrorManager'] = None
    _notifier: Optional[ErrorNotifier] = None
    _is_initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._is_initialized:
            raise RuntimeError("ErrorManager must be initialized with configure() first")

    @classmethod
    def configure(cls, config: TelegramNotifierConfig) -> 'ErrorManager':
        """
        Инициализация менеджера ошибок с конфигурацией
        """
        if cls._is_initialized:
            logger.warning("ErrorManager уже инициализирован")
            return cls._instance
            
        # Валидация конфигурации
        config.validate()
        
        # Инициализация нотификатора
        cls._notifier = ErrorNotifier(config)
        cls._is_initialized = True
        cls._instance = cls()
        
        logger.info("✅ ErrorManager инициализирован")
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'ErrorManager':
        """
        Получение экземпляра менеджера ошибок
        """
        if not cls._is_initialized:
            raise RuntimeError("ErrorManager не инициализирован. Сначала вызовите configure()")
        return cls._instance

    @classmethod
    async def notify_info(cls, category: ErrorCategory, message: str, details: Optional[Dict[str, Any]] = None):
        """Отправка информационного уведомления"""
        if cls._notifier:
            await cls._notifier.info(category, message, details)
        else:
            logger.info(f"[{category.value}] {message} - {details}")

    @classmethod
    async def notify_warning(cls, category: ErrorCategory, message: str, details: Optional[Dict[str, Any]] = None):
        """Отправка предупреждения"""
        if cls._notifier:
            await cls._notifier.warning(category, message, details)
        else:
            logger.warning(f"[{category.value}] {message} - {details}")

    @classmethod
    async def notify_error(cls, category: ErrorCategory, message: str, 
                          details: Optional[Dict[str, Any]] = None, 
                          exc: Optional[Exception] = None):
        """Отправка уведомления об ошибке"""
        if cls._notifier:
            await cls._notifier.error(category, message, details, exc)
        else:
            logger.error(f"[{category.value}] {message} - {details}", exc_info=exc)

    @classmethod
    async def notify_critical(cls, category: ErrorCategory, message: str, 
                             details: Optional[Dict[str, Any]] = None,
                             exc: Optional[Exception] = None):
        """Отправка уведомления о критической ошибке"""
        if cls._notifier:
            await cls._notifier.critical(category, message, details, exc)
        else:
            logger.critical(f"[{category.value}] {message} - {details}", exc_info=exc)

    @classmethod
    async def database_error(cls, operation: str, exc: Exception, details: Optional[Dict[str, Any]] = None):
        """Специализированный метод для ошибок базы данных"""
        await cls.notify_error(
            ErrorCategory.DATABASE,
            f"Ошибка базы данных при выполнении: {operation}",
            details,
            exc
        )

    @classmethod
    async def telegram_error(cls, operation: str, exc: Exception, details: Optional[Dict[str, Any]] = None):
        """Специализированный метод для ошибок Telegram API"""
        await cls.notify_error(
            ErrorCategory.TELEGRAM,
            f"Ошибка Telegram API при выполнении: {operation}",
            details,
            exc
        )

    @classmethod
    async def cache_error(cls, operation: str, exc: Exception, details: Optional[Dict[str, Any]] = None):
        """Специализированный метод для ошибок кэша"""
        await cls.notify_error(
            ErrorCategory.CACHE,
            f"Ошибка кэша при выполнении: {operation}",
            details,
            exc
        )

    @classmethod
    async def system_error(cls, operation: str, exc: Exception, details: Optional[Dict[str, Any]] = None):
        """Специализированный метод для системных ошибок"""
        await cls.notify_critical(
            ErrorCategory.SYSTEM,
            f"Системная ошибка при выполнении: {operation}",
            details,
            exc
        )

    @classmethod
    def is_initialized(cls) -> bool:
        """Проверка инициализации менеджера"""
        return cls._is_initialized

    @classmethod
    async def close(cls):
        """Закрытие соединений"""
        if cls._notifier:
            await cls._notifier.close()
            cls._is_initialized = False
            cls._notifier = None
            logger.info("✅ ErrorManager закрыт")