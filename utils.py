from main_folder.models import Session


def create_entity(model_class, **kwargs):
    session = Session()
    entity = model_class(**kwargs)
    session.add(entity)
    session.commit()
    return entity


def update_entity(entity, **kwargs):
    session = Session()
    for key, value in kwargs.items():
        setattr(entity, key, value)
    session.commit()
    return entity


def delete_entity(entity):
    session = Session()
    session.delete(entity)
    session.commit()
