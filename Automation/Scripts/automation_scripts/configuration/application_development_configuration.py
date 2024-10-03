import os
from typing import List

from bhamon_development_toolkit.applications.application_metadata import ApplicationMetadata

from automation_scripts.configuration.project_metadata import ProjectMetadata
from automation_scripts.configuration.python_development_configuration import PythonDevelopmentConfiguration
from automation_scripts.toolkit.applications.application_package_configuration import ApplicationPackageConfiguration


class ApplicationDevelopmentConfiguration:


    def __init__(self, python_package_identifier: str, package_configuration_collection: List[ApplicationPackageConfiguration]) -> None:
        self.python_package_identifier = python_package_identifier
        self.package_configuration_collection = package_configuration_collection


    def get_metadata(self, project_metadata: ProjectMetadata) -> ApplicationMetadata:
        return ApplicationMetadata(
            product_identifier = project_metadata.identifier,
            version_identifier = project_metadata.version.identifier,
            version_identifier_full = project_metadata.version.full_identifier,
            product_copyright = project_metadata.copyright_text,
        )


    def get_module_path(self, python_development_configuration: PythonDevelopmentConfiguration) -> str:
        application_python_package = python_development_configuration.get_package_by_identifier(self.python_package_identifier)
        return os.path.join(application_python_package.path_to_sources, application_python_package.name_for_file_system, "application.py")


    def get_package_configuration(self, identifier: str) -> ApplicationPackageConfiguration:
        configuration = next((x for x in self.package_configuration_collection if x.configuration_identifier == identifier), None)
        if configuration is None:
            raise KeyError("No application package configuration matching identifier '%s'" % identifier)
        return configuration
