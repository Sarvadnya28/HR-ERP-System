import importlib

packages = ['flask', 'flask_mysqldb', 'werkzeug']

for pkg in packages:
    try:
        importlib.import_module(pkg.replace('-', '_'))
        print(f"{pkg} is installed")
    except ImportError:
        print(f"{pkg} is NOT installed")
