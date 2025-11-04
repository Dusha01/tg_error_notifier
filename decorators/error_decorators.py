import functools
import asyncio
from typing import Callable, Any

from ..models.error_models import ErrorCategory
from ..core.error_manager import ErrorManager


def handle_errors(category: ErrorCategory, operation: str = ""):
    """
    Универсальный декоратор для обработки ошибок
    
    Args:
        category: Категория ошибки
        operation: Название операции (если не указано, используется имя функции)
    """
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                op_name = operation or func.__name__
                await ErrorManager.notify_error(
                    category,
                    f"Ошибка при выполнении: {op_name}",
                    {"function": func.__name__, "args": str(args)[:100], "kwargs": str(kwargs)[:100]},
                    e
                )
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                op_name = operation or func.__name__
                # Для синхронных функций используем асинхронную отправку
                asyncio.create_task(
                    ErrorManager.notify_error(
                        category,
                        f"Ошибка при выполнении: {op_name}",
                        {"function": func.__name__, "args": str(args)[:100], "kwargs": str(kwargs)[:100]},
                        e
                    )
                )
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator


def handle_database_errors(operation: str = ""):
    """Декоратор для обработки ошибок базы данных"""
    return handle_errors(ErrorCategory.DATABASE, operation)


def handle_telegram_errors(operation: str = ""):
    """Декоратор для обработки ошибок Telegram API"""
    return handle_errors(ErrorCategory.TELEGRAM, operation)


def handle_cache_errors(operation: str = ""):
    """Декоратор для обработки ошибок кэша"""
    return handle_errors(ErrorCategory.CACHE, operation)


def handle_system_errors(operation: str = ""):
    """Декоратор для обработки системных ошибок"""
    return handle_errors(ErrorCategory.SYSTEM, operation)


def handle_api_errors(operation: str = ""):
    """Декоратор для обработки ошибок API"""
    return handle_errors(ErrorCategory.API, operation)


def handle_auth_errors(operation: str = ""):
    """Декоратор для обработки ошибок аутентификации"""
    return handle_errors(ErrorCategory.AUTH, operation)