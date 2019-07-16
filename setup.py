from setuptools import find_packages, setup
setup(
    name='telly-test',
    version='0.0.1',
    # Include all the python modules except `tests`.
    packages=find_packages(exclude=['tests']),
    description='Customizing test',
    long_description='A long description of my custom package tested with tox',
    install_requires=[
        'Django>=2.1.4',
        'djangorestframework>=3.9.4',
        # Additional requirements, or
        # parse the requirements file and add it here
    ],
    classifiers=[
        'Programming Language :: Python',
    ],
    # entry_points={
    #     'pytest11': [
    #      'tox_tested_package =
    # tox_tested_package.fixtures'
    #     ]
    # },
)
