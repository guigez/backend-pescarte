from typing import Tuple
from sqlalchemy.exc import SQLAlchemyError

from src.database import Session


class BaseSQLModel:
    """Basic CRUD for models"""

    # TODO add correct documentation to each function of the class
    def update(self, db: Session, update_args: dict):
        try:
            for attr, value in update_args.items():
                setattr(self, attr, value)
            db.commit()
            return self, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def save(self, db: Session) -> Tuple["BaseSQLModel", bool | str]:
        try:
            db.add(self)
            db.commit()
            db.refresh(self)
            return self, False
        except SQLAlchemyError as error:
            print(error)
            return False, ''.join(error.args)

    def delete(self, db: Session):
        try:
            db.delete(self)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)
