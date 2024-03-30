class Identifier:
    def __init__(self, uuid=None, value=None, image_id=None, permalink=None, entity_def_id=None):
        self.uuid = uuid
        self.value = value
        self.image_id = image_id
        self.permalink = permalink
        self.entity_def_id = entity_def_id


class Entity:
    def __init__(self, facet_ids=None, identifier=None, short_description=None):
        self.facet_ids = facet_ids
        self.identifier = Identifier(**identifier) if identifier else None
        self.short_description = short_description


class Autocomplete:
    def __init__(self, count=None, entities=None):
        self.count = count
        self.entities = [Entity(**entity)
                         for entity in entities] if entities else []
