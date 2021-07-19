from aiogram import Bot
import asyncio
import datetime
from .types import UploadClient, InstagramUser, smart_send_media
from utils.db_api.database import ParsedStory, Subscriber


class ScheduledParser:
    def __init__(self, bot: Bot, upload_client: UploadClient, seconds_to_repeat: int = 30 * 60):
        self.bot = bot
        self.seconds_to_repeat = seconds_to_repeat
        self.upload_client = upload_client

    async def start(self):
        while True:
            now = datetime.datetime.now()
            subscriptions = await Subscriber.get_actual_usernames(date=now - datetime.timedelta(30))
            if subscriptions:
                for subscription in subscriptions:
                    stories = await InstagramUser(subscription.username_to_parse).get_stories()
                    new_stories = []
                    for story in stories:
                        if not await ParsedStory.query.where(ParsedStory.story_id == story.story_id).gino.first():
                            new_stories.append(story)
                            await ParsedStory(story_id=story.story_id, parsed_date=now).create()
                    for subscriber in await Subscriber.get_user_ids(username=subscription.username_to_parse,
                                                                    date=now - datetime.timedelta(30)):
                        await smart_send_media(bot=self.bot, upload_client=self.upload_client, chat_id=subscriber.user_id, medias=new_stories, all_as_group=True)
            await ParsedStory.delete_before(date=now - datetime.timedelta(2))
            await asyncio.sleep(self.seconds_to_repeat)
