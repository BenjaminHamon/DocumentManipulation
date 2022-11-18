import setuptools


def run_setup():
	parameters = {
		"version": "1.0.0",
		"author": "Benjamin Hamon",

		"name": "bhamon-book-distribution-toolkit",
		"description": "Toolkit for creating book distributions",

		"packages": [
			"bhamon_book_distribution_toolkit",
		],

		"python_requires": "~= 3.7",

		"install_requires": [
			"lxml ~= 4.9.1",
			"python-dateutil ~= 2.8.2",
		]
	}

	setuptools.setup(**parameters)


run_setup()
