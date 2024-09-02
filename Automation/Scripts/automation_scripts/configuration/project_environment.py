import os
import platform
import sys


class ProjectEnvironment:


    def get_python_executable(self) -> str:
        return sys.executable


    def get_python_system_executable(self) -> str:
        if platform.system() == "Windows":
            return os.path.join(sys.base_prefix, "python.exe")
        return os.path.join(sys.base_prefix, "python.exe")


    def get_python_package_repository_url(self, target_environment: str) -> str:
        if target_environment == "Development":
            return "https://nexus.benjaminhamon.com/repository/python-packages-development"
        if target_environment == "Production":
            return "https://nexus.benjaminhamon.com/repository/python-packages"

        raise ValueError("Unknown environment: '%s'" % target_environment)
