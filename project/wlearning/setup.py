 from setuptools import setup

 setup(
    name='test_module',
    version='0.1',
    description='Machine learning project module',
    author='Sergio Villamarin',
    author_email='svillamaringomez@tulane.edu',
    packages=['wlearning'], 
    install_requires=['numpy', 'scipy', 'sklearn'], # external packages as dependencies
  )