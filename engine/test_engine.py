import pytest

from engine import Engine

class Foo():
    def __init__(self, *args, **kwargs):
        self.tasks = {'bar': self.bar}

    def bar(self, baz):
        return baz

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
    def trigger(self, triggered=None):
        self.callback(triggered=triggered)

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
            {'examplemodule': {'triggered': 'no'}}
        ],
        'tasks': [
            {'examplemodule': {'task': {'name': 'bar', 'value': 'notbar'}}},
            # this fails it, and it should, because foo shouldn't be usable on noninitialized classes
            # {'example': {'task': {'name': 'foo', 'value': 'fail'}}},
            {'foo': {'bar': {'baz': 'baz'}}}
        ]
    }
}


def test_engine_runs_tasks(engine):
    e = engine(ruleset)
    examplemodule = e.modules['examplemodule']
    assert examplemodule.bar == 'bar'
    examplemodule.trigger(triggered='no')
    assert examplemodule.foo == 'foo'
    assert examplemodule.bar == 'notbar'
    examplemodule.trigger(triggered='yes')
    assert examplemodule.foo == 'bar'
