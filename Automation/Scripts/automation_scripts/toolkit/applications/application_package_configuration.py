import dataclasses
from typing import List, Tuple


@dataclasses.dataclass()
class ApplicationPackageConfiguration:
    configuration_identifier: str
    target_operating_system: str
    target_application_environment: str
    files_to_include: List[Tuple[str,str]]
