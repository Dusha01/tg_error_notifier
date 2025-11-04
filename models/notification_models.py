from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from .error_models import ErrorLevel, ErrorCategory


@dataclass
class ErrorNotification:
    """
    Модель уведомления об ошибке
    """
    level: ErrorLevel
    category: ErrorCategory
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
    traceback: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()