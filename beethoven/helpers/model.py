from copy import deepcopy

from beethoven.models import __all__ as Model


def update_model(object: Model, **kwargs) -> Model:
    object_data = deepcopy(object.dict())
    object_data.update(kwargs)

    return object.__class__(**object_data)
