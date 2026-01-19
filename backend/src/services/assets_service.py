from sqlalchemy.orm import Session
from sqlalchemy import or_ , asc , desc , func
import uuid
from datetime import datetime , timezone

from backend.src.models.asset import Asset
from backend.src.schemas.asset import AssetCreate, AssetUpdate


class AssetService:
    
    def __init__(self, db: Session, logger):
        self.db = db
        self.logger = logger

    def create_asset(self, asset: AssetCreate):

        """
            basically a func to create an asset and try to log it into the db
            if we couldn't for some reason then rollback on the db
        """

        try: 
            
            asset = Asset(
                id = str(uuid.uuid4()),
                name = asset.name,
                category=asset.category,
                value=asset.value,
                quantity=asset.quantity,
                status=asset.status,
                purchase_date=asset.purchase_date,
                created_at=datetime.now(timezone.utc)
            )

            self.db.add(asset)
            self.db.commit()
            self.db.refresh(asset)
            self.logger.info("Logged an asset record to the DB")
            return asset, None
        
        except Exception as e:
            self.logger.error(f"couldn't log the asset to the DB ... error: {e}")
            self.db.rollback()
            return None, str(e)


    def get_asset_by_id(self, asset_id):
        "retrieving an a single asset from the DB"
        try:
            asset = self.db.query(Asset).filter(Asset.id == asset_id).first()

            if asset is None:
                self.logger.warning(f"Asset with ID {asset_id} not found")
                return None, "Asset not found"
            
            self.logger.info("retrieving an Asset record from the DB")
            return asset, None
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            return None, str(e)
        

    def get_all_assets(self, skip = 0, limit = 100):

        "retrieving all the assets in the DB"
        try:
            assets = self.db.query(Asset).offset(skip).limit(limit).all()

            if not assets:
                self.logger.warning("No Assets found in the DB")
                return [] , None

            self.logger.info("retrieving Assets from the DB")
            return assets, None
        
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            return None, str(e)
        

    def update_asset(self, asset_update : AssetUpdate ,asset_id):

        # get the the asset to update
        db_asset, error = self.get_asset_by_id(asset_id)

        # check if we actually got somehting
        if error:
            return None, error
        
        # now let's update it
        try:

            update_data = asset_update.model_dump(exclude_unset=True)

            for key , value in update_data.items():
                setattr(db_asset , key , value)

            # commit if we did it but rollback if we didn't gang
            self.db.commit()
            self.db.refresh(db_asset)
            return db_asset, None
        except Exception as e:
            self.logger.error(f"DB Error while updating the DB {e}")
            self.db.rollback()
            return None, str(e)


    def delete_asset(self, asset_id):

        # 1st let's get the asset record
        asset, error = self.get_asset_by_id(asset_id)

        if error:
            return False, error
        
        # since we found it so let's delete it
        try:
            self.db.delete(asset)
            self.db.commit()
            return True, None
        

        except Exception as e:
            self.logger.error(f"DB Error while deleting asset with id {asset_id}")
            self.db.rollback()
            return False, str(e)
        
    def search_asset(self , query : str):
        "a method to search for asset by its name or category"

        try:
            result = self.db.query(Asset).filter(
                or_(
                    Asset.name.ilike(f"%{query}%"),
                    Asset.category.ilike(f"%{query}%")
                )
            ).all()

            if not result:
                self.logger.warning("No Assets found in the DB")
                return [] , None
            
            self.logger.info(f"query : {query} returned smth {result}")
            return result , None
        except Exception as e:
            self.logger.error(f"DB error while querying it {e}")
            return None , str(e)
        
    
    def get_max_value(self):

        try:
            asset = self.db.query(Asset).order_by(Asset.value.desc()).first()

            if asset is None:
                self.logger.warning(f"Couldn't find max value for any asset")
                return None, "Asset not found"
            
            self.logger.info("retrieving the max asset")
            return asset, None
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            return None, str(e)
        
    def get_min_value(self):

        try:
            asset = self.db.query(Asset).order_by(Asset.value.asc()).first()

            if asset is None:
                self.logger.warning(f"Couldn't find min value for any asset")
                return None, "Asset not found"
            
            self.logger.info("retrieving the min asset")
            return asset, None
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            return None, str(e)
        
    def get_asset_values_mean(self):

        try:
            result = self.db.query(func.avg(Asset.value)).scalar()

            if result is None:
                self.logger.warning(f"Couldn't find the avg value for the assets")
                return None, "Asset not found"
            
            self.logger.info("retrieving the mean value of the assets")
            return round(result, 2), None if result else 0.0 , None
        except Exception as e:
            self.logger.error(f"DB Error: {e}")
            return None, str(e)

        



