from loader import dp
from .instagram import InstagramUserFilter, InstagramHighlightFilter, InstagramStoryFilter, InstagramPostFilter, InstagramUserInlineFilter, InstagramHighlightInlineFilter, InstagramStoryInlineFilter, InstagramPostInlineFilter
from .is_admin import AdminFilter


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(InstagramUserFilter)
    dp.filters_factory.bind(InstagramHighlightFilter)
    dp.filters_factory.bind(InstagramStoryFilter)
    dp.filters_factory.bind(InstagramPostFilter)
    dp.filters_factory.bind(InstagramUserInlineFilter)
    dp.filters_factory.bind(InstagramHighlightInlineFilter)
    dp.filters_factory.bind(InstagramStoryInlineFilter)
    dp.filters_factory.bind(InstagramPostInlineFilter)
