from pg_base import PGRenderer
import pygame
import numpy as np

def translate(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

def rotatey(theta):
    rad = np.radians(theta)
    return np.array([
        [np.cos(rad), 0, np.sin(rad), 0],
        [0, 1, 0, 0],
        [-np.sin(rad), 0, np.cos(rad), 0],
        [0, 0, 0, 1]
    ])

def rotatez(theta):
    rad = np.radians(theta)
    return np.array([
        [np.cos(rad), np.sin(rad), 0, 0],
        [-np.sin(rad), np.cos(rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def model_transform(dx, dy, dz, theta, isZ=False):
    if isZ:
        return np.matmul(translate(dx, dy, dz), rotatez(theta))
    return np.matmul(translate(dx, dy, dz), rotatey(theta))

class Lab7Renderer(PGRenderer):
    title = "Lab 7: Graphics Implementation"
    def __init__(self):
        super().__init__()
        w, h = self.size
        self.to_screen = np.array ([
            [w/2, 0 , w/2],
            [0, -h/2, h/2],
            [0, 0, 1]
        ])

        self.xpos = 0
        self.ypos = 5
        self.zpos = -20
        self.angle = 0

        self.carx = -10
        self.tireAngle = 0


        self.house = [(np.array([pt.start.x, pt.start.y, pt.start.z, 1]),
         np.array([pt.end.x, pt.end.y, pt.end.z, 1])) for pt in self.house]
        self.tire = [(np.array([pt.start.x, pt.start.y, pt.start.z, 1]),
         np.array([pt.end.x, pt.end.y, pt.end.z, 1])) for pt in self.tire]
        self.car = [(np.array([pt.start.x, pt.start.y, pt.start.z, 1]),
         np.array([pt.end.x, pt.end.y, pt.end.z, 1])) for pt in self.car]

    def get_view(self):
        translationM = np.array([[1, 0, 0, -self.xpos],[0, 1, 0, -self.ypos],[0, 0, 1, -self.zpos],[0, 0, 0, 1]])
        rotationM = np.array([[np.cos(np.radians(self.angle)), 0, np.sin(np.radians(self.angle)), 0],
        [0, 1, 0, 0],
        [-np.sin(np.radians(self.angle)), 0, np.cos(np.radians(self.angle)), 0],
        [0, 0, 0, 1]])

        return np.matmul(rotationM, translationM)
    
    def render_object(self, screen, obj, model, pv, color):
        for start, end in obj:
            clip_start = np.matmul(np.matmul(pv, model), start)
            clip_end = np.matmul(np.matmul(pv, model), end)

            x, y, z, w = clip_start
            if x < -w or x > w:
                continue
            if y < -w or y > w:
                continue
            if z < -w or z > w:
                continue

            clip_start = clip_start / w

            x, y, z, w = clip_end
            if x < -w or x > w:
                continue
            if y < -w or y > w:
                continue
            if z < -w or z > w:
                continue
            
            clip_end = clip_end / w

            temps = np.array([clip_start[0], clip_start[1], clip_start[3]])
            tempe = np.array([clip_end[0], clip_end[1], clip_end[3]])

            screen_start = np.matmul(self.to_screen, temps)
            screen_end = np.matmul(self.to_screen, tempe)

            pygame.draw.line(screen, color, (screen_start[0],screen_start[1]),
             (screen_end[0], screen_end[1]))

    def render(self, screen):
        projection_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
        ])
        view_matrix = self.get_view()
        pv = np.matmul(projection_matrix, view_matrix)

        car_matrix = model_transform(self.carx,.5,-10,0)
        tire1 = np.matmul(car_matrix, model_transform(-1.75, 0, 1.5, self.tireAngle, True))
        tire2 = np.matmul(car_matrix, model_transform(1.75, 0, 1.5, self.tireAngle, True))
        tire3 = np.matmul(car_matrix, model_transform(1.75, 0, -1.5, self.tireAngle, True))
        tire4 = np.matmul(car_matrix, model_transform(-1.75, 0, -1.5, self.tireAngle, True))
        self.render_object(screen, self.car, car_matrix, pv, self.GREEN)
        self.render_object(screen, self.tire, tire1, pv, self.BLUE)
        self.render_object(screen, self.tire, tire2, pv, self.BLUE)
        self.render_object(screen, self.tire, tire3, pv, self.BLUE)
        self.render_object(screen, self.tire, tire4, pv, self.BLUE)
        self.render_object(screen, self.house, model_transform(0,0,0,180), pv, self.RED) 
        self.render_object(screen, self.house, model_transform(20,0,0,180), pv, self.RED)
        self.render_object(screen, self.house, model_transform(-20,0,0,180), pv, self.RED)
        self.render_object(screen, self.house, model_transform(-40,0,-20,90), pv, self.RED)
        self.render_object(screen, self.house, model_transform(0,0,-40,0), pv, self.RED) 
        self.render_object(screen, self.house, model_transform(20,0,-40,0), pv, self.RED)
        self.render_object(screen, self.house, model_transform(-20,0,-40,0), pv, self.RED)
        self.carx += 0.1
        self.tireAngle += 2

    def poll_keys(self):  
        if self.key_pressed[pygame.K_q]:
            self.angle += 1 

        if self.key_pressed[pygame.K_e]:
            self.angle -= 1 

        if self.key_pressed[pygame.K_d]:
            self.xpos += np.cos(np.radians(self.angle)) 
            self.zpos += np.sin(np.radians(self.angle)) 

        if self.key_pressed[pygame.K_a]:
            self.xpos -= np.cos(np.radians(self.angle)) 
            self.zpos -= np.sin(np.radians(self.angle))

        if self.key_pressed[pygame.K_s]:
            self.xpos -= -np.sin(np.radians(self.angle)) 
            self.zpos -= np.cos(np.radians(self.angle)) 

        if self.key_pressed[pygame.K_w]:
            self.xpos += -np.sin(np.radians(self.angle)) 
            self.zpos += np.cos(np.radians(self.angle)) 

        if self.key_pressed[pygame.K_r]:
            self.ypos += 1

        if self.key_pressed[pygame.K_f]:
            self.ypos -= 1
        
        if self.key_pressed[pygame.K_h]:
            self.xpos = 0
            self.ypos = 5
            self.zpos = -20
            self.angle = 0
            self.carx = -10
            self.tireAngle = 0

if __name__ == "__main__":
    Lab7Renderer.run()
