from djitellopy import tello
import pygame
import time
import numpy as np
import cv2
import turtle
#drone1.connect()

#drone1.get_speed_x()
#drone1.get_speed_z()
#drone1.get_speed_y()
class DJI:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.setup(400,400)
        self.window.bgcolor('black')
        self.window.title('Schematic')
        self.droneobject = turtle.Turtle()
        self.droneobject.shape('circle')
        self.droneobject.color('red')
        self.droneobject.goto(0,0)
        self.init_time = 0
        self.speedx = 0
        self.ct = 0
        self.speedfx = 0
        pygame.init()
        win = pygame.display.set_mode((400,400))
        self.drone = tello.Tello()
        self.drone.connect()
        self.drone.streamon()
        print("Battery : "+str(self.drone.get_battery()) + "%")

    def keyPressed(self,ascii):
        k = False
        for eve in pygame.event.get():pass
        keyboard = pygame.key.get_pressed()
        keypressed = getattr(pygame,'K_{}'.format(ascii))
        if keyboard[keypressed]:
            k = True
        return k
        pygame.display.update()
    def iteration(self):
        while True:
            self.speedfx = 0
            self.speedx = 0
            lr, fb, ud, a = 0, 0, 0, 0
            if self.keyPressed("f"):
                self.drone.takeoff()
                self.init_time = time.time()
            if self.keyPressed("LEFT"):
                self.speedx += float(-self.drone.get_speed_x())
                self.ct = time.time()
                lr = -99
                print("this is"+str(lr))
            self.init_time = time.time()
            if self.speedfx and self.ct and self.init_time != 0:
                cv2.putText(image, str(self.speedfx / (self.ct - self.init_time)), (200, 200), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 3)
            if self.keyPressed("RIGHT"):
                self.speedx += float(self.drone.get_speed_x())
                self.ct = time.time()
                lr=100-1
                print("this is"+str(lr))
            self.init_time = time.time()
            if self.speedfx and self.ct and self.init_time != 0:
                cv2.putText(image, str(self.speedfx / (self.ct - self.init_time)), (200, 200), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 3)
            if self.keyPressed("w"):
                self.speedfx += float(self.drone.get_speed_y())
                self.ct = time.time()
                fb = 90
            self.init_time = time.time()
            if self.speedfx and self.ct and self.init_time != 0:
                cv2.putText(image, str(self.speedfx / (self.ct - self.init_time)), (200, 200), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 3)
            if self.keyPressed("s"):
                self.speedfx += float(-self.drone.get_speed_y())
                self.ct = time.time()
                fb = -100
            self.init_time = time.time()
            if self.speedfx and self.ct and self.init_time != 0:
                cv2.putText(image, str(self.speedfx / (self.ct - self.init_time)), (200, 200), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 3)
            if self.keyPressed('e'):
                self.drone.land()
            if self.keyPressed("a"):
                a += -45
            if self.keyPressed("d"):
                a -= -45
            if self.keyPressed('r'):
                ud+= 40
            if self.keyPressed('t'):
                ud -= 40


            self.drone.send_rc_control(lr, fb, ud, a)
            image = self.drone.get_frame_read().frame
            image = cv2.resize(image, (400, 400))

            if self.speedfx != 0:
              self.droneobject.sety(float(self.droneobject.ycor()+float(self.speedfx / (self.ct - self.init_time))))

            cv2.imshow("Image", image)

            if self.keyPressed("i"):

                cv2.imwrite(f'Image'+str(time.time())+"image.jpg",image)
                time.sleep(2)

            if cv2.waitKey(1) == ord('q'):
                break
obj = DJI()
obj.iteration()
if __name__ == '__main__':
    DJI()
    while True:
        DJI().iteration()