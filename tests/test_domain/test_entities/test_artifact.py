from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.domain.entities.artifact import ArtifactEntity
from src.domain.exceptions import InvalidEraException, InvalidMaterialException
from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material


class TestArtifactEntity:
    """Test cases for ArtifactEntity"""

    def test_create_artifact_entity_success(self):
        """Test successful creation of ArtifactEntity"""
        inventory_id = uuid4()
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        
        artifact = ArtifactEntity(
            inventory_id=inventory_id,
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
            description="A beautiful ancient vase",
        )

        assert artifact.inventory_id == inventory_id
        assert artifact.acquisition_date == acquisition_date
        assert artifact.name == "Ancient Vase"
        assert artifact.department == "Archaeology"
        assert artifact.era.value == "antiquity"
        assert artifact.material.value == "ceramic"
        assert artifact.description == "A beautiful ancient vase"
        assert isinstance(artifact.created_at, datetime)

    def test_create_artifact_entity_without_description(self):
        """Test creation of ArtifactEntity without description"""
        inventory_id = uuid4()
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        
        artifact = ArtifactEntity(
            inventory_id=inventory_id,
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        assert artifact.description is None

    def test_artifact_entity_immutability(self):
        """Test that ArtifactEntity is immutable"""
        inventory_id = uuid4()
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        
        artifact = ArtifactEntity(
            inventory_id=inventory_id,
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        with pytest.raises(AttributeError):
            artifact.name = "New Name"

    def test_artifact_entity_equality(self):
        """Test equality comparison between ArtifactEntity instances"""
        inventory_id = uuid4()
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        created_at = datetime(2023, 1, 2, tzinfo=timezone.utc)
        
        artifact1 = ArtifactEntity(
            inventory_id=inventory_id,
            created_at=created_at,
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        artifact2 = ArtifactEntity(
            inventory_id=inventory_id,
            created_at=created_at,
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        assert artifact1 == artifact2

    def test_artifact_entity_inequality(self):
        """Test inequality comparison between ArtifactEntity instances"""
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        
        artifact1 = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        artifact2 = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        assert artifact1 != artifact2

    def test_artifact_entity_hash(self):
        """Test that ArtifactEntity can be hashed"""
        inventory_id = uuid4()
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        
        artifact = ArtifactEntity(
            inventory_id=inventory_id,
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        assert hash(artifact) is not None

    def test_artifact_entity_string_representation(self):
        """Test string representation of ArtifactEntity"""
        inventory_id = uuid4()
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        
        artifact = ArtifactEntity(
            inventory_id=inventory_id,
            acquisition_date=acquisition_date,
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )

        str_repr = str(artifact)
        assert "ArtifactEntity" in str_repr
        assert "Ancient Vase" in str_repr

    def test_artifact_entity_with_all_eras(self):
        """Test ArtifactEntity creation with all valid era values"""
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        valid_eras = [
            "paleolithic", "neolithic", "bronze_age", "iron_age",
            "antiquity", "middle_ages", "modern"
        ]

        for era_value in valid_eras:
            artifact = ArtifactEntity(
                inventory_id=uuid4(),
                acquisition_date=acquisition_date,
                name="Test Artifact",
                department="Test Department",
                era=Era(value=era_value),
                material=Material(value="ceramic"),
            )
            assert artifact.era.value == era_value

    def test_artifact_entity_with_all_materials(self):
        """Test ArtifactEntity creation with all valid material values"""
        acquisition_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        valid_materials = [
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        ]

        for material_value in valid_materials:
            artifact = ArtifactEntity(
                inventory_id=uuid4(),
                acquisition_date=acquisition_date,
                name="Test Artifact",
                department="Test Department",
                era=Era(value="antiquity"),
                material=Material(value=material_value),
            )
            assert artifact.material.value == material_value

    def test_artifact_entity_created_at_default(self):
        """Test that created_at is set to current time by default"""
        before_creation = datetime.now(timezone.utc)
        
        artifact = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
        )
        
        after_creation = datetime.now(timezone.utc)
        
        assert before_creation <= artifact.created_at <= after_creation
