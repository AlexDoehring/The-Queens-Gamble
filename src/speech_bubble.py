import pygame
import os

class SpeechBubble:
    def __init__(self):
        self.image = None
        self.font = pygame.font.SysFont("monospace", 18)
        self.message = ""
        self.visible = False
        self.timer = 0  # Time left to show the message (ms)
        self.duration = 3000  # default display duration in ms
        self.position = (370, 40)  # adjust as needed based on dealer location

        try:
            path = os.path.join("assets", "images", "blackjack", "speech_bubble.png")
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (300, 150))
        except Exception as e:
            print("Failed to load speech bubble image:", e)

    def say(self, message, duration=None):
        self.message = message
        self.visible = True
        self.timer = duration if duration else self.duration

    def update(self, dt):
        if self.visible:
            self.timer -= dt
            if self.timer <= 0:
                self.visible = False

    def draw(self, screen):
        if self.visible and self.image:
            x, y = self.position
            screen.blit(self.image, (x, y))

            lines = self.wrap_text(self.message, self.font, 260)
            for i, line in enumerate(lines):
                text = self.font.render(line, True, (0, 0, 0))
                screen.blit(text, (x + 20, y + 20 + i * 22))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines
