import pygame
import os

class SpeechBubble:
    def __init__(self):
        self.image = None
        self.font = pygame.font.SysFont("monospace", 18)
        self.message = ""
        self.position = (200, 160)  # adjust as needed based on dealer location

        try:
            path = os.path.join("assets", "images", "blackjack", "speech_bubble.png")
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (200, 120))  # adjust size as needed
        except Exception as e:
            print("Failed to load speech bubble image:", e)

    def say(self, message):
        self.message = message

    def update(self, dt):
        pass  # No longer needed for always-visible mode

    def draw(self, screen):
        x, y = self.position

        if self.image:
            screen.blit(self.image, (x, y))

        # Adjust for real usable space inside the image (due to transparent padding)
        usable_width = 160  # fits visually within the actual text area
        text_padding_x = 20
        text_padding_y = 40
        line_height = 22

        lines = self.wrap_text(self.message, self.font, usable_width)

        # Optional: center vertically if few lines
        total_height = line_height * len(lines)
        start_y = y + text_padding_y

        for i, line in enumerate(lines):
            text = self.font.render(line, True, (0, 0, 0))
            screen.blit(text, (x + text_padding_x, start_y + i * line_height))

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
