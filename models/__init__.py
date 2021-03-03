import datetime

class Serializrable(object):
    """A SQLAlchemy mixin class that can serialize itself as a JSON object"""

    def to_dict(self):
        """Return dict representation of class by iterating over database columns."""
        value = {}
        for column in self.__table__.columns:
            attribute = getattr(self, column.name)
            if isinstance(attribute, datetime.datetime):
                attribute = str(attribute)
            value[column.name] = attribute
        return value

    def from_dict(self, attributes):
        """Update the current instance base on attribute->value by *attributes*"""
        for attribute in attributes:
            print(attribute)
            setattr(self, attribute, attributes[attribute])
        return self