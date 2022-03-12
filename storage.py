import os
import sys
# user pour prendre le nom de l'utilisateur
user = sys.argv[1]

os.system("du -s /home/" + user +" | cut -d '/' -f 1")
