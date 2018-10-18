""" Helper functions and classes for tests
"""
from __future__ import absolute_import
import os
from aiida.utils.fixtures import PluginTestCase  # noqa

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
        raise ValueError("{} executable not found in PATH.".format(executable))

    return os.path.abspath(path)


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
