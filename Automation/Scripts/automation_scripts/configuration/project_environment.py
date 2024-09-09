import sys


class ProjectEnvironment:


    def get_python_executable(self) -> str:
        return sys.executable


    def get_python_system_executable(self) -> str:
        if hasattr(sys, "_base_executable"):
            return sys._base_executable # type: ignore # pylint: disable = protected-access
        raise RuntimeError("Unable to resolve the system Python executable")


    def get_application_package_repository_url(self) -> str:
        return "https://nexus.benjaminhamon.com/repository/application"


    def get_python_package_repository_url(self, target_environment: str) -> str:
        if target_environment == "Development":
            return "https://nexus.benjaminhamon.com/repository/python-packages-development"
        if target_environment == "Production":
            return "https://nexus.benjaminhamon.com/repository/python-packages"

        raise ValueError("Unknown environment: '%s'" % target_environment)
