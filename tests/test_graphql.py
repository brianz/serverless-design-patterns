from cupping.handlers.graphql import schema
from factories import SessionFactory


def test_basic():
    s = SessionFactory.create_batch(3)
    query = '''
    query allCuppings {
          cuppings {
            id
            name
            formName
            created
          }
    }
    '''
    #import pdb; pdb.set_trace()
    result = schema.execute(query)
    print(result.errors)
    print(result.data)



def no_test_basic_subselectionkkkk():
    s = SessionFactory.create_batch(3)
    query = '''
    query allCuppings {
          cuppings {
            id
            name
            formName
          }
    }
    '''
    #query = '{ cuppings }'
    #import pdb; pdb.set_trace()
    result = schema.execute(query)
    print(result.errors)
    print(result.data)
