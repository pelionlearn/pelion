from db.database import Session
from db.models import Class, ClassroomMember
from uuid import UUID


def get_classroom_members(class_id: UUID):
    with Session() as session:
        class_obj = session.get(Class, class_id)
        if class_obj is None:
            raise Exception
        return class_obj.members


def add_classroom_member(class_id: UUID, user_id: UUID):
    with Session() as session:
        class_member = ClassroomMember(class_id=class_id, user_id=user_id)
        session.add(class_member)
        session.commit()
        session.refresh(class_member)
        return class_member


def remove_classroom_member(class_id: UUID, user_id: UUID):
    with Session() as session:
        class_member = session.get(ClassroomMember, (class_id, user_id))
        if class_member:
            session.delete(class_member)
            return class_member
        else:
            return None
