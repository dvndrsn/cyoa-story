from django.utils.functional import cached_property

from .util import batch_load_foreign_key, batch_load_primary_key, DataLoader


class ChoiceLoaders:

    @cached_property
    def choice(self):
        choice_load_fn = batch_load_primary_key('story', 'Choice')
        return DataLoader(choice_load_fn)

    @cached_property
    def choice_from_frompassage(self):
        choice_from_frompassage_load_fn = batch_load_foreign_key('story', 'Choice', 'from_passage')
        return DataLoader(choice_from_frompassage_load_fn)

    @cached_property
    def choice_from_topassage(self):
        choice_from_topassage_load_fn = batch_load_foreign_key('story', 'Choice', 'to_passage')
        return DataLoader(choice_from_topassage_load_fn)
