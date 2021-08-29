import os
from pathlib import Path

from pytest import fixture, mark

from beethoven.models import GridModel
from beethoven.repository import JsonRepository, MongoRepository

TEST_LOCAL_FILE = "tests/generated/local_grid.json"


@fixture(autouse=True)
def clean_local_file():
    yield

    if Path(TEST_LOCAL_FILE).exists():
        os.unlink(TEST_LOCAL_FILE)


@mark.parametrize("repository", [
    JsonRepository(path=TEST_LOCAL_FILE, table="grid", model=GridModel),
    MongoRepository(collection="grid", model=GridModel)
])
def test_grid_model_repositories(repository):
    repository.delete_all()

    obj = GridModel(name="grid", data="some grid")
    assert repository.add(obj)
    assert obj == repository.get("grid")

    old_obj = obj
    obj = GridModel(name="grid", data="some other grid")
    assert repository.add(obj)

    assert old_obj != repository.get("grid")
    assert obj == repository.get("grid")

    fake_obj = GridModel(name="non exist", data="no grid")
    assert not repository.update(fake_obj)

    obj2 = GridModel(name="grid2", data="another grid")
    assert repository.add(obj2)

    assert [obj, obj2] == repository.list()
    assert repository.delete("grid")

    repository.list()
    assert not repository.delete("grid")

    repository.delete_all()
    assert [] == repository.list()
