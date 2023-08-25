""" Helper functions and classes for tests
"""
import os
import shutil
import tempfile

from aiida.common import NotExistent
from aiida.common.folders import Folder
from aiida.orm import Code, Computer

__all__ = ("get_path_to_executable", "get_computer", "get_code")

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
EXECUTABLES = {
    "zeopp.network": "network",
}


def get_path_to_executable(executable):
    """Get path to local executable.

    :param executable: Name of executable in the $PATH variable
    :type executable: str

    :return: path to executable
    :rtype: str
    """
    path = shutil.which(executable)
    if path is None:
        raise ValueError(f"{executable} executable not found in PATH.")

    return os.path.abspath(path)


def get_computer(name):
    """Set up localhost computer"""

    try:
        computer = Computer.objects.get(label=name)
    except NotExistent:
        computer = Computer(
            label=name,
            description="localhost computer set up by aiida_zeopp tests",
            hostname=name,
            workdir=tempfile.mkdtemp(),
            transport_type="core.local",
            scheduler_type="core.direct",
        )
        computer.store()
        computer.configure()

    return computer


def get_code(entry_point, computer_name="localhost-test"):
    """Set up code on provided computer"""

    executable = EXECUTABLES[entry_point]

    try:
        codes = Code.objects.find(filters={"label": executable})  # pylint: disable=no-member
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

    return Folder(tempfile.mkdtemp())
