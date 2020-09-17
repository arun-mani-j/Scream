import sys
sys.path.insert(0, "..")
import Scream

def main():
    app = Scream.application.Application()
    ret = app.run(sys.argv)
    exit(ret)
