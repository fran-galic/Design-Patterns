import importlib

def myfactory(moduleName):
    modul = importlib.import_module(f"plugins.{moduleName}")
    return getattr(modul, moduleName)