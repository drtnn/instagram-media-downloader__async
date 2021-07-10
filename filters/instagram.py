from aiogram.types import Message, InlineQuery
from aiogram.dispatcher.filters import BoundFilter
from utils.instagram.instagram import InstagramUser


class InstagramPostFilter(BoundFilter):
    key = 'instagram_post'

    def __init__(self, instagram_post):
        self.instagram_post = instagram_post

    async def check(self, message: Message):
        return True if 'instagram.com/p/' in message.text.lower() or 'instagram.com/tv/' in message.text.lower() or 'instagram.com/reel/' in message.text.lower() else False


class InstagramHighlightFilter(BoundFilter):
    key = 'instagram_highlight'

    def __init__(self, instagram_highlight):
        self.instagram_highlight = instagram_highlight

    async def check(self, message: Message):
        return True if 'instagram.com/s/' in message.text.lower() or 'instagram.com/stories/highlights/' in message.text.lower() else False


class InstagramStoryFilter(BoundFilter):
    key = 'instagram_story'

    def __init__(self, instagram_story):
        self.instagram_story = instagram_story

    async def check(self, message: Message):
        return True if 'instagram.com/stories/' in message.text.lower() else False


class InstagramUserFilter(BoundFilter):
    key = 'instagram_user'

    def __init__(self, instagram_user):
        self.instagram_user = instagram_user

    async def check(self, message: Message):
        return True if 'instagram.com/' in message.text.lower() or await InstagramUser(message.text).start() else False


class InstagramPostInlineFilter(BoundFilter):
    key = 'instagram_inline_post'

    def __init__(self, instagram_inline_post):
        self.instagram_inline_post = instagram_inline_post

    async def check(self, query: InlineQuery):
        return True if 'instagram.com/p/' in query.query.lower() or 'instagram.com/tv/' in query.query.lower() or 'instagram.com/reel/' in query.query.lower() else False


class InstagramHighlightInlineFilter(BoundFilter):
    key = 'instagram_inline_highlight'

    def __init__(self, instagram_inline_highlight):
        self.instagram_inline_highlight = instagram_inline_highlight

    async def check(self, query: InlineQuery):
        return True if 'instagram.com/s/' in query.query.lower() or 'instagram.com/stories/highlights/' in query.query.lower() else False


class InstagramStoryInlineFilter(BoundFilter):
    key = 'instagram_inline_story'

    def __init__(self, instagram_inline_story):
        self.instagram_inline_story = instagram_inline_story

    async def check(self, query: InlineQuery):
        return True if 'instagram.com/stories/' in query.query.lower() else False


class InstagramUserInlineFilter(BoundFilter):
    key = 'instagram_inline_user'

    def __init__(self, instagram_inline_user):
        self.instagram_inline_user = instagram_inline_user

    async def check(self, query: InlineQuery):
        return True if 'instagram.com/' in query.query.lower() or await InstagramUser(query.query).start() else False
