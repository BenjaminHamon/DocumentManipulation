from benjaminhamon_document_manipulation_toolkit.serialization.json_serializer import JsonSerializer
from benjaminhamon_document_manipulation_toolkit.serialization.serializer import Serializer
from benjaminhamon_document_manipulation_toolkit.serialization.yaml_serializer import YamlSerializer


def create_serializer(serialization_type: str) -> Serializer:
    if serialization_type == "json":
        return JsonSerializer()
    if serialization_type == "yaml":
        return YamlSerializer()

    raise ValueError("Unknown serialization type: '%s'" % serialization_type)
