from config import *
import random
import math


class Entity(pygame.sprite.Sprite):
    def __init__(self, game, x, y, layer, sheet, sheet_pos):
        super().__init__()
        self.scale = TILE_SIZE  # DELETE SCALER

        """ Get our main game, and setup the layer"""
        self.game = game
        self.layer = layer

        """ Add it to all sprites group """
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        """ Set up the size and pos"""
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = CROP_SIZE
        self.height = CROP_SIZE

        """ Set the sprite sheet"""
        self.sheet = sheet

        """ Get image from sheet, set up the cords for rect"""
        self.image = self.sheet.get_image(sheet_pos[0], sheet_pos[1], self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))  # DELETE SCALER
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


class Player(Entity):
    def __init__(self, game, x, y):
        sprite_sheet = game.player_sprite_sheet  # What sheet to use
        sprite_sheet_pos = (0, 64)  # Crop cords
        super().__init__(game, x, y, PLAYER_LAYER, sprite_sheet, sprite_sheet_pos)  # Construct the player
        self.direction = "RIGHT"  # Start direction
        self.x_change = 0  # Start change x
        self.y_change = 0  # Start change y

        self.frame_index = 0  # Track the current frame
        self.animation_speed = 0.1  # Speed of the animation
        self.frame_timer = 0  # Timer to track time for frame switching
        self.create_frame_lists()

        self.scale = 100



        # Making the sprite little bigger bc of small image

    def update(self):
        self.move()
        self.update_movement()
        self.animate()

    def update_movement(self):
        # CHANGE THE SPRITES POS BASED ON CHANGE
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        # to not accelerate set back the change to 0 every frame
        self.x_change = 0
        self.y_change = 0

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.x_change = self.x_change - PLAYER_STEPS
            self.direction = "LEFT"
        elif pressed[pygame.K_d]:
            self.x_change = self.x_change + PLAYER_STEPS
            self.direction = "RIGHT"
        elif pressed[pygame.K_w]:
            self.y_change = self.y_change - PLAYER_STEPS
            self.direction = "UPP"
        elif pressed[pygame.K_s]:
            self.y_change = self.y_change + PLAYER_STEPS
            self.direction = "DOWN"

    def create_frame_lists(self):
        self.right_frames = []
        self.left_frames = []
        self.right_idle_frames = []
        self.left_idle_frames = []
        for frame in range(0, 5):
            self.right_frames.append(self.game.player_sprite_sheet.get_image(0 + (CROP_SIZE * frame), 0, self.width, self.height))
            self.left_frames.append(self.game.player_sprite_sheet.get_image(0 + (CROP_SIZE * frame), 32, self.width, self.height))

        for frame in range(0, 1):
            self.right_idle_frames.append(self.game.player_sprite_sheet.get_image(0 + (CROP_SIZE * frame), 64, self.width, self.height))
            self.left_idle_frames.append(self.game.player_sprite_sheet.get_image(64 + (CROP_SIZE * frame), 64, self.width, self.height))

    def animate(self):
        # Handle frame updates for right and left movement
        frames = self.right_frames if self.direction == "RIGHT" else self.left_frames
        idle_frames = self.right_idle_frames if self.direction == "RIGHT" else self.left_idle_frames

        # Idle animation
        if self.x_change == 0 and self.y_change == 0:
            self.image = idle_frames[0]
        else:
            # Frame animation based on movement
            self.frame_timer += self.animation_speed
            if self.frame_timer >= 1:
                self.frame_index = (self.frame_index + 1) % len(frames)
                self.frame_timer = 0

            frames[self.frame_index]


class Block(Entity):
    def __init__(self, game, x, y):
        sprite_sheet = game.stone_sprite_sheet  # What sheet to use
        sprite_sheet_pos = (96, 96)  # Crop cords
        super().__init__(game, x, y, BLOCKS_LAYER, sprite_sheet, sprite_sheet_pos)  # Construct the block
        """ """


class Ground(Entity):
    def __init__(self, game, x, y):
        sprite_sheet = game.terrain_sprite_sheet  # What sheet to use
        sprite_sheet_pos = (32, 64)  # Crop cords
        super().__init__(game, x, y, GROUND_LAYER, sprite_sheet, sprite_sheet_pos)  # Construct the block


class Enemy(Entity):
    def __init__(self, game, x, y):
        sprite_sheet = game.enemy_sprite_sheet  # What sheet to use
        sprite_sheet_pos = (32, 64)  # Crop cords
        super().__init__(game, x, y, ENEMY_LAYER, sprite_sheet, sprite_sheet_pos)  # Construct the
        self.directions = ["LEFT", "RIGHT", "DOWN", "UPP"]
        self.direction = random.choice(self.directions)
        self.x_change = 0  # Start change x
        self.y_change = 0  # Start change y

        self.max_steps = 30
        self.stall_steps = 80
        self.current_steps = 0

        self.state = "moving"

    def move(self):
        if self.state == "moving":

            if self.direction == "LEFT":
                self.x_change = self.x_change - ENEMY_STEPS
                self.current_steps += 1
            elif self.direction == "RIGHT":
                self.x_change = self.x_change + ENEMY_STEPS
                self.current_steps += 1
            elif self.direction == "UPP":
                self.y_change = self.y_change - ENEMY_STEPS
                self.current_steps += 1
            elif self.direction == "DOWN":
                self.y_change = self.y_change + ENEMY_STEPS
                self.current_steps += 1

        elif self.state == "stalling":

            self.current_steps += 1
            if self.current_steps == self.stall_steps:
                self.state = "moving"
                self.current_steps = 0

    def update_movement(self):
        # CHANGE THE SPRITES POS BASED ON CHANGE
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        # to not accelerate set back the change to 0 every frame
        self.x_change = 0
        self.y_change = 0

        if self.current_steps >= self.max_steps:
            if self.state != "stalling":
                directions = self.directions.copy()
                remove_dir = self.direction
                if remove_dir in directions:
                    directions.remove(remove_dir)
                    self.direction = random.choice(directions)
                    self.stall_steps = random.randint(40, 180)
                self.state = "stalling"
                self.current_steps = 0

    def update(self):
        self.update_movement()
        self.move()
