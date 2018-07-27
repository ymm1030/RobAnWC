from CVHandler import CVHandler
from ADBTool import ADBTool
from WCAdapter import WCAdapter

adb = ADBTool()
cv = CVHandler()
wc = WCAdapter(adb, cv)
wc.execute()