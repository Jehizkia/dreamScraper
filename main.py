from DreamCatcher import DreamCatcher
import database

url = 'http://indreams.me'
parameter = '/?sort=mostliked'

dreamcatcher = DreamCatcher(url, parameter)

dreamcatcher.convert_dreams_to_objects()

print('hey')
