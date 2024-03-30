class Identifier:
    def __init__(self, uuid=None, value=None, image_id=None, permalink=None, entity_def_id=None):
        self.uuid = uuid
        self.value = value
        self.image_id = image_id
        self.permalink = permalink
        self.entity_def_id = entity_def_id


class LocationIdentifier:
    def __init__(self, uuid=None, value=None, permalink=None, entity_def_id=None, location_type=None):
        self.uuid = uuid
        self.value = value
        self.permalink = permalink
        self.entity_def_id = entity_def_id
        self.location_type = location_type


class Linkedin:
    def __init__(self, value=None):
        self.value = value


class Fields:
    def __init__(self, rank_delta_d30=None, image_url=None, identifier=None, linkedin=None, short_description=None,
                 rank_org=None, created_at=None, location_identifiers=None, rank_delta_d90=None, website_url=None,
                 updated_at=None, rank_delta_d7=None, **kwargs):
        self.rank_delta_d30 = rank_delta_d30
        self.image_url = image_url
        self.identifier = Identifier(**identifier) if identifier else None
        self.linkedin = Linkedin(**linkedin) if linkedin else None
        self.short_description = short_description
        self.rank_org = rank_org
        self.created_at = created_at
        self.location_identifiers = [LocationIdentifier(
            **loc) for loc in location_identifiers] if location_identifiers else []
        self.rank_delta_d90 = rank_delta_d90
        self.website_url = website_url
        self.updated_at = updated_at
        self.rank_delta_d7 = rank_delta_d7


class Cards:
    def __init__(self, fields):
        self.fields = Fields(**fields)


class Organization:
    def __init__(self, properties: dict, cards: dict):
        identifier = properties.get("identifier")
        location_identifiers = properties.get("location_identifiers")
        short_description = properties.get("short_description")
        linkedin = properties.get("linkedin")

        self.identifier = Identifier(**identifier) if identifier else None

        self.location_identifiers: list[LocationIdentifier] = []
        if location_identifiers:
            for location in location_identifiers:
                self.location_identifiers.append(
                    LocationIdentifier(**location))

        self.short_description = short_description
        self.linkedin = Linkedin(**linkedin) if linkedin else None
        self.cards = Cards(fields=cards.get('fields'))
