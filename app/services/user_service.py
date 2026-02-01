from sqlalchemy.orm import Session
from app.models.user import User


class UserService:

    # get id, name and email from firebase
    def get_userdata(db : Session, firebase_uid : str, name: str, email:str):
        check_user= db.query(User).filter(User.id==firebase_uid).first()

        if check_user:
            return check_user
        else:
            new_user=User(id=firebase_uid, email=email, name=name)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user
