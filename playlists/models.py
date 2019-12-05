from neomodel import RelationshipTo, StructuredNode, StringProperty, DateTimeProperty
from datetime import datetime

class User(StructuredNode):
    username = StringProperty(unique_index=True)
    created = DateTimeProperty(default=lambda: datetime.now())
    name = StringProperty()

    likes = RelationshipTo('Task', 'LIKES')
    dislikes = RelationshipTo('Task', 'DISLIKES')

class Task(StructuredNode):
    task = StringProperty(unique_index=True)
