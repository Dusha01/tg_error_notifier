from enum import Enum


class ErrorLevel(Enum):
    """
    Уровни важности ошибок
    """
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """
    Категории ошибок по модулям системы
    """
    DATABASE = "database"
    TELEGRAM = "telegram"
    API = "api"
    CACHE = "cache"
    AUTH = "authentication"
    SCHEDULE = "schedule"
    SYSTEM = "system"
    NETWORK = "network"
    VALIDATION = "validation"
    EXTERNAL_SERVICE = "external_service"