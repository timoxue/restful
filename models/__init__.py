import datetime
import collections

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
            #print(attribute)
            setattr(self, attribute, attributes[attribute])
        return self

    def add_attr(self, k, v):
        return self

    def remove_attr(self, k):
        delattr(self, k)
        return self

class Combined:
    def __init__(self,  *args):
        self.class_list = args
        self.list_l = len(args)
        self.exclude_list=[]
        self.columns_list = []
        self.filter_list = []
        self.get_column_list(args)
        self.filter_list = self.columns_list
    
    def get_column_list(self, args):
        for s in args:
            if type(s) is list:
                self.columns_list.append(s[0].keys())
            else:
                self.columns_list.append(s.__table__.columns.keys())

    def exclude(self, *args):
        self.exclude_list = args
        self.filter_list = list(map(self.differ, self.columns_list, self.exclude_list))
        return self

    def differ(self, a , b):
        a_multiset = collections.Counter(a)
        b_multiset = collections.Counter(b)
        #print(a_multiset, b_multiset)
        #overlap = list((a_multiset & b_multiset).elements())
        a_remainder = list((a_multiset - b_multiset).elements())
        #b_remainder = list((b_multiset - a_multiset).elements())

        return a_remainder

    def to_dict(self, results):
        #print(self.filter_list)

        final = []
        
        if type(results) is not list:
            results = [results]
        for result in results:
            value = {}
            for i in range(0, self.list_l):
                 for column in self.filter_list[i]:
                    attribute = getattr(result[i], column)
                    if isinstance(attribute, datetime.datetime):
                        attribute = str(attribute)
                    value[column] = attribute
                #for key in result[i].__table__.columns.keys(), getattr(result[i], 'id'))
                #return [dict(zip(result.keys(), result)) for result in results]
            final.append(value)
        #print(value)
        return final