""" Helper functions and classes for tests
"""
from __future__ import absolute_import
import os
from aiida.manage.fixtures import PluginTestCase

__all__ = ('PluginTestCase', 'get_backend', 'get_path_to_executable',
           'get_computer', 'get_code')

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
EXECUTABLES = {
    'zeopp.network': 'network',
}


def get_backend():
    from aiida.backends.profile import BACKEND_DJANGO, BACKEND_SQLA
    if os.environ.get('TEST_AIIDA_BACKEND') == BACKEND_SQLA:
        return BACKEND_SQLA
    return BACKEND_DJANGO


def get_path_to_executable(executable):
    """ Get path to local executable.

    :param executable: Name of executable in the $PATH variable
    :type executable: str

    :return: path to executable
    :rtype: str
    """
    # pylint issue https://github.com/PyCQA/pylint/issues/73
    import distutils.spawn  # pylint: disable=no-name-in-module,import-error
    path = distutils.spawn.find_executable(executable)
    if path is None:
        raise ValueError('{} executable not found in PATH.'.format(executable))

    return os.path.abspath(path)


def get_computer(name):
    """Set up localhost computer"""
    from aiida.orm import Computer
    from aiida.common import NotExistent

    try:
        computer = Computer.objects.get(name=name)
    except NotExistent:

        import tempfile
        computer = Computer(
            name=name,
            description='localhost computer set up by aiida_zeopp tests',
            hostname=name,
            workdir=tempfile.mkdtemp(),
            transport_type='local',
            scheduler_type='direct',
        )
        computer.store()
        computer.configure()

    return computer


def get_code(entry_point, computer_name='localhost-test'):
    """Set up code on provided computer"""
    from aiida.orm import Code

    executable = EXECUTABLES[entry_point]

    try:
        codes = Code.objects.find(filters={'label': executable})  # pylint: disable=no-member
        code = codes[0]
    except IndexError:
        path = get_path_to_executable(executable)
        code = Code(
            input_plugin_name=entry_point,
            remote_computer_exec=[get_computer(computer_name), path],
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
