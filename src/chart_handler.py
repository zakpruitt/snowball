import random

class ChartHandler:
    def __init__(self):
        self.color = None

    def generate_random_color(self):
        self.color = 'rgb(' + str(random.randint(0, 255)) + ', ' + str(random.randint(0, 255)) + ', ' + str(random.randint(0, 255)) + ')'
        return self.color
