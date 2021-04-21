import numpy as np

from lab5 import Lab5Renderer


class Lab6Renderer(Lab5Renderer):
    title = "Lab 6: Hierarchical Transformations"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render_scene(self, delta_time):
        """renders the scene
        TODO Place code here
        """
        self.push_model_matrix(np.eye(4))
        self.house.render(self.get_model_matrix(), color=np.array([255, 0, 0]))
        self.pop_model_matrix()


if __name__ == "__main__":
    Lab6Renderer.run()
