from setuptools import find_packages, setup

requirements = [x.strip() for x in open('requirements.txt')]
url = "https://"

setup(
    name='airflow_ml_dags',
    version='1.0.0',
    packages=find_packages(),
    url=url,
    license='',
    author='MarinaZav',
    author_email='',
    description='',
    install_requires=requirements
)