from database.models import app, db, Client, Flight, Booking, BoardingCheck, Baggage


def create_entity(model_class, **kwargs):
    session = db.session
    entity = model_class(**kwargs)
    session.add(entity)
    session.commit()
    return entity


def update_entity(entity, **kwargs):
    session = db.session
    for key, value in kwargs.items():
        setattr(entity, key, value)
    session.commit()
    return entity

def delete_entity(entity):
    session = db.session
    session.delete(entity)
    session.commit()