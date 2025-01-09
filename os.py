import platform


os_name = platform.system()


os_version = platform.version()


architecture = platform.architecture()

print("Operating System:", os_name)
print("Operating System Version:", os_version)
print("Platform Architecture:", architecture)
