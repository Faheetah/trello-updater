import pytest

from engine import Engine

class Foo():
    def __init__(self, callback, *args, **kwargs):
        self.foo = 'foo'
        self.tasks = {'bar': self.bar}
        self.callback = lambda x: callback(x)
    
    def bar(self, foo):
        self.foo = foo
        return self.foo
    

class Example():
    # module must include a callback for triggers and any initialization for config
    # if a module does not want to participate it can ignore it
    def __init__(self, callback, foo=None):
        self.foo = foo
        self.bar = 'bar'
        # list of tasks, needs to be whitelisted for clarity
        # can reference anything in relaity as long as it can execute
        self.tasks = {'task': self.task}
        self.callback = callback

    # trigger could be 
    def trigger(self, conditionals):
        self.callback(conditionals)

    def task(self, name, value):
        if getattr(self, name) is None:
            raise Exception('cannot be None!')
        setattr(self, name, value)
        return getattr(self, name)
    
@pytest.fixture
def engine():
    return lambda ruleset: Engine(ruleset, [Example, Foo])

ruleset = {
    'config': {'examplemodule': {'example': {'foo': 'foo'}}},
    'job1': {
        'triggers': [
            {'examplemodule': {'triggered': 'yes'}}
        ],
        'tasks': [
            {'examplemodule': {'task': {'name': 'foo', 'value': 'bar'}}}
        ]
    },
    'job2': {
        'triggers': [
            {'examplemodule': {'triggered': 'no', 'something': 'yes'}}
        ],
        'tasks': [
            {'examplemodule': {'task': {'name': 'bar', 'value': 'notbar'}}},
            # this fails it, and it should, because foo shouldn't be usable on noninitialized classes
            # {'example': {'task': {'name': 'foo', 'value': 'fail'}}},
            {'foo': {'bar': {'foo': 'baz'}}}
        ]
    }
}


def test_engine_runs_tasks(engine):
    e = engine(ruleset)
    em = e.modules['examplemodule']
    assert em.foo == 'foo'
    em.trigger({'triggered': 'no'})
    assert em.bar == 'bar'

def test_engine_runs_triggers(engine):
    e = engine(ruleset)
    em = e.modules['examplemodule']
    em.trigger({'triggered': 'yes'})
    assert em.foo == 'bar'
    assert em.bar == 'bar'

def test_engine_doesnt_trigger_multiple_conditionals(engine):
    e = engine(ruleset)
    em = e.modules['examplemodule']
    em.trigger({'triggered': 'no'})
    em.trigger({'triggered': 'yes'})
    assert em.bar == 'bar'

def test_engine_triggers_multiple_conditionals(engine):
    e = engine(ruleset)
    em = e.modules['examplemodule']
    em.trigger({'triggered': 'no', 'something': 'yes'})
    assert em.bar == 'notbar'

def test_regex_triggers(engine):
    ruleset = {
        'job1': {
            'triggers': [{
                'foo': {'bar': 'some REGEX-1234'}
            }],
            'tasks': [{
                'foo': {'bar': {'foo': 'baz'}}
            }]
        }
    }
    e = engine(ruleset)
    foo = e.modules['foo']
    foo.callback({'bar': '[a-z]+ [A-Z]+[0-9]+'})
    assert foo.foo == 'foo'
    foo.callback({'bar': '[a-z]+ [A-Z]+-[0-9]+'})
    assert foo.foo == 'baz'

def test_short_module_config(engine):
    ruleset = {'config': {'example': {'foo': 'foo'}}}
    e = engine(ruleset)
    assert e.modules['example'].foo == 'foo'

# def test_trello():
#     from trello.trello import Trello
#     with open('trello.yml') as t:
#         ruleset = t.read()

#     e = Engine(ruleset, [Trello, Foo])
#     e.modules['foo'].callback({'bar': False})
