import subprocess
from V1.plotlydash.dashboard import init_dashboard
from run import app
import time

subprocess.run('python run.py &',shell=True)
time.sleep(10)
init_dashboard(app)
print('duude')
print([i for i in app.url_map.iter_rules()])