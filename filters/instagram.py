from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.instagram.instagram import InstagramUser


class InstagramPostFilter(BoundFilter):
    key = 'instagram_post'

    def __init__(self, instagram_post):
        self.instagram_post = instagram_post

    async def check(self, message: types.Message):
        return True if 'instagram.com/p/' in message.text.lower() or 'instagram.com/tv/' in message.text.lower() or 'instagram.com/reel/' in message.text.lower() else False


class InstagramHighlightFilter(BoundFilter):
    key = 'instagram_highlight'

    def __init__(self, instagram_highlight):
        self.instagram_highlight = instagram_highlight

    async def check(self, message: types.Message):
        return True if 'instagram.com/s/' in message.text.lower() or 'instagram.com/stories/highlights/' in message.text.lower() else False


class InstagramStoryFilter(BoundFilter):
    key = 'instagram_story'

    def __init__(self, instagram_story):
        self.instagram_story = instagram_story

    async def check(self, message: types.Message):
        return True if 'instagram.com/stories/' in message.text.lower() else False


class InstagramUserFilter(BoundFilter):
    key = 'instagram_user'

    def __init__(self, instagram_user):
        self.instagram_user = instagram_user

    async def check(self, message: types.Message):
        return True if 'instagram.com/' in message.text.lower() or await InstagramUser(message.text).start() else False
