""" Helper functions and classes for tests
"""
import os
import aiida.utils.fixtures
import unittest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def get_backend():
    from aiida.backends.profile import BACKEND_DJANGO, BACKEND_SQLA
    if os.environ.get('TEST_AIIDA_BACKEND') == BACKEND_SQLA:
        return BACKEND_SQLA
    return BACKEND_DJANGO


def get_zeopp_binary():
    import distutils.spawn

    binary = 'network'
    path = distutils.spawn.find_executable(binary)
    if path is None:
        raise ValueError("{} binary not found in PATH.".format(binary))
    return path


def get_localhost_computer():
    """Setup localhost computer"""
    from aiida.orm import Computer
    import tempfile
    computer = Computer(
        name='localhost',
        description='my computer',
        hostname='localhost',
        workdir=tempfile.mkdtemp(),
        transport_type='local',
        scheduler_type='direct',
        enabled_state=True)

    return computer


def get_network_code(computer):
    """Setup code on computer"""
    from aiida.orm import Code

    path = get_zeopp_binary()

    code = Code(
        input_plugin_name='zeopp.network',
        remote_computer_exec=[computer, path],
    )
    code.label = 'zeopp'
    code.description = 'zeo++'

    return code


def get_temp_folder():
    """Returns AiiDA folder object.
    
    Useful for calculation.submit_test()
    """
    from aiida.common.folders import Folder
    import tempfile

    return Folder(tempfile.mkdtemp())


fixture_manager = aiida.utils.fixtures.FixtureManager()
fixture_manager.backend = get_backend()


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
        from aiida.utils.capturing import Capturing
        cls.fixture_manager = fixture_manager
        if not fixture_manager.has_profile_open():
            with Capturing():
                cls.fixture_manager.create_profile()

    def tearDown(self):
        self.fixture_manager.reset_db()

    #@classmethod
    #def tearDownClass(cls):
    #    cls.fixture_manager.destroy_all()
