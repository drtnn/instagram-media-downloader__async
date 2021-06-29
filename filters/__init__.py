from loader import dp
from .instagram import InstagramUserFilter, InstagramHighlightFilter, InstagramStoryFilter, InstagramPostFilter
from .is_admin import AdminFilter


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(InstagramUserFilter)
    dp.filters_factory.bind(InstagramHighlightFilter)
    dp.filters_factory.bind(InstagramStoryFilter)
    dp.filters_factory.bind(InstagramPostFilter)
