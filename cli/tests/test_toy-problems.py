
from pytest import raises
from toy-problems.main import ToyProblemsTest

def test_toy-problems():
    # test toy-problems without any subcommands or arguments
    with ToyProblemsTest() as app:
        app.run()
        assert app.exit_code == 0


def test_toy-problems_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with ToyProblemsTest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_command1():
    # test command1 without arguments
    argv = ['command1']
    with ToyProblemsTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        assert data['foo'] == 'bar'
        assert output.find('Foo => bar')


    # test command1 with arguments
    argv = ['command1', '--foo', 'not-bar']
    with ToyProblemsTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        assert data['foo'] == 'not-bar'
        assert output.find('Foo => not-bar')
