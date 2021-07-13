from aiogram import Bot
from aiogram.types import MediaGroup, ChatActions, CallbackQuery, InlineQuery, InlineQueryResultPhoto, \
    InlineQueryResultMpeg4Gif, InputTextMessageContent
from aiogram.utils.markdown import text
from bs4 import BeautifulSoup as BS
from data.config import BOT_NAME
from .headers import headers, headers_stories, headers_agent_list
from http3 import AsyncClient
from http3.exceptions import InvalidURL
from .instagram_query_result import inline_no_such_user, inline_no_actual_stories, inline_no_such_media, \
    inline_no_actual_posts
from io import BytesIO
import json
from keyboards.inline.instagram import user_keyboard, media_keyboard
import random
from utils.upload_client import UploadClient
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen

MAX_FILE_SIZE = 9.9


def get_post_link(data: dict):  # Получить ссылку на фото/видео из JSON
    return data['video_url'] if data['is_video'] else data['display_url']


def get_story_link(data: dict):  # Получить ссылку на фото/видео
    return data['video_versions'][0]['url'] if 'video_versions' in data else \
        data['image_versions2']['candidates'][0]['url']


async def get_big_video_id(upload_client: UploadClient, content: str, file_type: str):
    filename = await upload_client.get_file(url=content,
                                            filename=f'{hash(content)}.{file_type}')
    file_ids = await upload_client.send_files(BOT_NAME, [filename], delete_on_success=True)
    return file_ids[0]


async def smart_inline_media(medias: list):
    result = []
    for media in medias:
        if isinstance(media, (InstagramStory, InstagramPost, InstagramHighlight)):
            contents = media.media if isinstance(media.media, list) else [media.media]
            previews = media.preview if isinstance(media.preview, list) else [media.preview]
            sizes = media.size if isinstance(media.size, list) else [media.size]
            for index, (content, preview, size) in enumerate(zip(contents, previews, sizes)):
                meta = urlopen(content).info()
                media_type = meta['Content-Type'].split('/')[0]
                result_id = f'{hash(content)}-{index}'
                caption = f'<a href=\'https://www.instagram.com/{media.user.username}\'>{media.user.username}</a>: {media.caption}' if isinstance(
                    media, InstagramPost) else None
                if int(meta['Content-Length']) / 1024 / 1024 >= MAX_FILE_SIZE:
                    result.append(InlineQueryResultPhoto(id=result_id, photo_url=preview, thumb_url=preview,
                                                         title=f'📹 @{media.user.username}',
                                                         photo_width=size['width'],
                                                         photo_height=size['height'],
                                                         caption=caption if caption else f'📹 Видео весит больше лимита на выгрузку в inline-режиме, но доступно по ссылке ниже',
                                                         reply_markup=media_keyboard(content)
                                                         ))
                else:
                    if media_type == 'video':
                        result.append(InlineQueryResultMpeg4Gif(id=result_id, mpeg4_url=content,
                                                                thumb_url=preview, title=f'📹 @{media.user.username}',
                                                                mpeg4_width=size['width'],
                                                                mpeg4_height=size['height'],
                                                                mpeg4_duration=10,
                                                                caption=caption
                                                                ))
                    elif media_type == 'image':
                        result.append(InlineQueryResultPhoto(id=result_id, photo_url=content, thumb_url=preview,
                                                             title=f'📹 @{media.user.username}',
                                                             photo_width=size['width'],
                                                             photo_height=size['height'],
                                                             caption=caption
                                                             ))
    return result


async def smart_send_media(bot: Bot, upload_client: UploadClient, chat_id: int, medias: list,
                           all_as_group: bool = False):
    media_group = MediaGroup()
    client = AsyncClient()
    tmp_message = None
    for media in medias:
        if isinstance(media, (InstagramStory, InstagramPost, InstagramHighlight)):
            for content in media.media:
                meta = urlopen(content).info()
                media_type = meta['Content-Type'].split('/')[0]
                if int(meta["Content-Length"]) / 1024 / 1024 >= MAX_FILE_SIZE:
                    if not tmp_message:
                        tmp_message = await bot.send_message(chat_id=chat_id, text='📸 Начинается выгрузка контента...')
                    output = await get_big_video_id(upload_client=upload_client, content=content,
                                                    file_type=meta["Content-Type"].split("/")[1])
                else:
                    output = BytesIO((await client.get(content)).content)
                if media_type == 'video':
                    media_group.attach_video(output)
                elif media_type == 'image':
                    media_group.attach_photo(output)
                if len(media_group.media) == 10 or (not all_as_group and content is media.media[-1]) or (
                        all_as_group and media is medias[-1]):
                    await ChatActions.upload_video()
                    await bot.send_media_group(chat_id=chat_id, media=media_group)
                    if not all_as_group and isinstance(media, InstagramPost) and media.caption:
                        await bot.send_message(chat_id=chat_id,
                                               text=f'<a href=\'https://www.instagram.com/{media.user.username}\'>{media.user.username}</a>: {media.caption}')
                    media_group = MediaGroup()
    try:
        await tmp_message.delete()
    finally:
        pass


class InstagramUser:
    __is_started = False

    def __init__(self, username: str, biography: str = None, profile_pic_url: str = None, full_name: str = None,
                 posts_count: int = None, followers: int = None,
                 followings: int = None, user_id: int = None, is_private: bool = None, stories: list = None,
                 posts: list = None):
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
        self.posts = posts

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
        if self and self.user_id:
            return await bot.send_photo(chat_id=chat_id, photo=self.profile_pic_url, caption=self.to_message(),
                                        reply_markup=user_keyboard(self.username, self.is_private))
        elif not self or not self.user_id:
            await bot.send_message(chat_id=chat_id, text='🛑 <b>Профиль не найден или не существует</b>')

    async def send_stories_to(self, bot: Bot, upload_client: UploadClient, chat_id: int, call: CallbackQuery = None):
        if not self.__is_started:
            await self.start()
        if self and self.user_id:
            if self.stories is None:
                await self.get_stories()
            if isinstance(self.stories, list):
                if self.stories:
                    await smart_send_media(bot=bot, upload_client=upload_client, chat_id=chat_id, medias=self.stories,
                                           all_as_group=True)
                else:
                    if call:
                        await call.answer(text='🛑 Нет актуальных историй')
                    else:
                        await bot.send_message(chat_id=chat_id, text='🛑 <b>Нет актуальных историй</b>')
        elif not self or not self.user_id or (self and self.user_id and self.is_private):
            if call:
                await call.answer(text='🛑 Профиль не найден или не существует', show_alert=True)
            else:
                await bot.send_message(chat_id=chat_id, text='🛑 <b>Профиль не найден или не существует</b>')

    async def inline_stories_to(self, query: InlineQuery):
        if not self.__is_started:
            await self.start()
        if self and self.user_id and not self.is_private:
            if self.stories is None:
                await self.get_stories()
            if isinstance(self.stories, list):
                if self.stories:
                    result = await smart_inline_media(medias=self.stories)
                    await query.answer(results=result)
                else:
                    await query.answer(inline_no_actual_stories())
        elif not self or not self.user_id or (self and self.user_id and self.is_private):
            await query.answer(inline_no_such_user())

    async def inline_posts_to(self, query: InlineQuery, cache_time: int = None):
        if not self.__is_started:
            await self.start()
        if self and self.user_id and not self.is_private:
            if self.posts is None:
                await self.get_posts()
            if isinstance(self.posts, list):
                if self.posts:
                    result = await smart_inline_media(medias=self.posts)
                    await query.answer(results=result, cache_time=cache_time)
                else:
                    await query.answer(inline_no_actual_posts(), cache_time=cache_time)
        elif not self or not self.user_id or (self and self.user_id and self.is_private):
            await query.answer(inline_no_such_user(), cache_time=cache_time)

    async def get_stories(self):  # Получить ссылки на истории пользователя
        if not self.__is_started:
            await self.start()
        if not self or not self.user_id:
            return
        elif self and self.user_id and not self.is_private:
            client = AsyncClient()
            url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={self.user_id}'
            headers_stories['user-agent'] = headers_agent_list[random.randrange(0, 4)]
            result = await client.get(url=url, headers=headers_stories)
            try:
                data = json.loads(result.text)
            except ValueError:
                return
            self.stories = []
            if 'reels_media' in data and data['reels_media']:
                for story_responsive in data['reels_media'][0]['items']:
                    story = InstagramStory(user=self,
                                           media=[get_story_link(story_responsive)],
                                           preview=[story_responsive['image_versions2']['candidates'][0]['url']],
                                           size=[
                                               {'width': story_responsive['image_versions2']['candidates'][0]['width'],
                                                'height': story_responsive['image_versions2']['candidates'][0][
                                                    'height']}])
                    if 'story_cta' in story_responsive:
                        try:
                            story.swipe_link = story_responsive['story_cta'][0]['links'][0]['webUri']
                        except KeyError:
                            pass
                    self.stories.append(story)
            return self.stories

    async def get_posts(self):
        if not self.__is_started:
            await self.start()
        if not self or not self.user_id:
            return
        elif self and self.user_id and not self.is_private and self.posts_count:
            client = AsyncClient()
            url = f'https://instagram.com/{self.username}'
            headers['referer'] = url
            headers['user-agent'] = headers_agent_list[random.randrange(0, 4)]
            result = await client.get(url=url, headers=headers)
            soup = BS(result.text, 'lxml')
            shared_data = None
            for script in soup.select('script'):
                if len(script.contents) and 'window._sharedData = ' in script.contents[0]:
                    shared_data = script.contents[0]
                    break
            if shared_data:
                try:
                    data = json.loads(shared_data.replace('window._sharedData = ', '')[:-1])
                except ValueError:
                    return
                self.posts = []
                for post in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                    'edges']:
                    if 'edge_sidecar_to_children' in post['node']:
                        tmp_post = InstagramPost(user=self,
                                                 caption=post['node']['edge_media_to_caption']['edges'][0]['node'][
                                                     'text'] if post['node']['edge_media_to_caption'][
                                                     'edges'] else None, preview=[], media=[], size=[])
                        for media in post['node']['edge_sidecar_to_children']['edges']:
                            tmp_post.preview.append(media['node']['display_url'])
                            tmp_post.media.append(get_post_link(media['node']))
                            tmp_post.size.append(media['node']['dimensions'])
                        self.posts.append(tmp_post)
                    else:
                        self.posts.append(InstagramPost(user=self, caption=
                        post['node']['edge_media_to_caption']['edges'][0]['node']['text'] if
                        post['node']['edge_media_to_caption']['edges'] else None, preview=[post['node']['display_url']],
                                                        media=[get_post_link(post['node'])],
                                                        size=[post['node']['dimensions']]))
                return self.posts

    def __set_username_from_link(self):
        link = urlparse(self.username)[2].split('/')
        if len(link) >= 2:
            return link[1]

    def __str__(self):
        return f'@{self.username}. {self.full_name}: {self.biography}'


class InstagramPost:
    __is_started = False

    def __init__(self, link: str = None, user: InstagramUser = None, caption: str = None, preview: list = None,
                 media: list = None, size: list = None):
        self.link = link
        self.user = user
        self.caption = caption
        self.preview = preview
        self.media = media
        self.size = size

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
        self.size = []
        self.user = await InstagramUser(username).start()
        if 'edge_sidecar_to_children' in data['shortcode_media']:
            for media in data['shortcode_media']['edge_sidecar_to_children']['edges']:
                self.preview.append(media['node']['display_url'])
                self.media.append(get_post_link(media['node']))
                self.size.append(media['node']['dimensions'])
        else:
            self.preview.append(data['shortcode_media']['display_url'])
            self.media.append(get_post_link(data['shortcode_media']))
            self.size.append(data['shortcode_media']['dimensions'])
        if data['shortcode_media']['edge_media_to_caption']['edges'] and 'edge_media_to_caption' in data[
            'shortcode_media']:
            self.caption = data['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        return self

    async def send_to(self, bot: Bot, upload_client: UploadClient, chat_id: int, call: CallbackQuery = None):
        if not self.__is_started:
            await self.start()
        if self.user and self.user.user_id and self.media:
            await smart_send_media(bot, upload_client, chat_id, [self])
        elif not self.user or not self.user.user_id:
            if call:
                await call.answer(text='🛑 Неверная ссылка', show_alert=True)
            else:
                await bot.send_message(chat_id=chat_id, text='🛑 <b>Неверная ссылка</b>')

    async def inline_to(self, query: InlineQuery):
        if not self.__is_started:
            await self.start()
        if self.user and self.user.user_id and self.media:
            result = await smart_inline_media(medias=[self])
            await query.answer(result)
        elif not self or not self.user.user_id:
            inline_no_such_media(media_type='Пост')

    def __get_shortcode(self):  # Получить ID поста
        link = urlparse(self.link)[2].split('/')
        if 'p' in link:
            return link[link.index('p') + 1]
        elif 'tv' in link:
            return link[link.index('tv') + 1]
        elif 'reel' in link:
            return link[link.index('reel') + 1]
        else:
            return

    def __str__(self):
        return f'@{self.user.username if self.user else None}: {self.media}'


class InstagramStory:
    __is_started = False

    def __init__(self, link: str = None, user: InstagramUser = None, swipe_link: str = None, media: list = None,
                 preview: list = None, size: list = None):
        self.link = link
        self.user = user
        self.swipe_link = swipe_link
        self.media = media
        self.preview = preview
        self.size = size

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
                    self.size = [{'width': story['image_versions2']['candidates'][0]['width'],
                                  'height': story['image_versions2']['candidates'][0]['height']}]
                    return self

    async def send_to(self, bot: Bot, upload_client: UploadClient, chat_id: int, call: CallbackQuery = None):
        if not self.__is_started:
            await self.start()
        if self.user and self.user.user_id and self.media:
            await smart_send_media(bot, upload_client, chat_id, [self])
        elif not self.user or not self.user.user_id:
            if call:
                await call.answer(text='🛑 Неверная ссылка', show_alert=True)
            else:
                await bot.send_message(chat_id=chat_id, text='🛑 <b>Неверная ссылка</b>')

    async def inline_to(self, query: InlineQuery):
        if not self.__is_started:
            await self.start()
        if self.user and self.user.user_id and self.media:
            result = await smart_inline_media(medias=[self])
            await query.answer(result)
        elif not self.user or not self.user.user_id:
            inline_no_such_media(media_type='История')

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

    def __init__(self, link: str = None, user: InstagramUser = None, highlight_id: str = None,
                 story_media_id: str = None,
                 media: list = None):
        self.link = link
        self.user = user
        self.highlight_id = highlight_id
        self.story_media_id = story_media_id
        self.media = media

    async def start(self):  # Получить ссылку на историю
        self.__is_started = True
        await self.__parse_highlight_id()
        self.story_media_id = urlparse(self.link).query.split('&')[0].replace('story_media_id=',
                                                                              '') if '?story_media_id=' in self.link else None
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
            story = InstagramStory(user=self.user, media=[get_story_link(story_responsive)],
                                   preview=story_responsive['image_versions2']['candidates'][0]['url'],
                                   size=[{'width': story_responsive['image_versions2']['candidates'][0]['width'],
                                          'height': story_responsive['image_versions2']['candidates'][0]['height']}])
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
        if self.user and self.user.user_id and self.media:
            await smart_send_media(bot, upload_client, chat_id, self.media)
        elif not self.user or not self.user.user_id:
            if call:
                await call.answer(text='🛑 Неверная ссылка', show_alert=True)
            else:
                await bot.send_message(chat_id=chat_id, text='🛑 <b>Неверная ссылка</b>')

    async def inline_to(self, query: InlineQuery):
        if not self.__is_started:
            await self.start()
        if self.user and self.user.user_id and self.media:
            result = await smart_inline_media(medias=self.media)
            await query.answer(result)
        elif not self.user or not self.user.user_id:
            inline_no_such_media(media_type='Хайлайт')

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
