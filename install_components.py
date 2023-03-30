"""_summary_

Install components for Burrito
"""

import os
import sys
import subprocess


class PackageManager:
    def __init__(
            self,
            package_manager_name: str,
            linux_distributive_list: list[str],
            install_commands: list[str]) -> None:

        self.__name = package_manager_name
        self.__linux_distributive_list = linux_distributive_list
        self.__install_commands = install_commands

    @property
    def name(self) -> str:
        """_summary_

        Returns:
            str: package manager name
        """

        return self.__name

    @property
    def linux_distributive_list(self) -> list[str]:
        """_summary_

        Returns:
            list[str]: linux distributive list
        """

        return self.__linux_distributive_list

    @property
    def commands(self) -> list[str]:
        """_summary_

        Returns:
            list[str]: commands to install needed components
        """

        return self.__install_commands

    def install(self) -> None:
        """_summary_

        Install needed components
        """

        for command in self.__install_commands:
            subprocess.call(command)


def get_package_manager(
        package_managers: tuple[PackageManager],
        linux_distributive_name: str) -> PackageManager | None:

    """_summary_

    Return package manager used for current OS

    Returns:
        PackageManager | None: package manager object or None
    """

    for manager in package_managers:
        if linux_distributive_name in manager.linux_distributive_list:
            return manager


OS_NAME = os.name
if OS_NAME == "nt":
    # TODO: for Windows

    sys.exit(0)

elif OS_NAME == "posix":
    import distro

    linux_distributive = distro.id()

    _package_managers = (
        PackageManager("apt", ["ubuntu", "debian"], []),
        PackageManager("yum", ["rhel", "centos", "fedora", "oracle", ""], [])
    )

    manager = get_package_manager(_package_managers, linux_distributive)
    print(manager.name)

else:
    sys.exit(0)
