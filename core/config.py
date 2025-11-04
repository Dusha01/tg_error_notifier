from dataclasses import dataclass

@dataclass
class TelegramNotifierConfig:
    """
    Конфигурация для Telegram нотификатора
    """
    admin_bot_token: str
    notification_chat_id: str
    app_name: str = "MyApp"
    enable_logging: bool = True
    log_level: str = "INFO"
    parse_mode: str = "Markdown"
    disable_notifications: bool = False
    max_message_length: int = 4096
    
    def validate(self):
        """Проверка конфигурации"""
        if not self.admin_bot_token:
            raise ValueError("admin_bot_token is required")
        if not self.notification_chat_id:
            raise ValueError("notification_chat_id is required")