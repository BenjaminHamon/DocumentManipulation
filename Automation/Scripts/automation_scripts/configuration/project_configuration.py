import os
from typing import List

from bhamon_development_toolkit.automation.project_version import ProjectVersion
from bhamon_development_toolkit.python.python_package import PythonPackage

from automation_scripts.toolkit.applications.application_metadata import ApplicationMetadata


class ProjectConfiguration:


    def __init__(self, # pylint: disable = too-many-arguments
            project_identifier: str,
            project_display_name: str,
            project_version: ProjectVersion,
            copyright_text: str,
            author: str,
            author_email: str,
            project_url: str) -> None:

        self.project_identifier = project_identifier
        self.project_display_name = project_display_name
        self.project_version = project_version

        self.copyright = copyright_text

        self.author = author
        self.author_email = author_email
        self.project_url = project_url


    def get_artifact_default_parameters(self) -> dict:
        return {
            "project": self.project_identifier,
            "version": self.project_version.identifier,
            "revision": self.project_version.revision_short,
        }


    def list_automation_packages(self) -> List[PythonPackage]:
        return [
            PythonPackage(
                identifier = "automation-scripts",
                path_to_sources = os.path.join("Automation", "Scripts"),
                path_to_tests = os.path.join("Automation", "Tests")),
        ]


    def list_python_packages(self) -> List[PythonPackage]:
        return [
            PythonPackage(
                identifier = "benjaminhamon-document-manipulation-application",
                path_to_sources = os.path.join("Sources", "application"),
                path_to_tests = os.path.join("Tests", "application")),

            PythonPackage(
                identifier = "benjaminhamon-document-manipulation-scripts",
                path_to_sources = os.path.join("Sources", "scripts"),
                path_to_tests = os.path.join("Tests", "scripts")),

            PythonPackage(
                identifier = "benjaminhamon-document-manipulation-toolkit",
                path_to_sources = os.path.join("Sources", "toolkit"),
                path_to_tests = os.path.join("Tests", "toolkit")),
        ]


    def get_application_metadata(self) -> ApplicationMetadata:
        return ApplicationMetadata(
            product_identifier = self.project_identifier,
            version_identifier = self.project_version.identifier,
            version_identifier_full = self.project_version.full_identifier,
            product_copyright = self.copyright,
        )


    def get_application_module_path(self) -> str:
        all_python_packages = self.list_python_packages()
        application_python_package = next(x for x in all_python_packages if x.identifier == "benjaminhamon-document-manipulation-application")
        return os.path.join(application_python_package.path_to_sources, application_python_package.name_for_file_system, "application.py")
