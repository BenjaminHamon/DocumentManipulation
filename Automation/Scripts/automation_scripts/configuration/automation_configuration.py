from bhamon_development_toolkit.python.python_package import PythonPackage

from automation_scripts.configuration.application_development_configuration import ApplicationDevelopmentConfiguration
from automation_scripts.configuration.project_metadata import ProjectMetadata
from automation_scripts.configuration.python_development_configuration import PythonDevelopmentConfiguration
from automation_scripts.configuration.workspace_environment import WorkspaceEnvironment


class AutomationConfiguration:


    def __init__(self, # pylint: disable = too-many-arguments
            project_metadata: ProjectMetadata,
            python_development_configuration: PythonDevelopmentConfiguration,
            application_development_configuration: ApplicationDevelopmentConfiguration,
            workspace_environment: WorkspaceEnvironment,
            automation_python_package: PythonPackage) -> None:

        self.project_metadata = project_metadata
        self.python_development_configuration = python_development_configuration
        self.application_development_configuration = application_development_configuration
        self.workspace_environment = workspace_environment
        self.automation_python_package = automation_python_package


    def get_artifact_default_parameters(self) -> dict:
        return {
            "project": self.project_metadata.identifier,
            "version": self.project_metadata.version.identifier,
            "revision": self.project_metadata.version.revision_short,
        }
