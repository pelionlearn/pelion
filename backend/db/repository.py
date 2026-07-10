from db.database import Session


def create(model, **kwargs):
    with Session() as session:
        obj = model(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj


def delete(model, id):
    with Session as session:
        obj = session.get(model, id)
        if obj:
            session.delete(obj)
            session.commit()
