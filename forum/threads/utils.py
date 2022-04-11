from functools import partial
from threads.models import *


def get_model_by_id(model: models.Model, _id: int) -> models.Model | None:
    try:
        return model.objects.get(id=_id)
    except Exception as e:
        print(e)
        return None


get_thread = partial(get_model_by_id, Thread)
get_comment = partial(get_model_by_id, Comment)
