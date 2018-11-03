# passage
#
# 8--------9
# |        |
# |        |
# 4--5--6--7
# |        |
# 0--1--2--3
#

# passage secret
#
#   ________
#  /        \
# | 8--------9
# | |\      /|
#  \| \    / |
#   4--5--6--7
#   |  |  |  |\
#   0--1--2--3 |
#       \______/
#


class Board():
    path = [{1, 4}, {0, 2}, {1, 3}, {2, 7}, {0, 5, 8}, {4, 6}, {5, 7}, {3, 6, 9}, {4, 9}, {7, 8}]
    path_pink = [{1, 4}, {0, 2, 5, 7}, {1, 3, 6}, {2, 7}, {0, 5, 8, 9}, {4, 6, 1, 8}, {5, 7, 2, 9}, {3, 6, 9, 1},
                {4, 9, 5}, {7, 8, 4, 6}]
    lock = None

    def getLinkForRoom(self, room, pink=False):
        if self.lock is None or self.lock[0] is not room:
            return self.path[room] if pink is False else self.path_pink[room]
        tmp = self.path if pink is False else self.path_pink
        tmp[self.lock[0]].remove(self.lock[1])
        return tmp[room]

    def lockPath(self, origin, next_room):
        self.lock = [origin, next_room]

