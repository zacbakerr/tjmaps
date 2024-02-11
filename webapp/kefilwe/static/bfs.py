import cv2
import threading
import urllib.request as urllib
import numpy as np
from skimage import io
from django.templatetags.static import static


class Point(object):
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

mouse_click_status = 0
rw = 4
start = Point()
end = Point()
directions = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]

def bfs(s, e):
    global img, h, w

    found = False
    queue = []

    visited = [[0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]

    queue.append(s)
    visited[s.y][s.x] = 1

    while len(queue) > 0:
        p = queue.pop(0)
        for d in directions:
            cell = p + d
            if (0 <= cell.x < w and 0 <= cell.y < h and
            visited[cell.y][cell.x] == 0 and
                    (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):
                queue.append(cell)
                visited[cell.y][cell.x] = 1
                parent[cell.y][cell.x] = p
                if cell == e:
                    found = True
                    del queue[:]
                    break

    path = []
    if found:
        p = e

        while p != s:
            path.append(p)
            p = parent[p.y][p.x]

        path.append(p)
        path.reverse()

        for p in path:
            img[p.y+1][p.x+1] = [0, 0, 255]
            img[p.y][p.x] = [0, 0, 255]
            img[p.y-1][p.x-1] = [0, 0, 255]
            img[p.y+1][p.x-1] = [0, 0, 255]
            img[p.y-1][p.x+1] = [0, 0, 255]
            img[p.y][p.x+1] = [0, 0, 255]
            img[p.y][p.x-1] = [0, 0, 255]
            img[p.y+1][p.x] = [0, 0, 255]
            img[p.y-1][p.x] = [0, 0, 255]

def mouse_click(event, px, py, flag, params):

    global img, mouse_click_status, start, end, rw

    if event == cv2.EVENT_LBUTTONUP:
        if mouse_click_status == 0:
            cv2.rectangle(img, (px-rw, py-rw), (px+rw, py+rw), (0, 255, 255), -1)
            start = Point(px, py)
            mouse_click_status = mouse_click_status + 1

        elif mouse_click_status == 1:
            cv2.rectangle(img, (px-rw, py-rw), (px+rw, py+rw), (0, 255, 0), -1)
            end = Point(px, py)
            mouse_click_status = mouse_click_status + 1

def display():
    global img
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouse_click)
    while True:
        cv2.imshow("image", img)
        cv2.waitKey(1)
        if mouse_click_status == 2:
            break

def main():
  # img = io.imread('http://answers.opencv.org/upfiles/logo_2.png')
  # img = cv2.imdecode(img, -1) # 'Load it as it is'
  img = cv2.imread(static('kefilwe/maze.jpeg'))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  img = cv2.resize(img, (1080, 720), interpolation=cv2.INTER_NEAREST)

  _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

  img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

  h, w = img.shape[:2]

  t = threading.Thread(target=display, args=())
  t.daemon = True
  t.start()

  while mouse_click_status < 2:
      pass
  cv2.destroyAllWindows()

  bfs(start, end)
  cv2.imwrite("output.jpg", img)
  cv2.waitKey(0)

if __name__ == '__main__':
    import os
    print(os.listdir())
    main()