from collections import defaultdict

from django.apps import apps
from promise import Promise
from promise.dataloader import DataLoader as BaseDataLoader


def batch_load_primary_key(app_name, model_name):
    ModelToLoad = apps.get_model(app_name, model_name)
    def load(primary_keys):
        return ModelToLoad.objects.filter(id__in=primary_keys)

    def batch_load_fn(model_ids):
        model_records = load(model_ids)
        model_map = {}
        for model_record in model_records:
            model_map[model_record.id] = model_record
        return [model_map[model_id] for model_id in model_ids]
    return batch_load_fn


def batch_load_foreign_key(app_name, model_name, foreign_key_name):
    ModelToLoad = apps.get_model(app_name, model_name)
    def load(foreign_keys):
        condition = {f'{foreign_key_name}_id__in':foreign_keys}
        return ModelToLoad.objects.filter(**condition)

    def batch_load_fn(model_ids):
        model_records = load(model_ids)
        model_map = defaultdict(list)
        for model in model_records:
            foreign_key_id = getattr(model, f'{foreign_key_name}_id')
            model_map[foreign_key_id].append(model)
        return [model_map[model_id] for model_id in model_ids]
    return batch_load_fn


class DataLoader(BaseDataLoader):
    def __init__(self, *args, **kwargs):
        fn = kwargs.pop('batch_load_fn', None)
        if not fn:
            fn = args[0]
            args = (None,) + args[1:]
        self.fn = fn

        super().__init__(*args, **kwargs)

    def batch_load_fn(self, keys):
        return Promise.resolve(self.fn(keys))