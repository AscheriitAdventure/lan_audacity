import AppKit
from PyObjCTools import AppHelper

class AppDelegate(AppKit.NSObject):
    def applicationSupportsSecureRestorableState(self):
        return True

if __name__ == '__main__':
    app = AppKit.NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
