import pygame
import numpy as np
import subprocess
import threading
from time import sleep
import json

pick = None
mouseButtonDownLeft = False
mouseMoved = False


def loadSettings():
    with open('settings.json') as settingsfile:
        return json.load(settingsfile)


settings = loadSettings()
_edition = settings['insider']['edition']
_iconResolution = 64 if settings['insider']['allow64pxIcon'] else 32
_width = settings['WindowSize']['width']
_height = settings['WindowSize']['height']
_project = "unbenannt"
icon = pygame.image.load(f'icon {_iconResolution}px.png')


class QuickAccessBar(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None

    def run(self):
        self.process = subprocess.Popen(
            ['py', 'QuickAccessBar.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


QAB = None


def openQuickAccessBar():
    global QAB
    QAB = QuickAccessBar()
    QAB.start()


class main():  # threading.Thread):
    def __init__(self):
        # threading.Thread.__init__(self)
        pygame.init()
        self.mousePos = np.array([0, 0])
        self.width = _width
        self.height = _height
        self.paintResolution = np.array([60, 40])
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption(f'{_project} - MS Paint {_edition} edition')
        pygame.display.set_icon(icon)
        openQuickAccessBar()

    def run(self):
        global mouseButtonDownLeft, QAB
        while True:
            mouseMoved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QAB.process.kill()
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEMOTION:
                    self.mousePos = np.array(event.pos)
                    mouseMoved = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.button)
                    mouseButtonDownLeft = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouseButtonDownLeft = False

            # for x in np.arange(self.paintResolution[0]):
            #     pygame.draw.line(self.screen, (0, 0, 0), (self.width / self.paintResolution[0] * x, 0), (self.width / self.paintResolution[0] * x, self.height), 1)

            # for y in np.arange(self.paintResolution[1]):
            #     pygame.draw.line(self.screen, (0, 0, 0), (0, self.height / self.paintResolution[1] * y), (self.width, self.height / self.paintResolution[1] * y), 1)
            if mouseMoved and mouseButtonDownLeft:
                pygame.draw.rect(self.screen, (255, 0, 50), (int(self.mousePos[0] / (self.width / self.paintResolution[0])) * self.width / self.paintResolution[0], int(
                    self.mousePos[1] / (self.height / self.paintResolution[1])) * self.height / self.paintResolution[1], 10, 10))
            pygame.display.flip()


if __name__ == "__main__":
    mainprocess = main()
    mainprocess.run()
