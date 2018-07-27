import cv2
import subprocess
import sys, os

class CVHandler(object):
    def __init__(self):
        self.TOP = 100
        self.BOTTOM = 130
        self.BANNER = 135
        self.CHECK_COLUMN = 1005
        self.CONTACT_COLOR = [255, 255, 255]
        self.CONTACT_HEIGHT = 155

        self.IGNORED_CONTACT = []
        self.IGNORED_CONTACT.append(cv2.imread('ignore/1.png'))
        self.IGNORED_CONTACT.append(cv2.imread('ignore/2.png'))
        self.IGNORED_CONTACT.append(cv2.imread('ignore/3.png'))
        self.IGNORED_CONTACT.append(cv2.imread('ignore/4.png'))
        self.IGNORED_CONTACT.append(cv2.imread('ignore/5.png'))
        self.IGNORED_CONTACT.append(cv2.imread('ignore/6.png'))

        self.last_10_contacts = []

    def isIgnored(self, img):
        for item in self.IGNORED_CONTACT:
            if item.shape != img.shape:
                continue
            if (img==item).all():
                return True
        return False

    def handle(self):
        if not os.path.exists('screenshot.png'):
            print("Can not get the screenshot!")
            exit(0)
        img = cv2.imread('screenshot.png')
        if img is None:
            print('Invalid screen capture!')
            exit(0)
        img = img[self.TOP:img.shape[0]-self.BOTTOM, 0:img.shape[1]]
        return self.splitImg(img)
    
    def splitImg(self, img):
        continues_colored = 0
        prevColor = [0, 0, 0]
        pendingAreas = []
        # count = 1
        for i in range(0, img.shape[0]):
            color = list(img[i, self.CHECK_COLUMN])
            if color != prevColor:
                # if continues_colored > 0:
                #     print("Get continues colord {} with height {}".format(prevColor, continues_colored))
                if prevColor == self.CONTACT_COLOR and continues_colored == self.CONTACT_HEIGHT:
                    contact = img[i-continues_colored:i, 0:self.CHECK_COLUMN]
                    # cv2.imwrite("split/%d.png" % count, contact)
                    # count += 1
                    if self.isIgnored(contact):
                        print("Ignore a system contact!")
                    elif self.isHandledContact(contact):
                        print("Ignore a handled contact!")
                    else:
                        rect = [0, self.TOP + i - continues_colored, contact.shape[1], contact.shape[0]]
                        print("Get a contact at {}!".format(rect))
                        pendingAreas.append(rect)
                        self.saveContact(contact)
                continues_colored = 1
            else:
                continues_colored += 1
            prevColor = color
        #last part is the bottom, just drop it.
        return pendingAreas

    def saveContact(self, contact):
        self.last_10_contacts.append(contact)
        if len(self.last_10_contacts) > 10:
            self.last_10_contacts = self.last_10_contacts[1:]

    def isHandledContact(self, contact):
        for c in self.last_10_contacts:
            if (contact==c).all():
                return True
        return False

# v = CVHandler()
# v.splitImg(v.pull_screen())

# for i in range(0, img.shape[0]):
#     img.itemset((i, 1006, 0), 255)
#     img.itemset((i, 1006, 1), 0)
#     img.itemset((i, 1006, 2), 255)
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()