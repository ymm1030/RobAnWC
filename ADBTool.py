import os, subprocess, sys

class ADBTool(object):
    def __init__(self):
        if os.path.exists('screenshot.png'):
            os.remove('screenshot.png')
        pass

    def pull_screen(self):
        path = os.path.join(os.getcwd(), 'Tools/adb')
        process = subprocess.Popen('{} shell screencap -p'.format(path), shell=True, stdout=subprocess.PIPE)
        screenshot = process.stdout.read()
        if sys.platform == 'win32':
            screenshot = screenshot.replace(b'\r\n', b'\n')
        f = open('screenshot.png', 'wb')
        f.write(screenshot)
        f.flush()
        f.close()