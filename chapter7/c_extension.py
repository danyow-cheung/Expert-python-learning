from distutils.core import setup,Extension
module1 = Extension(
    'demo',sources=['demo.c']
)

setup(
    name = "Package_name",
    version = '1.0',
    description= ' This is a demo package',
    ext_modules=[module1]
)
'''
一旦以這種方式準備好，您的分發流程中還需要一個額外的步驟：
python setup.py build 
'''
