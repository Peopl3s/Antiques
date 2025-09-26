from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.artifact import ArtifactEntity
from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material
from tests.test_infrastructure.test_db.models.test_artifact_model import (
    TestArtifactModel,
)
from tests.test_infrastructure.test_db.repositories.test_artifact_repository_impl import (
    TestArtifactRepositorySQLAlchemy,
)


class TestArtifactRepository:
    @pytest.mark.asyncio
    async def test_save_artifact_success(self, test_session: AsyncSession):
        """Test successful artifact saving"""
        # Arrange
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        artifact_entity = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
            description="A beautiful ancient vase",
        )

        await repository.save(artifact_entity)

        result = await test_session.execute(
            text(
                f"SELECT * FROM artifacts WHERE inventory_id = '{artifact_entity.inventory_id}'"
            )
        )
        db_artifact = result.fetchone()

        assert db_artifact is not None
        assert db_artifact.inventory_id == str(artifact_entity.inventory_id)
        assert db_artifact.name == artifact_entity.name
        assert db_artifact.department == artifact_entity.department
        assert db_artifact.era == artifact_entity.era.value
        assert db_artifact.material == artifact_entity.material.value
        assert db_artifact.description == artifact_entity.description

    @pytest.mark.asyncio
    async def test_get_by_inventory_id_found(self, test_session: AsyncSession):
        """Test successful artifact retrieval by inventory ID"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        inventory_id = uuid4()

        artifact_model = TestArtifactModel(
            inventory_id=inventory_id,
            created_at=datetime.now(UTC),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name="Ancient Vase",
            department="Archaeology",
            era="antiquity",
            material="ceramic",
            description="A beautiful ancient vase",
        )
        test_session.add(artifact_model)
        await test_session.commit()

        result = await repository.get_by_inventory_id(str(inventory_id))

        assert result is not None
        assert result.inventory_id == inventory_id
        assert result.name == "Ancient Vase"
        assert result.department == "Archaeology"
        assert result.era.value == "antiquity"
        assert result.material.value == "ceramic"
        assert result.description == "A beautiful ancient vase"

    @pytest.mark.asyncio
    async def test_get_by_inventory_id_not_found(self, test_session: AsyncSession):
        """Test artifact retrieval when not found"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        non_existent_id = str(uuid4())

        result = await repository.get_by_inventory_id(non_existent_id)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_inventory_id_with_uuid_object(
        self, test_session: AsyncSession
    ):
        """Test artifact retrieval with UUID object"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        inventory_id = uuid4()

        artifact_model = TestArtifactModel(
            inventory_id=inventory_id,
            created_at=datetime.now(UTC),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name="Ancient Vase",
            department="Archaeology",
            era="antiquity",
            material="ceramic",
            description="A beautiful ancient vase",
        )
        test_session.add(artifact_model)
        await test_session.commit()

        result = await repository.get_by_inventory_id(inventory_id)

        assert result is not None
        assert result.inventory_id == inventory_id

    @pytest.mark.asyncio
    async def test_save_artifact_with_null_description(
        self, test_session: AsyncSession
    ):
        """Test saving artifact with null description"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        artifact_entity = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
            description=None,
        )

        await repository.save(artifact_entity)

        result = await test_session.execute(
            text(
                f"SELECT * FROM artifacts WHERE inventory_id = '{str(artifact_entity.inventory_id)}'"
            )
        )
        db_artifact = result.fetchone()

        assert db_artifact is not None
        assert db_artifact.description is None

    @pytest.mark.asyncio
    async def test_save_multiple_artifacts(self, test_session: AsyncSession):
        """Test saving multiple artifacts"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        artifacts = [
            ArtifactEntity(
                inventory_id=uuid4(),
                acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
                name=f"Artifact {i}",
                department="Archaeology",
                era=Era(value="antiquity"),
                material=Material(value="ceramic"),
                description=f"Description {i}",
            )
            for i in range(3)
        ]

        for artifact in artifacts:
            await repository.save(artifact)

        for artifact in artifacts:
            result = await test_session.execute(
                text(
                    f"SELECT * FROM artifacts WHERE inventory_id = '{str(artifact.inventory_id)}'"
                )
            )
            db_artifact = result.fetchone()
            assert db_artifact is not None
            assert db_artifact.name == artifact.name

    @pytest.mark.asyncio
    async def test_repository_session_handling(self, test_session: AsyncSession):
        """Test that repository properly handles database sessions"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        artifact_entity = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name="Test Artifact",
            department="Test Department",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        await repository.save(artifact_entity)

        assert not test_session.in_transaction()

        result = await repository.get_by_inventory_id(str(artifact_entity.inventory_id))
        assert result is not None

    @pytest.mark.asyncio
    async def test_artifact_entity_mapping(self, test_session: AsyncSession):
        """Test that database model is correctly mapped to entity"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        inventory_id = uuid4()
        created_at = datetime.now(UTC)
        acquisition_date = datetime(2023, 1, 1, tzinfo=UTC)

        artifact_model = TestArtifactModel(
            inventory_id=inventory_id,
            created_at=created_at,
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era="antiquity",
            material="ceramic",
            description="A beautiful ancient vase",
        )
        test_session.add(artifact_model)
        await test_session.commit()

        result = await repository.get_by_inventory_id(str(inventory_id))

        assert result is not None
        assert isinstance(result, ArtifactEntity)
        assert result.inventory_id == inventory_id
        assert result.created_at == created_at
        assert result.acquisition_date == acquisition_date
        assert result.name == "Ancient Vase"
        assert result.department == "Archaeology"
        assert result.era.value == "antiquity"
        assert result.material.value == "ceramic"
        assert result.description == "A beautiful ancient vase"

    @pytest.mark.asyncio
    async def test_repository_with_invalid_era_value(self, test_session: AsyncSession):
        """Test repository behavior with invalid era value in database"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        inventory_id = uuid4()

        artifact_model = TestArtifactModel(
            inventory_id=inventory_id,
            created_at=datetime.now(UTC),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name="Ancient Vase",
            department="Archaeology",
            era="invalid_era",  # This should cause issues
            material="ceramic",
        )
        test_session.add(artifact_model)
        await test_session.commit()

        with pytest.raises(Exception):
            await repository.get_by_inventory_id(str(inventory_id))

    @pytest.mark.asyncio
    async def test_repository_with_invalid_material_value(
        self, test_session: AsyncSession
    ):
        """Test repository behavior with invalid material value in database"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        inventory_id = uuid4()

        artifact_model = TestArtifactModel(
            inventory_id=inventory_id,
            created_at=datetime.now(UTC),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name="Ancient Vase",
            department="Archaeology",
            era="antiquity",
            material="invalid_material",  # This should cause issues
        )
        test_session.add(artifact_model)
        await test_session.commit()

        with pytest.raises(Exception):
            await repository.get_by_inventory_id(str(inventory_id))

    @pytest.mark.asyncio
    async def test_save_artifact_datetime_handling(self, test_session: AsyncSession):
        """Test that datetime fields are properly handled"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        acquisition_date = datetime(2023, 1, 1, 12, 30, 45, tzinfo=UTC)

        artifact_entity = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        await repository.save(artifact_entity)

        result = await test_session.execute(
            text(
                f"SELECT * FROM artifacts WHERE inventory_id = '{str(artifact_entity.inventory_id)}'"
            )
        )
        db_artifact = result.fetchone()

        assert db_artifact is not None

        if isinstance(db_artifact.acquisition_date, str):
            parsed_datetime = datetime.fromisoformat(
                db_artifact.acquisition_date.replace(" ", "T")
            )
            parsed_datetime = parsed_datetime.replace(tzinfo=UTC)
            assert parsed_datetime == acquisition_date
        else:
            assert db_artifact.acquisition_date == acquisition_date

    @pytest.mark.asyncio
    async def test_repository_error_handling(self, test_session: AsyncSession):
        """Test repository error handling"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)

        artifact_entity = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name=None,  # This should violate NOT NULL constraint
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        with pytest.raises(Exception):
            await repository.save(artifact_entity)

    @pytest.mark.asyncio
    async def test_get_by_inventory_id_empty_string(self, test_session: AsyncSession):
        """Test artifact retrieval with empty string ID"""
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)

        result = await repository.get_by_inventory_id("")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_inventory_id_malformed_uuid(self, test_session: AsyncSession):
        """Test artifact retrieval with malformed UUID"""

        repository = TestArtifactRepositorySQLAlchemy(session=test_session)

        result = await repository.get_by_inventory_id("not-a-uuid")
        assert result is None
