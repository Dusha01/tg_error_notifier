from typing import Optional

from ..models.error_models import ErrorCategory
from ..core.error_manager import ErrorManager


class NotificationTemplates:
    """
    Шаблоны стандартных уведомлений
    """
    
    @staticmethod
    async def bot_started(app_name: str = "Бот"):
        """Уведомление о запуске бота"""
        await ErrorManager.notify_info(
            ErrorCategory.SYSTEM,
            f"🤖 {app_name} успешно запущен"
        )
    
    @staticmethod
    async def bot_stopped(app_name: str = "Бот"):
        """Уведомление об остановке бота"""
        await ErrorManager.notify_info(
            ErrorCategory.SYSTEM,
            f"🤖 {app_name} остановлен"
        )
    
    @staticmethod
    async def database_connected():
        """Уведомление о подключении к БД"""
        await ErrorManager.notify_info(
            ErrorCategory.DATABASE,
            "✅ Подключение к базе данных восстановлено"
        )
    
    @staticmethod
    async def database_slow():
        """Уведомление о медленном соединении с БД"""
        await ErrorManager.notify_warning(
            ErrorCategory.DATABASE,
            "⚠️ Медленное соединение с базой данных"
        )
    
    @staticmethod
    async def database_connection_lost(exc: Optional[Exception] = None):
        """Уведомление о потере соединения с БД"""
        await ErrorManager.notify_error(
            ErrorCategory.DATABASE,
            "❌ Потеряно соединение с базой данных",
            exc=exc
        )
    
    @staticmethod
    async def cache_refreshed():
        """Уведомление об обновлении кэша"""
        await ErrorManager.notify_info(
            ErrorCategory.CACHE,
            "🔄 Кэш успешно обновлен"
        )
    
    @staticmethod
    async def cache_failure(exc: Optional[Exception] = None):
        """Уведомление об ошибке кэша"""
        await ErrorManager.notify_error(
            ErrorCategory.CACHE,
            "❌ Ошибка кэширования",
            exc=exc
        )
    
    @staticmethod
    async def service_unavailable(service_name: str, exc: Optional[Exception] = None):
        """Уведомление о недоступности сервиса"""
        await ErrorManager.notify_critical(
            ErrorCategory.EXTERNAL_SERVICE,
            f"🚨 Сервис {service_name} полностью недоступен",
            exc=exc
        )
    
    @staticmethod
    async def service_degraded(service_name: str, exc: Optional[Exception] = None):
        """Уведомление о деградации сервиса"""
        await ErrorManager.notify_warning(
            ErrorCategory.EXTERNAL_SERVICE,
            f"⚠️ Сервис {service_name} работает с перебоями",
            exc=exc
        )
    
    @staticmethod
    async def user_registered(user_id: str, username: str = ""):
        """Уведомление о регистрации пользователя"""
        details = {"user_id": user_id}
        if username:
            details["username"] = username
            
        await ErrorManager.notify_info(
            ErrorCategory.SYSTEM,
            "👤 Новый пользователь зарегистрирован",
            details
        )
    
    @staticmethod
    async def high_load_warning(service: str, load_percent: int):
        """Уведомление о высокой нагрузке"""
        await ErrorManager.notify_warning(
            ErrorCategory.SYSTEM,
            f"📈 Высокая нагрузка на {service}",
            {"load_percent": load_percent}
        )