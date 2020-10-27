from setuptools import setup, find_packages

setup(name='PyMOFScreen',
      description='Python code to do high-throughput DFT of MOFs with VASP',
      author='Andrew S. Rosen',
      author_email='rosen@u.northwestern.edu',
      url='https://github.com/arosen93/mof_screen',
      requires_python='>=3.6.0',
      version='1.1',
      packages=find_packages(),
      license='MIT'
     )
