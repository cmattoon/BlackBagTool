from BlackBagTool.Apps.Chrome import Chrome
import os

def getChromeData():
    infile = ''
    outfile = ''

    while not os.path.exists(infile):
        infile = raw_input("Path to chrome folder (/home/user/.config/google-chrome/):")

    while not os.path.exists(outfile):
        outfile = raw_input("Enter path to output directory (must be created already):")
        # Of course, you could try to make the directory, but this is a heads-up for the demo

    c = Chrome(infile, outfile)

    raw_input("Press ENTER to dump Chrome's web history")
    for item in c.getWebHistory():
        print item.pretty()

    raw_input("Press ENTER to dump Chrome's Download History")
    for item in c.getDownloadHistory():
        print item.pretty()


if __name__ == "__main__":
    getChromeData()
    
