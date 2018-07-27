import time

class WCAdapter(object):
    def __init__(self, adb, cv):
        self.adb = adb
        self.cv = cv

    def handleContact(self, contact_rect):
        x, y, w, h = contact_rect
        x = int(x + w/2)
        y = int(y + h/2)
        # print('contact_rect is %s, and will press:%d, %d' % (contact_rect, x, y))
        self.adb.press_xy(x, y) #enter the contact info
        self.adb.press_xy(560, 1470) #enter the chat interface
        time.sleep(1)
        self.adb.long_press(200, 2100, 2000) #long press text edit
        self.adb.press_xy(180, 1970) #press paste
        self.adb.press_xy(1000, 2070) #press send
        self.adb.press_back()
        self.adb.press_xy(400, 2060) #press contact list

    def start(self, contact_list):
        for contact_rect in contact_list:
            self.handleContact(contact_rect)

    def execute(self):
        self.adb.pull_screen()
        contact_list = self.cv.handle()
        print(contact_list)
        while len(contact_list):
            self.start(contact_list)
            self.adb.swipe(500, 1900, 500, 400)
            self.adb.pull_screen()
            contact_list = self.cv.handle()