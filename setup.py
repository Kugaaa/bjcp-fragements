from setuptools import setup

setup(
    name='service-fragments-set',
    version='0.0.1',
    py_modules=['service-fragments'],
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bjcp=bjcp.main:cli
    ''',
)
