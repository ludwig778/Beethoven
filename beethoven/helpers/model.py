from copy import deepcopy


def update_model(object, **kwargs):
    object_data = deepcopy(object.dict())
    object_data.update(kwargs)

    return object.__class__(**object_data)
