import os.path  # Для создания пути
import sys  # To find out the script name (in argv[0])


modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
print(modpath)
