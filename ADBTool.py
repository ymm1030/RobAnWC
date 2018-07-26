import os, subprocess, sys, time

class ADBTool(object):
    def __init__(self):
        # if os.path.exists('screenshot.png'):
        #     os.remove('screenshot.png')
        self.adb_path = os.path.join(os.getcwd(), 'Tools/adb')

    def pull_screen(self, name='screenshot.png'):
        process = subprocess.Popen('{} shell screencap -p'.format(self.adb_path), shell=True, stdout=subprocess.PIPE)
        screenshot = process.stdout.read()
        if sys.platform == 'win32':
            screenshot = screenshot.replace(b'\r\n', b'\n')
        f = open(name, 'wb')
        f.write(screenshot)
        f.flush()
        f.close()

    def press_back(self):
        process = subprocess.Popen('{} shell input keyevent 4'.format(self.adb_path), shell=True)
        process.wait()

    def press_xy(self, x, y):
        process = subprocess.Popen('{} shell input tap {:d} {:d}'.format(self.adb_path, x, y), shell=True)
        process.wait()

if __name__ == '__main__':
    adt = ADBTool()
    adt.press_xy(500, 1250) #enter the contact info
    adt.press_xy(560, 1470) #enter the chat interface
    time.sleep(1) 
    adt.press_back()
    adt.press_xy(400, 2060) #back to contact list
    