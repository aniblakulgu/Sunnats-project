import time
from pyrogram import Client, filters
from pyrogram.types import Message

class ThrottlingMiddleware:
    def __init__(self, slow_mode_delay=0.5):
        self.user_timeouts = {}
        self.media_group_timeouts = {}
        self.slow_mode_delay = slow_mode_delay

    async def check_throttle(self, message: Message):
        user_id = message.from_user.id
        current_time = time.time()

        if message.media_group_id:
            # Media group uchun throttling
            last_request_time = self.media_group_timeouts.get(message.media_group_id, 0)
            if current_time - last_request_time < self.slow_mode_delay:
                return False  # Throttle qilingan
            self.media_group_timeouts[message.media_group_id] = current_time
        else:
            # Oddiy xabar uchun throttling
            last_request_time = self.user_timeouts.get(user_id, 0)
            if current_time - last_request_time < self.slow_mode_delay:
                return False  # Throttle qilingan
            self.user_timeouts[user_id] = current_time

        return True  # Ruxsat berilgan