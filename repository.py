from sqlalchemy import select, delete, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import *


class CareerManagerDB:
    # set logging=True to log all SQL queries
    def __init__(self, path="sqlite:///application.db", logging=False):
        self.engine = create_engine(path, echo=logging)
        Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.session = Session()
        
        
    def user_exists(self, email) -> bool:
        
        user = self.session.query(AppUser).filter(AppUser.email == email).first()
        if user:
            return True
        else:
            return False  
    
    def add_user(self, new_user_name, new_user_email, password):
        try:
            self.session.add(AppUser(name=new_user_name, email= new_user_email, password=password ))
            self.session.commit()
            return "Account created Succesfully"
        except:
            return "It seems this email has been used before"
            

    def add_career(self, title, description, user_id):
        self.session.add(Career(title=title, description= description, user_id= user_id ))
        self.session.commit()
    
    
    def get_user(self, user_id_to_lookup):
        result = self.session.get(AppUser, user_id_to_lookup)
        # if result == None:
        #     raise Exception(f"User not Found")
        return result
    
    def get_career(self, career_id_to_lookup):
        result = self.session.get(Career, career_id_to_lookup)
        if result == None:
            raise Exception(f"User not Found")
        return result

    def find_user_by_email(self, email):
        user = self.session.query(AppUser).filter_by(email=email).first()
        return user
    # breakpoint() 
    def find_careers_by_user_id(self, user_id):
        careers = self.session.query(Career).join(AppUser).filter(AppUser.id == user_id).all()
        # if len(careers) == 0:
            
        return careers
    
    def update_career(self, career_id, new_title, new_description, new_status):
        career = self.session.get(Career, career_id)
        if career is None:
            return {"error": "career not found"}
        career.title = new_title
        career.description = new_description
        career.status = new_status
        self.session.commit()
        self.session.refresh(career)
        return career

    
    
    def update_user(self, user_id, new_name):
        user = self.session.get(AppUser, user_id)
        if user is None:
            Exception("User  not found")
        user.name = new_name
        self.session.commit()
        self.session.refresh(user)
        return user


    def remove_user(self, user_id_to_remove):
        count = self.session.execute(
            delete(AppUser).where(AppUser.id == user_id_to_remove)
        ).rowcount
        self.session.commit()
        if count == 0:
            raise Exception(f"No user with ID {user_id_to_remove}.")
        
        
    def remove_career(self, career_id_to_remove):
        count = self.session.execute(
            delete(Career).where(Career.id == career_id_to_remove)
        ).rowcount
        self.session.commit()
        if count == 0:
            raise Exception(f"No career with ID {career_id_to_remove}.")

    def get_users (self):
        return self.session.scalars(select(AppUser)).all()

    def search_careers_by_name(self, career_to_lookup):
        return (
            self.session.query(Career)
            .filter(Career.title.ilike("%" + career_to_lookup + "%"))
            .all()
        )
