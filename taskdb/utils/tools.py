import subprocess
import logging


LOG = logging.getLogger('taskdb')
LOG.setLevel(logging.INFO)

def run_cmd(cmd_str):
    '''Run cmdline with shell'''

    out_err = subprocess.Popen(cmd_str, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    res = []
    for val in out_err:
        res.append(val.decode().replace('\\n', '\n'))
    return res
