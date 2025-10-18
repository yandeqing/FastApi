import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
import os

from Config import Config


class FcmService:
    """FCM推送服务类，用于发送Firebase Cloud Messaging推送通知"""

    def __init__(self, cred_path=None):
        """
        初始化FCM服务

        Args:
            cred_path: Firebase服务账号密钥JSON文件的路径
                      如果不提供，将尝试从环境变量FCM_CREDENTIALS_PATH获取
        """
        # 检查Firebase应用是否已经初始化
        if not firebase_admin._apps:
            # 获取凭证路径
            if cred_path is None:
                cred_path = os.environ.get('FCM_CREDENTIALS_PATH')

            if not cred_path:
                raise ValueError("请提供Firebase服务账号密钥文件路径，或设置FCM_CREDENTIALS_PATH环境变量")

            # 初始化Firebase应用
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

    def send_single_notification(self, token, title, body, data=None):
        """
        向单个设备发送通知

        Args:
            token: 设备令牌
            title: 通知标题
            body: 通知内容
            data: 可选的额外数据字典

        Returns:
            消息ID
        """
        # 构建通知消息，支持透传数据
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
            data=data,
        )

        # 默认的Android配置
        message.android = messaging.AndroidConfig(
            priority='high',
            direct_boot_ok=True,
            notification=messaging.AndroidNotification(
                sound='notification.mp3',
                default_sound=False,
                channel_id='default_channel_id',
                default_vibrate_timings=True,
                vibrate_timings_millis=[1000, 500, 1000],
            ),
        )
        # 发送消息
        response = messaging.send(message)
        return response

    def send_data_message(self, token, data):
        """
        发送仅包含数据的消息

        Args:
            token: 设备令牌
            data: 数据字典

        Returns:
            消息ID
        """
        # 构建数据消息
        message = messaging.Message(
            data=data,
            token=token,
        )

        # 发送消息
        response = messaging.send(message)
        return response

    def subscribe_to_topic(self, tokens, topic):
        """
        订阅设备到指定主题

        Args:
            tokens: 设备令牌列表
            topic: 主题名称

        Returns:
            订阅响应
        """
        response = messaging.subscribe_to_topic(tokens, topic)
        return {
            "success_count": response.success_count,
            "failure_count": len(tokens) - response.success_count
        }

    def unsubscribe_from_topic(self, tokens, topic):
        """
        取消订阅设备从指定主题

        Args:
            tokens: 设备令牌列表
            topic: 主题名称

        Returns:
            取消订阅响应
        """
        response = messaging.unsubscribe_from_topic(tokens, topic)
        return {
            "success_count": response.success_count,
            "failure_count": len(tokens) - response.success_count
        }

    def send_topic_notification(self, topic, title, body, data=None):
        """
        向主题发送通知

        Args:
            topic: 主题名称
            title: 通知标题
            body: 通知内容
            data: 可选的额外数据字典

        Returns:
            消息ID
        """
        # 构建主题消息
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            topic=topic,
            data=data,
        )

        # 发送消息
        response = messaging.send(message)
        return response

    def sendTest(self):
        """
        测试发送通知
        """
        # 时间戳
        timestamp = int(time.time())
        # 初始化服务
        fcm_service = FcmService('./uchat-9d016-firebase-adminsdk-fbsvc-7493c4b2eb.json')
        response = fcm_service.send_single_notification(
            Config.device_token,
            f'通知标题{timestamp}',
            f'通知内容{timestamp}',
            {'custom_key12': 'custom_value'}  # 可选的自定义数据
        )

        print(f"发送成功，消息ID: {response}")
