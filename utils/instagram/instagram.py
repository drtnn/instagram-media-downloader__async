from aiogram import Bot
from aiogram.types import MediaGroup, ChatActions, CallbackQuery
from aiogram.utils.markdown import text
from data.config import BOT_NAME
from .headers import headers, headers_stories, headers_agent_list
from http3 import AsyncClient
from http3.exceptions import InvalidURL
from io import BytesIO
import json
from keyboards.inline.instagram import user_keyboard
import random
from utils.upload_client import UploadClient
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen


def get_post_link(data: dict):  # Получить ссылку на фото/видео из JSON
    return data['video_url'] if data['is_video'] else data['display_url']


def get_story_link(data: dict):  # Получить ссылку на фото/видео
    return data['video_versions'][0]['url'] if 'video_versions' in data else \
        data['image_versions2']['candidates'][0]['url']


async def smart_send_media(bot: Bot, upload_client: UploadClient, chat_id: int, medias: list):
    media_group = MediaGroup()
    client = AsyncClient()
    for media in medias:
        if isinstance(media, str):
            content = media
        elif isinstance(media, (InstagramStory, InstagramPost, InstagramHighlight)):
            content = media.media
        else:
            return
        meta = urlopen(content).info()
        if int(meta["Content-Length"]) / 1024 / 1024 >= 5:
            filename = await upload_client.get_file(url=content, filename=f'{hash(content)}.{meta["Content-Type"].split("/")[1]}')
            file_ids = await upload_client.send_files(BOT_NAME, [filename], delete_on_success=True)
            output = file_ids[0]
        else:
            output = BytesIO((await client.get(content)).content)
        if meta['Content-Type'].split('/')[0] == 'video':
            media_group.attach_video(output)
        elif meta['Content-Type'].split('/')[0] == 'image':
            media_group.attach_photo(output)
        if len(media_group.media) == 10 or media is medias[-1]:
            await ChatActions.upload_video()
            await bot.send_media_group(chat_id=chat_id, media=media_group)
            media_group = MediaGroup()


class InstagramUser:
    __is_started = False

    def __init__(self, username: str, biography: str = None, profile_pic_url: str = None, full_name: str = None,
                 posts_count: int = None, followers: int = None,
                 followings: int = None, user_id: int = None, is_private: bool = None, stories: list = None):
        self.username = username
        self.biography = biography
        self.profile_pic_url = profile_pic_url
        self.full_name = full_name
        self.posts_count = posts_count
        self.followers = followers
        self.followings = followings
        self.user_id = user_id
        self.is_private = is_private
        self.stories = stories

    async def start(self):
        self.__is_started = True
        if 'instagram.com' in self.username:
            self.username = self.__set_username_from_link()
        client = AsyncClient()
        result = await client.get(url=f'https://www.instagram.com/{self.username}/?__a=1', headers=headers)
        try:
            data = json.loads(result.text)
            user = data['graphql']['user']
        except (ValueError, KeyError, TypeError, IndexError):
            return
        self.biography = user['biography'] if user['biography'] else None
        self.profile_pic_url = user['profile_pic_url_hd'] if user['profile_pic_url_hd'] else None
        self.full_name = user['full_name'] if user['full_name'] else None
        self.posts_count = user['edge_owner_to_timeline_media']['count'] if user['edge_owner_to_timeline_media'][
            'count'] else None
        self.followers = user['edge_followed_by']['count'] if user['edge_followed_by']['count'] else None
        self.followings = user['edge_follow']['count'] if user['edge_follow']['count'] else None
        self.user_id = int(user['id']) if user['id'] else None
        self.is_private = user['is_private'] if user['is_private'] else False
        return self

    def to_message(self):
        return text(
            f'{"🔒" if self.is_private else "👤"} <a href="https://www.instagram.com/{self.username}/">{self.username}</a>',
            f'📷 Количество постов – <b>{self.posts_count}</b>' if self.posts_count else '',
            f'📥 Количество подписчиков – <b>{self.followers}</b>' if self.followers else '',
            f'📤 Количество подписок – <b>{self.followings}</b>\n' if self.followings else '\n',
            f'<b>{self.full_name}</b>' if self.full_name and self.biography else '',
            f'<i>{self.biography}</i>' if self.biography else '',
            sep='\n')

    async def send_to(self, bot: Bot, chat_id: int):
        if not self.__is_started:
            await self.start()
        if self.user_id:
            return await bot.send_photo(chat_id=chat_id, photo=self.profile_pic_url, caption=self.to_message(),
                                        reply_markup=user_keyboard(self.username))
        elif not self.user_id:
            return await bot.send_message(chat_id=chat_id, text='🛑 <b>Профиль не найден или не существует</b>')

    async def send_stories_to(self, bot: Bot, upload_client: UploadClient, chat_id: int, call: CallbackQuery = None):
        if not self.__is_started:
            await self.start()
        if self.user_id:
            if self.stories is None:
                await self.get_stories()
            if isinstance(self.stories, list):
                if self.stories:
                    await smart_send_media(bot, upload_client, chat_id, self.stories)
                else:
                    if call:
                        return await call.answer(text='🛑 Нет актуальных историй')
                    else:
                        return await bot.send_message(chat_id=chat_id, text='🛑 <b>Нет актуальных историй</b>')
        elif not self.user_id:
            if call:
                return await call.answer(text='🛑 Профиль не найден или не существует', show_alert=True)
            else:
                return await bot.send_message(chat_id=chat_id, text='🛑 <b>Профиль не найден или не существует</b>')

    async def get_stories(self):  # Получить ссылки на истории пользователя
        if not self.__is_started:
            await self.start()
        if not self.user_id:
            return
        client = AsyncClient()
        url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={self.user_id}'
        headers['user-agent'] = headers_agent_list[random.randrange(0, 4)]
        result = await client.get(url=url, headers=headers_stories)
        try:
            data = json.loads(result.text)
        except ValueError:
            return
        self.stories = []
        if 'reels_media' in data and data['reels_media']:
            for story_responsive in data['reels_media'][0]['items']:
                story = InstagramStory(user=self,
                                       media=get_story_link(story_responsive),
                                       preview=story_responsive['image_versions2']['candidates'][0][
                                           'url'])
                if 'story_cta' in story_responsive:
                    try:
                        story.swipe_link = story_responsive['story_cta'][0]['links'][0]['webUri']
                    except KeyError:
                        pass
                self.stories.append(story)
        return self.stories

    def __set_username_from_link(self):
        link = urlparse(self.username)[2].split('/')
        if len(link) >= 2:
            return link[1]

    def __str__(self):
        return f'@{self.username}. {self.full_name}: {self.biography}'


class InstagramPost:
    __is_started = False

    def __init__(self, link: str, user: InstagramUser = None, caption: str = None, preview: list = None,
                 media: list = None):
        self.link = link
        self.user = user
        self.caption = caption
        self.preview = preview
        self.media = media

    async def start(self):  # Получить ссылки фото и видео из поста
        self.__is_started = True
        shortcode_id = self.__get_shortcode()
        if not shortcode_id:
            return
        headers['referer'] = self.link
        headers['user-agent'] = headers_agent_list[random.randrange(0, 4)]
        url = 'https://www.instagram.com/graphql/query/?' + urlencode({'query_hash': '2c4c2e343a8f64c625ba02b2aa12c7f8',
                                                                       'variables': f'{{"shortcode":"{shortcode_id}","has_threaded_comments":true}}'})
        client = AsyncClient()
        result = await client.get(url, headers=headers)
        try:
            data = json.loads(result.text)['data']
            username = data['shortcode_media']['owner']['username']
        except (ValueError, KeyError, TypeError, IndexError):
            return
        self.media = []
        self.preview = []
        self.user = await InstagramUser(username).start()
        if 'edge_sidecar_to_children' in data['shortcode_media']:
            for media in data['shortcode_media']['edge_sidecar_to_children']['edges']:
                self.preview.append(media['node']['display_url'])
                self.media.append(get_post_link(media['node']))
        else:
            self.preview.append(data['shortcode_media']['display_url'])
            self.media.append(get_post_link(data['shortcode_media']))
        if data['shortcode_media']['edge_media_to_caption']['edges'] and 'edge_media_to_caption' in data['shortcode_media']:
            self.caption = data['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        return self

    async def send_to(self, bot: Bot, upload_client: UploadClient, chat_id: int, call: CallbackQuery = None):
        if not self.__is_started:
            await self.start()
        if self.user.user_id and self.media:
            await smart_send_media(bot, upload_client, chat_id, self.media)
        elif not self.user.user_id:
            if call:
                return await call.answer(text='🛑 Неверная ссылка', show_alert=True)
            else:
                return await bot.send_message(chat_id=chat_id, text='🛑 <b>Неверная ссылка</b>')

    def __get_shortcode(self):  # Получить ID поста
        link = urlparse(self.link)[2].split('/')
        if 'p' in link or 'tv' in link:
            return link[link.index('p') + 1] if 'p' in link else link[link.index('tv') + 1]

    def __str__(self):
        return f'@{self.user.username if self.user else None}: {self.media}'


class InstagramStory:
    __is_started = False

    def __init__(self, link: str = None, user: InstagramUser = None, swipe_link: str = None, media: list = None,
                 preview: str = None):
        self.link = link
        self.user = user
        self.swipe_link = swipe_link
        self.media = media
        self.preview = preview

    async def start(self):  # Получить ссылку на историю
        self.__is_started = True
        self.user = await InstagramUser(self.__get_username_from_link()).start()
        if not self.link or not self.user:
            return
        url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={self.user.user_id}'
        headers_stories['user-agent'] = headers_agent_list[random.randrange(0, 4)]
        client = AsyncClient()
        result = await client.get(url, headers=headers_stories)
        try:
            data = json.loads(result.text)['reels_media']
        except (ValueError, KeyError, TypeError, IndexError):
            return
        if data:
            for story in data[0]['items']:
                if story['pk'] == self.__get_shortcode():
                    if 'story_cta' in story:
                        try:
                            self.swipe_link = story['story_cta'][0]['links'][0]['webUri']
                        except KeyError:
                            pass
                    self.preview = [story['image_versions2']['candidates'][0]['url']]
                    self.media = [get_story_link(story)]
                    return self

    async def send_to(self, bot: Bot, upload_client: UploadClient, chat_id: int, call: CallbackQuery = None):
        if not self.__is_started:
            await self.start()
        if self.user.user_id and self.media:
            await smart_send_media(bot, upload_client, chat_id, self.media)
        elif not self.user.user_id:
            if call:
                return await call.answer(text='🛑 Неверная ссылка', show_alert=True)
            else:
                return await bot.send_message(chat_id=chat_id, text='🛑 <b>Неверная ссылка</b>')

    def __get_shortcode(self):  # Получить ID истории
        link = urlparse(self.link)[2].split('/')
        return link[link.index('stories') + 2] if 'stories' in link else None

    def __get_username_from_link(self):  # Получить имя пользователя
        link = urlparse(self.link)[2].split('/')
        return link[link.index('stories') + 1] if 'stories' in link else None

    def __str__(self):
        return f'@{self.user.username if self.user else None}: {self.media}'


class InstagramHighlight:
    __is_started = False

    def __init__(self, link: str, user: InstagramUser = None, highlight_id: str = None, story_media_id: str = None,
                 media: list = None):
        self.link = link
        self.user = user
        self.highlight_id = highlight_id
        self.story_media_id = story_media_id
        self.media = media

    async def start(self):  # Получить ссылку на историю
        self.__is_started = True
        await self.__parse_highlight_id()
        self.story_media_id = urlparse(self.link).query.split('&')[0].replace('story_media_id=', '') if '?story_media_id=' in self.link else None
        if not self.highlight_id:
            return
        url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids=highlight%3A{self.highlight_id}'
        headers_stories['user-agent'] = headers_agent_list[random.randrange(0, 4)]
        client = AsyncClient()
        result = await client.get(url, headers=headers_stories)
        try:
            data = json.loads(result.text)['reels_media']
            username = data[0]['user']['username']
        except (ValueError, KeyError, TypeError, IndexError):
            return
        self.user, self.media = await InstagramUser(username).start(), []
        for story_responsive in data[0]['items']:
            story = InstagramStory(user=self.user, media=get_story_link(story_responsive),
                                   preview=story_responsive['image_versions2']['candidates'][0]['url'])
            if 'story_cta' in story_responsive:
                try:
                    story.swipe_link = story_responsive['story_cta'][0]['links'][0]['webUri']
                except KeyError:
                    pass
            if self.story_media_id and story_responsive['pk'] == self.story_media_id:
                self.media = [story]
                return self
            elif not self.story_media_id:
                self.media.append(story)
        return self

    async def send_to(self, bot: Bot, upload_client: UploadClient, chat_id: int, call: CallbackQuery = None):
        if not self.__is_started:
            await self.start()
        if self.user.user_id and self.media:
            await smart_send_media(bot, upload_client, chat_id, self.media)
        elif not self.user.user_id:
            if call:
                return await call.answer(text='🛑 Неверная ссылка', show_alert=True)
            else:
                return await bot.send_message(chat_id=chat_id, text='🛑 <b>Неверная ссылка</b>')

    async def __parse_highlight_id(self):
        if self.link and 'instagram.com/stories/highlights/' in self.link:
            try:
                link = urlparse(self.link)[2].split('/')
                self.highlight_id = link[link.index('highlights') + 1] if 'highlights' in link else None
            except (ValueError, KeyError, TypeError, IndexError):
                return
        else:
            headers_stories['user-agent'] = headers_agent_list[random.randrange(0, 4)]
            client = AsyncClient()
            try:
                result = await client.get(url=self.link, headers=headers_stories)
                for data in result.history:
                    if data.is_redirect:
                        link = urlparse(data.headers.raw[1][1].decode('utf-8'))[2].split('/')
                        self.highlight_id = link[link.index('highlights') + 1] if 'highlights' in link else None
            except (ValueError, KeyError, TypeError, IndexError, InvalidURL):
                return

    def __str__(self):
        return f'@{self.user.username if self.user else None}: {self.media}'
