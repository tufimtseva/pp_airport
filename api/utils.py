from init import db


def create_entity(model_class, **kwargs):
    entity = model_class(**kwargs)
    db.session.add(entity)
    db.session.commit()
    return entity


def update_entity(entity, **kwargs):
    for key, value in kwargs.items():
        setattr(entity, key, value)
    db.session.commit()
    return entity


def delete_entity(entity):
    db.session.delete(entity)
    db.session.commit()
