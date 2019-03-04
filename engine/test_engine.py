import pytest

from engine import Engine

class Example(object):
    def __init__(self, foo=None):
        self.foo = foo
        self.tasks = {'task': self.task}

    def task(self, name, value):
        setattr(self, name, value)
        return getattr(self, name)

    def trigger(self, job):
        for task in job.tasks:
            task.run()


@pytest.fixture
def engine():
    return lambda ruleset: Engine(ruleset, [Example])

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
            {'foo': {'bar': {'foo': 'baz'}}}
        ]
    }
}


def test_engine_loads_modules(engine):
    e = Engine({'config': {'examplemodule': {'example': {'foo': 'foo'}}}}, [Example])
    assert e.modules['example'].foo == None
    assert e.modules['examplemodule'].foo == 'foo'

def test_engine_runs_tasks(engine):
    ruleset = {'job1': {
            'triggers': {'example': {'immediate': True}}, 
            'tasks': {'example': {'task': {'name': 'foo', 'value': 'bar'}}}}
        }
    e = Engine(ruleset, [Example])
    assert e.modules['example'].foo == 'bar'


# def test_engine_runs_triggers(engine):
#     e = engine(ruleset)
#     em = e.modules['examplemodule']
#     em.trigger({'triggered': 'yes'})
#     assert em.foo == 'bar'
#     assert em.bar == 'bar'

# def test_engine_doesnt_trigger_multiple_conditionals(engine):
#     e = engine(ruleset)
#     em = e.modules['examplemodule']
#     em.trigger({'triggered': 'no'})
#     em.trigger({'triggered': 'yes'})
#     assert em.bar == 'bar'

# def test_engine_triggers_multiple_conditionals(engine):
#     e = engine(ruleset)
#     em = e.modules['examplemodule']
#     em.trigger({'triggered': 'no', 'something': 'yes'})
#     assert em.bar == 'notbar'

# def test_regex_triggers(engine):
#     ruleset = {
#         'job1': {
#             'triggers': [{
#                 'foo': {'bar': 'some REGEX-1234'}
#             }],
#             'tasks': [{
#                 'foo': {'bar': {'foo': 'baz'}}
#             }]
#         }
#     }
#     e = engine(ruleset)
#     foo = e.modules['foo']
#     foo.callback({'bar': '[a-z]+ [A-Z]+[0-9]+'})
#     assert foo.foo == 'foo'
#     foo.callback({'bar': '[a-z]+ [A-Z]+-[0-9]+'})
#     assert foo.foo == 'baz'

# def test_short_module_config(engine):
#     ruleset = {'config': {'example': {'foo': 'foo'}}}
#     e = engine(ruleset)
#     assert e.modules['example'].foo == 'foo'
