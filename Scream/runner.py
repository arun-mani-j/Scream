import time
from typing import Callable, List


class Runner:
    def __init__(self, function: Callable, args: List[List]):

        self.function = function
        self.args = args

    def start(self):

        print("Starting execution ...")
        for i, (args, delay) in enumerate(self.args):
            time.sleep(delay)
            self.function(*args)
            print(f"Done {i+1} epoch.")
        print("Completed")
