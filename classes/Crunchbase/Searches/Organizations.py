class Identifier:
    def __init__(self, permalink=None, image_id=None, uuid=None, entity_def_id=None, value=None):
        self.permalink = permalink
        self.image_id = image_id
        self.uuid = uuid
        self.entity_def_id = entity_def_id
        self.value = value


class Category:
    def __init__(self, entity_def_id=None, permalink=None, uuid=None, value=None):
        self.entity_def_id = entity_def_id
        self.permalink = permalink
        self.uuid = uuid
        self.value = value


class Entity:
    def __init__(self, uuid=None, properties=None):
        self.uuid = uuid
        properties = properties or {}
        self.identifier = Identifier(**properties.get('identifier', {}))
        self.short_description = properties.get('short_description')
        self.categories = [Category(**category)
                           for category in properties.get('categories', [])]
        self.rank_org = properties.get('rank_org')


class Organization:
    def __init__(self, count=None, entities=None):
        self.count = count
        self.entities = [Entity(entity['uuid'], entity['properties'])
                         for entity in entities] if entities else []
