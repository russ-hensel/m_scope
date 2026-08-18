#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 14:11:36 2025

@author: russ with chat help
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof

import heapq

class TopTracker():
    def __init__(self, max_items):
        """ """
        self.reset( max_items )


    def reset( self,   max_items ):
        """ """
        self.max_items = max_items
        self.max_list = []



    def push_next(self, *, ix, size):
        """ """
        heapq.heappush(self.max_list, (size, ix))
        if len(self.max_list) > self.max_items:
            heapq.heappop(self.max_list)  # removes smallest size

    def get_result(self):
        result = [(index, length) for length, index in self.max_list]
        result.sort(key=lambda x: (-x[1], x[0]))  # descending by size
        return result


def test_1(   ):

    # ---- test
    lines = [
        "a short line",
        "a loooooo ",
        "123456789012345678901234",
        "a loo ooo line",
        "12345678901234567890123456",
        "a loo ooooooooo line",
        "12345678901234567890",
        "a loooooooooooooooo line",
        "a loooooooooooooooo line",
    ]

    print("start")
    a_tracker = TopTracker(5)
    for ix, i_line in enumerate(lines):
        size = len(i_line)
        a_tracker.push_next(ix=ix, size=size)

    result = a_tracker.get_result()
    print(result)
    print()
    for i_result in result:
        print( i_result )

if __name__ == "__main__":
    #----- run the full app
    test_1()

# --------------------
