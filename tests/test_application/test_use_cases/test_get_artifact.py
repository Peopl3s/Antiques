from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
    EraDTO,
    MaterialDTO,
)
from src.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from src.application.use_cases.get_artifact import GetArtifactUseCase
from src.domain.entities.artifact import ArtifactEntity
from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material


class TestGetArtifactUseCase:
    """Test cases for GetArtifactUseCase"""

    @pytest.mark.asyncio
    async def test_execute_artifact_found_in_repository(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_entity: ArtifactEntity,
        sample_artifact_dto: ArtifactDTO,
    ):
        """Test successful execution when artifact is found in local repository"""
        # Arrange
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = sample_artifact_entity
        mock_mapper.to_dto.return_value = sample_artifact_dto

        # Act
        result = await get_artifact_use_case.execute(inventory_id)

        # Assert
        assert result == sample_artifact_dto
        mock_repository.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_mapper.to_dto.assert_called_once_with(sample_artifact_entity)
        mock_repository.save.assert_not_called()
        mock_museum_api = get_artifact_use_case.museum_api_client
        mock_museum_api.fetch_artifact.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_artifact_not_found_locally_fetched_from_api(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_museum_api: AsyncMock,
        mock_catalog_api: AsyncMock,
        mock_message_broker: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_dto: ArtifactDTO,
        sample_artifact_entity: ArtifactEntity,
        sample_notification_dto: ArtifactAdmissionNotificationDTO,
        sample_publication_dto: ArtifactCatalogPublicationDTO,
    ):
        """Test successful execution when artifact is fetched from external API"""
        # Arrange
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = None
        mock_museum_api.fetch_artifact.return_value = sample_artifact_dto
        mock_mapper.to_entity.return_value = sample_artifact_entity
        mock_catalog_api.publish_artifact.return_value = "public_id_123"

        # Act
        result = await get_artifact_use_case.execute(inventory_id)

        # Assert
        assert result == sample_artifact_dto
        
        # Verify repository calls
        mock_repository.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_repository.save.assert_called_once_with(sample_artifact_entity)
        
        # Verify API calls
        mock_museum_api.fetch_artifact.assert_called_once_with(inventory_id)
        mock_catalog_api.publish_artifact.assert_called_once()
        
        # Verify message broker call
        mock_message_broker.publish_new_artifact.assert_called_once()
        
        # Verify mapper calls
        mock_mapper.to_entity.assert_called_once_with(sample_artifact_dto)
        # Note: to_dto is not called when artifact is fetched from external API
        # because the use case returns the original artifact_dto from the API

    @pytest.mark.asyncio
    async def test_execute_artifact_not_found_in_external_api(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_museum_api: AsyncMock,
        sample_artifact_entity: ArtifactEntity,
    ):
        """Test execution when artifact is not found in external API"""
        # Arrange
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = None
        mock_museum_api.fetch_artifact.side_effect = ArtifactNotFoundError("Artifact not found")

        # Act & Assert
        with pytest.raises(ArtifactNotFoundError):
            await get_artifact_use_case.execute(inventory_id)

        # Verify calls
        mock_repository.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_museum_api.fetch_artifact.assert_called_once_with(inventory_id)
        mock_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_external_api_failure(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_museum_api: AsyncMock,
        sample_artifact_entity: ArtifactEntity,
    ):
        """Test execution when external API call fails"""
        # Arrange
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = None
        mock_museum_api.fetch_artifact.side_effect = Exception("API Error")

        # Act & Assert
        with pytest.raises(FailedFetchArtifactMuseumAPIException):
            await get_artifact_use_case.execute(inventory_id)

        # Verify calls
        mock_repository.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_museum_api.fetch_artifact.assert_called_once_with(inventory_id)
        mock_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_message_broker_failure(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_museum_api: AsyncMock,
        mock_message_broker: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_dto: ArtifactDTO,
        sample_artifact_entity: ArtifactEntity,
    ):
        """Test execution when message broker publish fails"""
        # Arrange
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = None
        mock_museum_api.fetch_artifact.return_value = sample_artifact_dto
        mock_mapper.to_entity.return_value = sample_artifact_entity
        mock_message_broker.publish_new_artifact.side_effect = Exception("Broker Error")

        # Act & Assert
        with pytest.raises(FailedPublishArtifactMessageBrokerException):
            await get_artifact_use_case.execute(inventory_id)

        # Verify calls
        mock_repository.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_museum_api.fetch_artifact.assert_called_once_with(inventory_id)
        mock_repository.save.assert_called_once_with(sample_artifact_entity)
        mock_message_broker.publish_new_artifact.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_catalog_api_failure(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_museum_api: AsyncMock,
        mock_catalog_api: AsyncMock,
        mock_message_broker: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_dto: ArtifactDTO,
        sample_artifact_entity: ArtifactEntity,
    ):
        """Test execution when catalog API publish fails"""
        # Arrange
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = None
        mock_museum_api.fetch_artifact.return_value = sample_artifact_dto
        mock_mapper.to_entity.return_value = sample_artifact_entity
        mock_catalog_api.publish_artifact.side_effect = Exception("Catalog Error")

        # Act & Assert
        with pytest.raises(FailedPublishArtifactInCatalogException):
            await get_artifact_use_case.execute(inventory_id)

        # Verify calls
        mock_repository.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_museum_api.fetch_artifact.assert_called_once_with(inventory_id)
        mock_repository.save.assert_called_once_with(sample_artifact_entity)
        mock_message_broker.publish_new_artifact.assert_called_once()
        mock_catalog_api.publish_artifact.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_with_uuid_input(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_entity: ArtifactEntity,
        sample_artifact_dto: ArtifactDTO,
    ):
        """Test execution with UUID input instead of string"""
        # Arrange
        inventory_id = sample_artifact_entity.inventory_id
        mock_repository.get_by_inventory_id.return_value = sample_artifact_entity
        mock_mapper.to_dto.return_value = sample_artifact_dto

        # Act
        result = await get_artifact_use_case.execute(inventory_id)

        # Assert
        assert result == sample_artifact_dto
        mock_repository.get_by_inventory_id.assert_called_once_with(str(inventory_id))

    @pytest.mark.asyncio
    async def test_validate_era_valid_values(
        self,
        get_artifact_use_case: GetArtifactUseCase,
    ):
        """Test era validation with valid values"""
        valid_eras = [
            "paleolithic", "neolithic", "bronze_age", "iron_age",
            "antiquity", "middle_ages", "modern"
        ]

        for era_value in valid_eras:
            result = get_artifact_use_case._validate_era(era_value)
            assert result == era_value

    @pytest.mark.asyncio
    async def test_validate_era_invalid_values(
        self,
        get_artifact_use_case: GetArtifactUseCase,
    ):
        """Test era validation with invalid values"""
        invalid_eras = ["invalid_era", "prehistoric", "future", ""]

        for era_value in invalid_eras:
            with pytest.raises(ValueError, match="Invalid era value"):
                get_artifact_use_case._validate_era(era_value)

    @pytest.mark.asyncio
    async def test_validate_material_valid_values(
        self,
        get_artifact_use_case: GetArtifactUseCase,
    ):
        """Test material validation with valid values"""
        valid_materials = [
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        ]

        for material_value in valid_materials:
            result = get_artifact_use_case._validate_material(material_value)
            assert result == material_value

    @pytest.mark.asyncio
    async def test_validate_material_invalid_values(
        self,
        get_artifact_use_case: GetArtifactUseCase,
    ):
        """Test material validation with invalid values"""
        invalid_materials = ["invalid_material", "plastic", "paper", ""]

        for material_value in invalid_materials:
            with pytest.raises(ValueError, match="Invalid material value"):
                get_artifact_use_case._validate_material(material_value)

    @pytest.mark.asyncio
    async def test_execute_notification_dto_creation(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_museum_api: AsyncMock,
        mock_message_broker: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_dto: ArtifactDTO,
        sample_artifact_entity: ArtifactEntity,
    ):
        """Test that notification DTO is created correctly"""
        # Arrange
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = None
        mock_museum_api.fetch_artifact.return_value = sample_artifact_dto
        mock_mapper.to_entity.return_value = sample_artifact_entity

        # Act
        await get_artifact_use_case.execute(inventory_id)

        # Assert
        mock_message_broker.publish_new_artifact.assert_called_once()
        call_args = mock_message_broker.publish_new_artifact.call_args[0][0]
        
        assert isinstance(call_args, ArtifactAdmissionNotificationDTO)
        assert call_args.inventory_id == sample_artifact_entity.inventory_id
        assert call_args.name == sample_artifact_entity.name
        assert call_args.acquisition_date == sample_artifact_entity.acquisition_date
        assert call_args.department == sample_artifact_entity.department

    @pytest.mark.asyncio
    async def test_execute_publication_dto_creation(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_museum_api: AsyncMock,
        mock_catalog_api: AsyncMock,
        mock_message_broker: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_dto: ArtifactDTO,
        sample_artifact_entity: ArtifactEntity,
    ):
        """Test that publication DTO is created correctly"""
        # Arrange
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = None
        mock_museum_api.fetch_artifact.return_value = sample_artifact_dto
        mock_mapper.to_entity.return_value = sample_artifact_entity
        mock_catalog_api.publish_artifact.return_value = "public_id_123"

        # Act
        await get_artifact_use_case.execute(inventory_id)

        # Assert
        mock_catalog_api.publish_artifact.assert_called_once()
        call_args = mock_catalog_api.publish_artifact.call_args[0][0]
        
        assert isinstance(call_args, ArtifactCatalogPublicationDTO)
        assert call_args.inventory_id == sample_artifact_entity.inventory_id
        assert call_args.name == sample_artifact_entity.name
        assert call_args.era.value == sample_artifact_entity.era.value
        assert call_args.material.value == sample_artifact_entity.material.value
        assert call_args.description == sample_artifact_entity.description

    @pytest.mark.asyncio
    async def test_execute_with_different_inventory_id_formats(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_repository: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_entity: ArtifactEntity,
        sample_artifact_dto: ArtifactDTO,
    ):
        """Test execution with different inventory ID formats"""
        # Test with UUID object
        inventory_id_uuid = sample_artifact_entity.inventory_id
        mock_repository.get_by_inventory_id.return_value = sample_artifact_entity
        mock_mapper.to_dto.return_value = sample_artifact_dto

        result1 = await get_artifact_use_case.execute(inventory_id_uuid)
        assert result1 == sample_artifact_dto

        # Verify first call
        mock_repository.get_by_inventory_id.assert_called_once_with(str(inventory_id_uuid))

        # Reset mocks
        mock_repository.reset_mock()
        mock_mapper.reset_mock()

        # Test with string
        inventory_id_str = str(sample_artifact_entity.inventory_id)
        mock_repository.get_by_inventory_id.return_value = sample_artifact_entity
        mock_mapper.to_dto.return_value = sample_artifact_dto

        result2 = await get_artifact_use_case.execute(inventory_id_str)
        assert result2 == sample_artifact_dto

        # Verify second call
        mock_repository.get_by_inventory_id.assert_called_once_with(inventory_id_str)
