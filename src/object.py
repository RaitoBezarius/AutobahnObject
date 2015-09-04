from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import RegisterOptions, SubscribeOptions
from twisted.internet.defer import inlineCallbacks, returnValue

import uuid

class ObjectService(ApplicationSession):

    def __init__(self, config=None):
        super(ObjectService, self).__init__(config)

        self.objects = {}
        self.objects_by_id = {}

    def generate_uuid(self):
        return str(uuid.uuid4())

    def extract_object_id(self, details):
        topic = getattr(details, 'topic', getattr(details, 'procedure', None))
        if topic is None:
            raise RuntimeError('Unknown URL attribute.')
        parts = topic.split('.')
        return parts[parts.index('objects') + 1]

    @inlineCallbacks
    def onJoin(self, details):
        print ('Session joined for the Object Service.')

        yield self.register(self.create, u'com.objects.create')
        yield self.register(self.get, u'com.objects..get', RegisterOptions(match=u'wildcard', details_arg='details'))
        yield self.register(self.delete, u'com.objects..delete', RegisterOptions(match=u'wildcard', details_arg='details'))
        yield self.subscribe(self.update, u'com.objects..update', SubscribeOptions(match=u'wildcard', details_arg='details'))

    def create(self, object_type, object_data):
        object_data['id'] = self.generate_uuid()
        object_data['type'] = object_type

        self.objects.setdefault(object_type, [])
        self.objects[object_type].append(object_data)
        self.objects_by_id[object_data['id']] = object_data

        return object_data['id']

    def update(self, new_data, details=None):
        try:
            object_id = self.extract_object_id(details)
            obj = self.objects_by_id.get(object_id, None)
            if obj is None:
                raise ValueError('Object does not exists')
            else:
                if 'id' in new_data or 'type' in new_data:
                    raise RuntimeError('Forbidden change of id or type attribute of the object')

                obj.update(new_data) # automatically update all others stores.
        except Exception as e:
            raise e

    def get(self, details=None):
        try:
            object_id = self.extract_object_id(details)
            return self.objects_by_id.get(object_id, None)
        except Exception as e:
            raise e

    def delete(self, details):
        try:
            object_id = self.extract_object_id(details)
            object = self.objects_by_id[object_id]
            del self.objects_by_id[object_id]
            del self.objects[object['type']]
        except Exception as e:
            raise e
