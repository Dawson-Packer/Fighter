import objects.objects as obj

class AnimationHandler:
    def __init__(self):
        self.s_tick = 0

    def animate_sprite(self, object: obj.Sprite, stage: str):
        if stage == "s": object.set_texture(stage, object.name, "0.png", object.width, object.height)
        if stage == "w": object.set_texture(stage, object.name, str(self.s_tick) + ".png", object.width, object.height)

    def animation_tick(self):
        self.s_tick += 1
        if self.s_tick == 4: self.s_tick = 0