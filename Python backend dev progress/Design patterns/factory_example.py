from abc import ABC, abstractmethod


class Notification(ABC):
	@abstractmethod
	def send(self, message: str) -> None:
		"""Send a notification."""


class EmailNotification(Notification):
	def send(self, message: str) -> None:
		print(f"Email: {message}")


class SMSNotification(Notification):
	def send(self, message: str) -> None:
		print(f"SMS: {message}")


class NotificationFactory:
	@staticmethod
	def create(notification_type: str) -> Notification:
		if notification_type == "email":
			return EmailNotification()
		if notification_type == "sms":
			return SMSNotification()
		raise ValueError(f"Unsupported notification type: {notification_type}")


if __name__ == "__main__":
	notification = NotificationFactory.create("email")
	notification.send("Your order has shipped!")
