from gl_base import Renderer
import numpy as np
import moderngl as gl


class Lab5Renderer(Renderer):
    title = "Lab 5: 3D Rendering (OpenGL)"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modeState = "p"
        self.xpos = 0
        self.ypos = 0
        self.zpos = -20
        self.angle = 0

        
    def poll_keys(self):
        """Handles key press events
        TODO: insert key press event code here:
        a: move left
        d: move right
        s: move back
        w: move forward
        q: turn left
        e: turn right
        r: move up
        f: move down
        p: change to perspective mode
        o: change to orthographic mode
        h: return "home"
        """
        if self.key_pressed[self.keys.P]:
            self.modeState = "p"

        if self.key_pressed[self.keys.O]:
            self.modeState = "o"   

        if self.key_pressed[self.keys.Q]:
            self.angle += 1 

        if self.key_pressed[self.keys.E]:
            self.angle -= 1 

        if self.key_pressed[self.keys.D]:
            self.xpos += np.cos(np.radians(self.angle)) 
            self.zpos += np.sin(np.radians(self.angle)) 

        if self.key_pressed[self.keys.A]:
            self.xpos -= np.cos(np.radians(self.angle)) 
            self.zpos -= np.sin(np.radians(self.angle))

        if self.key_pressed[self.keys.S]:
            self.xpos -= -np.sin(np.radians(self.angle)) 
            self.zpos -= np.cos(np.radians(self.angle)) 

        if self.key_pressed[self.keys.W]:
            self.xpos += -np.sin(np.radians(self.angle)) 
            self.zpos += np.cos(np.radians(self.angle)) 

        if self.key_pressed[self.keys.R]:
            self.ypos += 1

        if self.key_pressed[self.keys.F]:
            self.ypos -= 1
        
        if self.key_pressed[self.keys.H]:
            self.xpos = 0
            self.ypos = 0
            self.zpos = -20
            self.angle = 0
        

    def get_projection(self):
        """gets the projection matrix
        TODO: if in p state, returns perspective matrix
        TODO: if in o state, returns orthographic matrix
        
        """
        if self.modeState == "p":
            return np.transpose(np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 1, 0]]))
        elif self.modeState == "o":
            return np.transpose(np.array([[.1, 0, 0, 0],[0, .1, 0, 0],[0, 0, 0, 0],[0, 0, 0, 1]]))
        # return self.house

    def get_view(self):
        """gets the view matrix
        TODO: return the view matrix
        """
        translationM = np.transpose(np.array([[1, 0, 0, -self.xpos],[0, 1, 0, -self.ypos],[0, 0, 1, -self.zpos],[0, 0, 0, 1]]))
        rotationM = np.transpose(np.array([[np.cos(np.radians(self.angle)), 0, np.sin(np.radians(self.angle)), 0],
        [0, 1, 0, 0],
        [-np.sin(np.radians(self.angle)), 0, np.cos(np.radians(self.angle)), 0],
        [0, 0, 0, 1]]))

        return np.matmul(translationM, rotationM)


if __name__ == "__main__":
    Lab5Renderer.run()
