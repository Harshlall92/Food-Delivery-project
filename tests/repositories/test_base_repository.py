import json
import pytest
from pydantic import BaseModel
from app.repositories.base_repository import BaseRepository
from app.repositories.exceptions import *

class Model(BaseModel):
    id: str
    name: str

def create_test_model(
    id: str = "1",
    name: str = "Test Model"
):
    return Model(id=id, name=name)

def data(*model: Model) -> list[dict]:
    return [item.model_dump() for item in model]

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

def read_file(test_file, * ,return_json: bool = False) -> list[dict] | str:
    return json.loads(test_file.read_text(encoding="utf-8")) if return_json else test_file.read_text(encoding="utf-8")

class TestFileInteraction:

    class TestReadFile:

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

            repository = BaseRepository[Model](file_path=str(test_file))

            content = await repository._read_file()

            assert content == test_data

        @pytest.mark.anyio
        async def test_repository_handles_file_not_found_on_read(self, tmp_path):
            test_file = tmp_path / "non_existent.json"

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

            assert not test_file.exists()

            content = await repository._read_file()

            assert content == []
            assert test_file.exists()
            assert read_file(test_file) == "[]"

        @pytest.mark.anyio
        async def test_repository_handles_invalid_json_on_read(self, tmp_path):
            test_file = tmp_path / "invalid.json"
            write_data_to_file(test_file, "invalid json")

            repository = BaseRepository[Model](file_path=str(test_file))

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

            assert content == []
            assert test_file.exists()
            assert read_file(test_file) == "[]"

    class TestWriteFile:

        @pytest.mark.anyio
        async def test_repository_can_write_to_file(self, tmp_path):
            test_file = tmp_path / "test_write.json"
            write_data_to_file(test_file, "")
            test_data = data(create_test_model())

            repository = BaseRepository[Model](file_path=str(test_file))

            assert test_file.exists() == True

            await repository._write_file(test_data)

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

            assert content == test_data

    assert items == [TestModel(**data[0])]

            repository = BaseRepository[Model](file_path=str(test_file))

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

            await repository._write_file(test_data)

            content = read_file(test_file, return_json=True)

            assert content == test_data

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

    class TestCreateOperations:

        @pytest.mark.anyio
        async def test_add_record(self, tmp_path):
            test_file = tmp_path / "test.json"

            repository = BaseRepository[Model](file_path=str(test_file))

            new_item = create_test_model()
            added_item = await repository.add_record(new_item)

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

            content = read_file(test_file, return_json=True)
            assert len(content) == 1

        @pytest.mark.anyio
        async def test_add_record_raises_duplicate_item_error_if_id_already_exists(self, tmp_path):
            test_file = tmp_path / "test.json"
            write_data_to_file(test_file, data(create_test_model()))

            repository = BaseRepository[Model](file_path=str(test_file))

            duplicate_item = create_test_model()

    repository = BaseRepository(file_path=str(file_path), model=TestModel)


    assert item == TestModel(**data[1])

        @pytest.mark.anyio
        async def test_get_all(self, tmp_path):
            test_file = tmp_path / "test.json"
            file_contents = data(create_test_model(), create_test_model(id="2"))
            write_data_to_file(test_file, file_contents)

    repository = BaseRepository(file_path=str(file_path), model=TestModel)

            items = await repository.get_all()

            assert items == file_contents

        @pytest.mark.anyio
        async def test_get_all_returns_empty_list_if_file_is_empty(self, tmp_path):
            test_file = tmp_path / "empty.json"

            write_data_to_file(test_file, "")

            repository = BaseRepository[Model](file_path=str(test_file))

            items = await repository.get_all()

            assert items == []

        @pytest.mark.anyio
        async def test_get_by_id(self, tmp_path):
            test_file = tmp_path / "test.json"
            write_data_to_file(test_file, data(create_test_model(), create_test_model(id="2", name="Another Test")))

            repository = BaseRepository[Model](file_path=str(test_file))

            item = await repository.get_by_id("2")

            assert item == {"id": "2", "name": "Another Test"}

        @pytest.mark.anyio
        async def test_get_by_id_raises_item_not_found_error_if_item_not_found(self, tmp_path):
            test_file = tmp_path / "test.json"
            write_data_to_file(test_file, data(create_test_model()))

            repository = BaseRepository[Model](file_path=str(test_file))

            with pytest.raises(RecordNotFoundError) as e:
                await repository.get_by_id("2")

            assert str(e.value) == "Model with id 2 not found."

    class TestUpdateOperations:

        @pytest.mark.anyio
        async def test_update_record(self, tmp_path):
            test_file = tmp_path / "test.json"
            write_data_to_file(test_file, data(create_test_model()))

            repository = BaseRepository[Model](file_path=str(test_file))

            updated_model = create_test_model(name="Updated Test")
            updated_record = await repository.update_record("1", updated_model)

            assert updated_record == {"id": "1", "name": "Updated Test"}

            content = read_file(test_file, return_json=True)
            assert content[0] == updated_record

        @pytest.mark.anyio
        async def test_update_record_raises_item_not_found_error_if_item_not_found(self, tmp_path):
            test_file = tmp_path / "test.json"
            write_data_to_file(test_file, data(create_test_model()))

            repository = BaseRepository[Model](file_path=str(test_file))

            updated_model = create_test_model(name="Updated Test")

            with pytest.raises(RecordNotFoundError) as e:
                await repository.update_record("2", updated_model)
            
            assert str(e.value) == "Model with id 2 not found."
    
    class TestDeleteOperations:

        @pytest.mark.anyio
        async def test_delete_record(self, tmp_path):
            test_file = tmp_path / "test.json"
            write_data_to_file(test_file, data(create_test_model(), create_test_model(id="2")))

            repository = BaseRepository[Model](file_path=str(test_file))

            result = await repository.delete_record("1")

            assert result

            content = read_file(test_file, return_json=True)
            assert len(content) == 1

        @pytest.mark.anyio
        async def test_delete_record_returns_false_if_item_not_found(self, tmp_path):
            test_file = tmp_path / "test.json"
            write_data_to_file(test_file, data(create_test_model()))

            repository = BaseRepository[Model](file_path=str(test_file))

            result = await repository.delete_record("2")

            assert result == False

            content = read_file(test_file, return_json=True)
            assert len(content) == 1