from Apps.Chrome import Chrome
import os, getpass

def getChromeData():
    infile = "/home/%s/.config/google-chrome/" % getpass.getuser()
    outfile = ''

    while not os.path.exists(infile):
        infile = raw_input("Path to chrome folder (/home/user/.config/google-chrome/):")

    while not os.path.exists(outfile):
        outfile = raw_input("Enter path to output directory (must be created already):")
        # Of course, you could try to make the directory, but this is a heads-up for the demo

    c = Chrome(infile, outfile)
    reportdata = ''
    raw_input("Press ENTER to dump Chrome's web history")
    for item in c.getWebHistory():
        i = item.pretty()
        reportdata += "%s\n" % i
        print i

    raw_input("Press ENTER to dump Chrome's Download History")
    for item in c.getDownloadHistory():
        i = item.pretty()
        reportdata += "%s\n" % i
        print i

    try:
        with open(outfile, 'wb') as f:
            lines = []
            for line in reportdata.split("\n"):
                lines.append(line)
            f.writelines(lines)
    except IOError:
        print "Can't write to %s" % outfile

if __name__ == "__main__":
    getChromeData()
    
