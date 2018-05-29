from setuptools import setup, find_packages

setup(
    name = 'test_service',
    url = 'none',
    version = '0.0.1',
    description = 'Test proxy',
    author = 'Zoe McCormick',
    author_email = 'zoe.mccormick@deciphernow.com',
    keyworks = ['NLP', 'microservice'],
    classifiers = ['Programming Language :: Python',
                   'Development Status :: 1 - Planning'],
    packages = find_packages(),
    include_package_data=True,
    install_requires = ['flask'],
    entry_points = {'console_scripts': ['test-start=test_service.server.app:launch_server']},
    )