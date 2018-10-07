from django.utils.functional import cached_property

from .util import batch_load_primary_key, DataLoader


class StoryLoaders:

    @cached_property
    def story(self):
        story_load_fn = batch_load_primary_key('story', 'Story')
        return DataLoader(story_load_fn)
