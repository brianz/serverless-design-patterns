import os
import boto3


TABLE_NAME = os.environ['DYNAMODB_RESULTS_TABLE_NAME']
AWS_REGION = os.environ['AWS_REGION']


class DynamoDB(dict):

    def __init__(self, *args, **kwargs):
        super(DynamoDB, self).__init__(*args, **kwargs)
        self._db = None
        self._table = None

    def connect(self, **kwargs):
        if not self._db:
            self._db = boto3.resource('dynamodb', region_name=AWS_REGION)
            self._table = self._db.Table(TABLE_NAME)

            #print("Looking up: %s" % (kwargs, ))
            data = self._table.get_item(Key=kwargs)
            record = data.get('Item', {})
            #print("Got record: %s" % (record, ))
            self.update(record)

    def save(self):
        item = {k: v for k, v in self.iteritems()}
        return self._table.put_item(Item=item)


class ClassiferResults(object):

    def __init__(self, url):
        self.__url = url
        self.__db = DynamoDB()
        self.__db.connect(url=url)

    @property
    def exists(self):
        return not self.is_empty

    @property
    def is_empty(self):
        return self.__db == {}

    def update(self, **kwargs):
        self.__db.update(kwargs)
        self.__db.save()
