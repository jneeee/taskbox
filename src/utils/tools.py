import subprocess


def run_cmd(cmd_str):
    res = {'cmd': cmd_str}
    out, err = subprocess.Popen(cmd_str, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    if out:
        res['out'] = out.decode().strip('\n').split('\n')
        err = None
    else:
        res['err'] = err.decode().strip('\n').split('\n')
        out = None
    return res
