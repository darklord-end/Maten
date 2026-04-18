def get_platform():
    import platform
    return platform.system()

def get_version():
    import main
    return f"{main.Basic.version[0]}.{main.Basic.version[1]}.{main.Basic.version[2]}"