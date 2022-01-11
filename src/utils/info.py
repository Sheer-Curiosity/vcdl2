def versionInfo():
	return (f"[DEBUG]: Current Version: {read_version()}\n")

def generalInfo():
	return('''
[INFO]: Written By: Sheer Curiosity
[INFO]: Tested By: Sheer Curiosity, Chimatta
	''')

def read_version():
    exec(compile(open('src/version.py').read(), 'src/version.py', 'exec'))
    return locals()['__version__']
