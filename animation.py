from os.path import join
import pygame
pygame.init()


# load each frame for an animation keeping into account the duration of each frame
def load_animation(directory, file_name, frame_counters):
    animation_frames = []
    for i in range(len(frame_counters)):
        new_frame = pygame.image.load(join(directory, file_name + "_" + str(i) + ".png"))
        new_frame.convert_alpha()
        animation_frames.append(new_frame)

    frame_indices = []
    for i in range(len(frame_counters)):
        for j in range(frame_counters[i]):
            frame_indices.append(i)

    return animation_frames, frame_indices


# intended to be run once per tick for every animation
def get_surface(animations, frames, rect, current_frame):
    current_frame += 1
    if current_frame == len(frames):
        current_frame = 0

    surface = animations[frames[current_frame]]
    surface = pygame.transform.scale(surface, rect.size)

    return surface, current_frame
