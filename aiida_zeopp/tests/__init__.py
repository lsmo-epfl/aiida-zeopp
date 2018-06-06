""" Helper functions and classes for tests
"""
import os
import unittest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
executables = {
    'zeopp.network': 'network',
}


def get_backend():
    from aiida.backends.profile import BACKEND_DJANGO, BACKEND_SQLA
    if os.environ.get('TEST_AIIDA_BACKEND') == BACKEND_SQLA:
        return BACKEND_SQLA
    return BACKEND_DJANGO


def get_path_to_executable(executable):
    import distutils.spawn
    path = distutils.spawn.find_executable(executable)
    if path is None:
        raise ValueError("{} executable not found in PATH.".format(executable))

    return path


def get_computer(name='localhost'):
    """Setup localhost computer"""
    from aiida.orm import Computer
    from aiida.common.exceptions import NotExistent

    try:
        computer = Computer.get(name)
    except NotExistent:

        import tempfile
        computer = Computer(
            name=name,
            description='localhost computer set up by aiida_gudhi tests',
            hostname='localhost',
            workdir=tempfile.mkdtemp(),
            transport_type='local',
            scheduler_type='direct',
            enabled_state=True)
        computer.store()

    return computer


def get_code(entry_point, computer_name='localhost'):
    """Setup code on localhost computer"""
    from aiida.orm import Code
    from aiida.common.exceptions import NotExistent

    computer = get_computer(computer_name)
    executable = executables[entry_point]

    try:
        code = Code.get_from_string('{}@{}'.format(executable, computer_name))
    except NotExistent:
        path = get_path_to_executable(executable)
        code = Code(
            input_plugin_name=entry_point,
            remote_computer_exec=[computer, path],
        )
        code.label = executable
        code.store()

    return code


def get_temp_folder():
    """Returns AiiDA folder object.
    
    Useful for calculation.submit_test()
    """
    from aiida.common.folders import Folder
    import tempfile

    return Folder(tempfile.mkdtemp())


#TODO: Replace this class by aiida.utils.fixtures.PluginTestCase when aiida-core v0.12.1 is released
class PluginTestCase(unittest.TestCase):
    """
    Set up a complete temporary AiiDA environment for plugin tests

    Filesystem:

        * temporary config (``.aiida``) folder
        * temporary repository folder

    Database:

        * temporary database cluster via the ``pgtest`` package
        * with aiida database user
        * with aiida_db database

    AiiDA:

        * set to use the temporary config folder
        * create and configure a profile
    """

    @classmethod
    def setUpClass(cls):
        from aiida.utils.fixtures import _PYTEST_FIXTURE_MANAGER
        cls.fixture_manager = _PYTEST_FIXTURE_MANAGER

    def tearDown(self):
        self.fixture_manager.reset_db()
