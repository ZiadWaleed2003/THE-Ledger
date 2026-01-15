import unittest
from unittest.mock import MagicMock, ANY
from datetime import datetime, timezone
import uuid

from backend.src.services.assets_service import AssetService
from backend.src.schemas.asset import AssetCreate, AssetUpdate
from backend.src.models.asset import Asset

class TestAssetService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_logger = MagicMock()
        self.service = AssetService(self.mock_db, self.mock_logger)

    def test_create_asset_success(self):
        # Arrange
        asset_create = AssetCreate(
            name="Test Asset",
            category="Test Category",
            value=100.0,
            quantity=1.0,
            status="Active",
            purchase_date=datetime.now(timezone.utc)
        )
        
        # Act
        result = self.service.create_asset(asset_create)

        # Assert
        self.assertTrue(result)
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()
        self.mock_logger.info.assert_called_with("Logged an asset record to the DB")

    def test_create_asset_failure(self):
        # Arrange
        asset_create = AssetCreate(
            name="Test Asset",
            category="Test Category",
            value=100.0,
            quantity=1.0,
            status="Active"
        )
        self.mock_db.add.side_effect = Exception("DB Error")

        # Act
        result = self.service.create_asset(asset_create)

        # Assert
        self.assertFalse(result)
        self.mock_db.rollback.assert_called_once()
        self.mock_logger.error.assert_called()

    def test_get_asset_by_id_found(self):
        # Arrange
        asset_id = "test-id"
        mock_asset = Asset(id=asset_id, name="Test")
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_asset

        # Act
        result = self.service.get_asset_by_id(asset_id)

        # Assert
        self.assertEqual(result, mock_asset)
        self.mock_logger.info.assert_called_with("retrieving an Asset record from the DB")

    def test_get_asset_by_id_not_found(self):
        # Arrange
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = self.service.get_asset_by_id("missing-id")

        # Assert
        self.assertIsNone(result)
        self.mock_logger.warning.assert_called()

    def test_get_asset_by_id_exception(self):
        # Arrange
        self.mock_db.query.side_effect = Exception("DB Error")

        # Act
        result = self.service.get_asset_by_id("test-id")

        # Assert
        self.assertIsNone(result)
        self.mock_logger.error.assert_called()

    def test_get_all_assets_found(self):
        # Arrange
        mock_assets = [Asset(id="1"), Asset(id="2")]
        self.mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_assets

        # Act
        result = self.service.get_all_assets()

        # Assert
        self.assertEqual(result, mock_assets)
        self.mock_logger.info.assert_called()

    def test_get_all_assets_empty(self):
        # Arrange
        self.mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = []

        # Act
        result = self.service.get_all_assets()

        # Assert
        self.assertEqual(result, [])
        self.mock_logger.warning.assert_called()

    def test_get_all_assets_exception(self):
        # Arrange
        self.mock_db.query.side_effect = Exception("DB Error")

        # Act
        result = self.service.get_all_assets()

        # Assert
        self.assertIsNone(result)
        self.mock_logger.error.assert_called()

    def test_update_asset_success(self):
        # Arrange
        asset_id = "test-id"
        mock_asset = MagicMock(spec=Asset)
        self.service.get_asset_by_id = MagicMock(return_value=mock_asset)
        
        update_data = AssetUpdate(name="Updated Name")
        
        # Act
        result = self.service.update_asset(update_data, asset_id)

        # Assert
        self.assertTrue(result)
        self.assertEqual(mock_asset.name, "Updated Name")
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_with(mock_asset)

    def test_update_asset_not_found(self):
        # Arrange
        self.service.get_asset_by_id = MagicMock(return_value=None)
        update_data = AssetUpdate(name="Updated Name")

        # Act
        result = self.service.update_asset(update_data, "missing-id")

        # Assert
        self.assertFalse(result)
        self.mock_logger.error.assert_called_with("couldn't find any asset to update")

    def test_update_asset_exception(self):
        # Arrange
        mock_asset = MagicMock(spec=Asset)
        self.service.get_asset_by_id = MagicMock(return_value=mock_asset)
        self.mock_db.commit.side_effect = Exception("DB Error")
        update_data = AssetUpdate(name="Updated Name")

        # Act
        result = self.service.update_asset(update_data, "test-id")

        # Assert
        self.assertFalse(result)
        self.mock_db.rollback.assert_called_once()
        self.mock_logger.error.assert_called()

    def test_delete_asset_success(self):
        # Arrange
        mock_asset = MagicMock(spec=Asset)
        self.service.get_asset_by_id = MagicMock(return_value=mock_asset)

        # Act
        result = self.service.delete_asset("test-id")

        # Assert
        self.assertTrue(result)
        self.mock_db.delete.assert_called_with(mock_asset)
        self.mock_db.commit.assert_called_once()

    def test_delete_asset_not_found(self):
        # Arrange
        self.service.get_asset_by_id = MagicMock(return_value=None)

        # Act
        result = self.service.delete_asset("missing-id")

        # Assert
        self.assertFalse(result)
        self.mock_logger.error.assert_called_with("couldn't find any asset to delete")

    def test_delete_asset_exception(self):
        # Arrange
        mock_asset = MagicMock(spec=Asset)
        self.service.get_asset_by_id = MagicMock(return_value=mock_asset)
        self.mock_db.delete.side_effect = Exception("DB Error")

        # Act
        result = self.service.delete_asset("test-id")

        # Assert
        self.assertFalse(result)
        self.mock_db.rollback.assert_called_once()
        self.mock_logger.error.assert_called()

if __name__ == '__main__':
    unittest.main()
