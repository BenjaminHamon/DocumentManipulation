# cspell:words filevers prodvers pyinstaller

""" Unit tests for PyInstallerRunner """

import mockito

from bhamon_development_toolkit.processes.process_runner import ProcessRunner

from automation_scripts.toolkit.applications.application_metadata import ApplicationMetadata
from automation_scripts.toolkit.python.pyinstaller_runner import PyInstallerRunner


def test_generate_windows_version_info():
    process_runner = mockito.mock(spec = ProcessRunner)
    pyinstaller_runner = PyInstallerRunner(process_runner, "DoesNotExist") # type: ignore

    application_metadata = ApplicationMetadata(
        product_identifier = "Some Product",
        version_identifier = "1.2.3",
        version_identifier_full = "1.2.3+abcde",
        product_copyright = "Copyright (c) 2020 Some Copyright Holder",
    )

    expected = """
VSVersionInfo(
    ffi = FixedFileInfo(
        filevers = (1, 2, 3, 0),
        prodvers = (1, 2, 3, 0),
    ),
    kids = [
        StringFileInfo([
            StringTable(
                "040904B0",
                [
                    StringStruct("ProductName", "Some Product"),
                    StringStruct("ProductVersion", "1.2.3+abcde"),
                    StringStruct("FileVersion", "1.2.3"),
                    StringStruct("LegalCopyright", "Copyright (c) 2020 Some Copyright Holder"),
                ])
        ]),
		VarFileInfo([VarStruct("Translation", [1033, 1200])])
    ]
)
"""

    expected = expected.lstrip()

    actual = pyinstaller_runner.generate_windows_version_info(application_metadata)

    assert actual == expected
