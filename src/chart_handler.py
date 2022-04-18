import random


class ChartHandler:
    def __init__(self):
        self.color = None
        self.color_map = dict()
        self.colors = [
            'rgb(255, 173, 173)',
            'rgb(255, 214, 165)',
            'rgb(253, 255, 182)',
            'rgb(202, 255, 191)',
            'rgb(155, 246, 255)',
            'rgb(160, 196, 255)',
            'rgb(189, 178, 255)',
            'rgb(255, 198, 255)',
        ]

    def map_employees(self, employees):
        for employee in employees:
            if employee not in self.color_map.keys():
                color = random.choice(self.colors)
                self.colors.remove(color)
                self.color_map[employee] = color

    def get_color(self, employee):
        return self.color_map[employee]

    

    def generate_random_color(self):
        color = random.choice(self.colors)
        self.colors.remove(color)
        self.color = color
        return self.color

    def reset_colors(self):
        self.color_map.clear()
        self.colors = [
            'rgb(255, 173, 173)',
            'rgb(255, 214, 165)',
            'rgb(253, 255, 182)',
            'rgb(202, 255, 191)',
            'rgb(155, 246, 255)',
            'rgb(160, 196, 255)',
            'rgb(189, 178, 255)',
            'rgb(255, 198, 255)',
        ]
