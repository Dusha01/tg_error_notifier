import logging
import traceback
from datetime import datetime
from typing import Optional, Dict, Any

from aiogram import Bot

from ..models.error_models import ErrorLevel, ErrorCategory
from ..models.notification_models import ErrorNotification
from .config import TelegramNotifierConfig

logger = logging.getLogger(__name__)


class ErrorNotifier:
    """
    Основной класс для отправки уведомлений об ошибках
    """
    
    def __init__(self, config: TelegramNotifierConfig):
        self.config = config
        self.bot = None
        self._setup_logging()
        self._initialize_bot()

    def _setup_logging(self):
        """Настройка логирования"""
        if self.config.enable_logging:
            logging.basicConfig(
                level=getattr(logging, self.config.log_level.upper()),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )

    def _initialize_bot(self):
        """Инициализация Telegram бота"""
        try:
            if (self.config.admin_bot_token and 
                self.config.notification_chat_id and 
                not self.config.disable_notifications):
                self.bot = Bot(token=self.config.admin_bot_token)
                logger.info("✅ Telegram бот для уведомлений инициализирован")
            else:
                logger.warning("❌ Токен бота или chat_id не настроены, уведомления отключены")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации бота для уведомлений: {e}")

    async def send_notification(self, notification: ErrorNotification):
        """
        Отправка уведомления
        """
        try:
            # Логируем уведомление
            self._log_notification(notification)
            
            # Отправляем в Telegram если бот инициализирован
            if (self.bot and 
                self.config.notification_chat_id and 
                not self.config.disable_notifications):
                message = self._format_message(notification)
                await self._send_telegram_message(message)
                
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления: {e}")

    async def _send_telegram_message(self, message: str):
        """Отправка сообщения в Telegram"""
        try:
            if len(message) > self.config.max_message_length:
                message = message[:self.config.max_message_length-100] + "\n\n... (сообщение обрезано)"
            
            await self.bot.send_message(
                chat_id=self.config.notification_chat_id,
                text=message,
                parse_mode=self.config.parse_mode
            )
        except Exception as e:
            logger.error(f"Ошибка отправки Telegram сообщения: {e}")

    def _format_message(self, notification: ErrorNotification) -> str:
        """Форматирование сообщения для Telegram"""
        level_emoji = {
            ErrorLevel.INFO: "ℹ️",
            ErrorLevel.WARNING: "⚠️",
            ErrorLevel.ERROR: "❌",
            ErrorLevel.CRITICAL: "🚨"
        }.get(notification.level, "📝")

        message_lines = [
            f"{level_emoji} *{self.config.app_name} - {notification.level.value.upper()}*",
            f"*Модуль:* {notification.category.value}",
            f"*Сообщение:* {notification.message}",
        ]

        if notification.details:
            details_str = "\n".join([f"  - {k}: {v}" for k, v in notification.details.items()])
            message_lines.append(f"*Детали:*\n{details_str}")

        if notification.timestamp:
            message_lines.append(f"*Время:* {notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

        if notification.traceback and notification.level in [ErrorLevel.ERROR, ErrorLevel.CRITICAL]:
            tb_preview = "\n".join(notification.traceback.split('\n')[-5:])
            message_lines.append(f"*Трассировка:*\n```\n{tb_preview}\n```")

        return "\n".join(message_lines)

    def _log_notification(self, notification: ErrorNotification):
        """Логирование уведомления"""
        log_message = f"[{notification.category.value}] {notification.message}"
        
        if notification.details:
            log_message += f" | Details: {notification.details}"
            
        if notification.level == ErrorLevel.INFO:
            logger.info(log_message)
        elif notification.level == ErrorLevel.WARNING:
            logger.warning(log_message)
        elif notification.level == ErrorLevel.ERROR:
            logger.error(log_message)
        elif notification.level == ErrorLevel.CRITICAL:
            logger.critical(log_message)

    async def info(self, category: ErrorCategory, message: str, details: Optional[Dict[str, Any]] = None):
        """Информационное уведомление"""
        await self.send_notification(ErrorNotification(
            level=ErrorLevel.INFO,
            category=category,
            message=message,
            details=details,
            timestamp=datetime.now()
        ))

    async def warning(self, category: ErrorCategory, message: str, details: Optional[Dict[str, Any]] = None):
        """Предупреждение"""
        await self.send_notification(ErrorNotification(
            level=ErrorLevel.WARNING,
            category=category,
            message=message,
            details=details,
            timestamp=datetime.now()
        ))

    async def error(self, category: ErrorCategory, message: str, 
                   details: Optional[Dict[str, Any]] = None, 
                   exc: Optional[Exception] = None):
        """Ошибка"""
        traceback_str = traceback.format_exc() if exc else None
        
        await self.send_notification(ErrorNotification(
            level=ErrorLevel.ERROR,
            category=category,
            message=message,
            details=details,
            timestamp=datetime.now(),
            traceback=traceback_str
        ))

    async def critical(self, category: ErrorCategory, message: str, 
                      details: Optional[Dict[str, Any]] = None,
                      exc: Optional[Exception] = None):
        """Критическая ошибка"""
        traceback_str = traceback.format_exc() if exc else None
        
        await self.send_notification(ErrorNotification(
            level=ErrorLevel.CRITICAL,
            category=category,
            message=message,
            details=details,
            timestamp=datetime.now(),
            traceback=traceback_str
        ))

    async def close(self):
        """Закрытие соединений"""
        if self.bot:
            await self.bot.session.close()
            logger.info("✅ Соединение с ботом для уведомлений закрыто")