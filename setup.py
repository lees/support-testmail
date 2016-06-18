from setuptools import setup, find_packages

setup(
    name='django-support-testmail',
    version="1.0.1",
    description='Test project django app',
    author='Slava Ksenz',
    author_email='leesasp@gmail.com',
    url='https://github.com/lees/support-testmail',
    package_dir={'support': 'support'},
    packages=find_packages(exclude='test_app'),
)
