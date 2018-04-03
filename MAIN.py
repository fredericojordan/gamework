import pygame
from pygame.locals import (
    K_m,
    K_p,
    K_q,
    K_c,
    K_SPACE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
)
import sys

import camera
import maps
import player
import tracks
import traffic

TRAFFIC_COUNT = 50
MAP_LENGTH = 50


def main():
    """Main function."""
    
    # initialize objects.
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 24)
    car = player.Player()
    cam = camera.Camera()
    
    # create sprite groups.
    map_s     = pygame.sprite.Group()
    player_s  = pygame.sprite.Group()
    traffic_s = pygame.sprite.Group()
    tracks_s  = pygame.sprite.Group()

    # load map
    maps.initialize()
    for y in range(MAP_LENGTH):
        map_s.add(maps.Map(0, -y * maps.MAP_SIZE[1]))

    # load tracks
    tracks.initialize()
    
    # load traffic
    traffic.initialize()
    for _ in range(0, TRAFFIC_COUNT):
        traffic_s.add(traffic.Traffic())

    player_s.add(car)

    cam.set_pos(car.x, car.y)

    while running:
        # Render loop.
        
        # Check for key input. (KEYDOWN, trigger often)
        keys = pygame.key.get_pressed()

        # Check for menu/reset, (keyup event - trigger ONCE)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if (keys[K_p]):
                    car.reset()
                if (keys[K_q]):
                    pygame.quit()
                    sys.exit(0)
                if (keys[K_c]):
                    car.change_sprite()
                if keys[K_SPACE]:
                    car.release_handbrake()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

        if keys[K_LEFT]:
            car.steerleft()
        if keys[K_RIGHT]:
            car.steerright()
        if keys[K_UP]:
            car.accelerate()
        else:
            car.soften()
        if keys[K_DOWN]:
            car.decelerate()
        if keys[K_SPACE]:
            car.pull_handbrake()

        cam.set_pos(car.x, car.y)

        # Show text data.
        text_color = (170, 80, 50)
        text_fps = font.render('FPS: ' + str(int(clock.get_fps())), 1, text_color)
        text_score = font.render('PROGRESS: {:.0f}'.format(car.get_progress()), 1, text_color)
        text_speed = font.render('SPEED: {:.0f}'.format(car.speed*10), 1, text_color)
        textpos_fps = text_fps.get_rect(centery=25, centerx=60)
        textpos_score = text_fps.get_rect(centery=45, centerx=60)
        textpos_speed = text_fps.get_rect(centery=65, centerx=60)
                
        # Blit Blit..       
        screen.blit(text_fps, textpos_fps)
        screen.blit(text_score, textpos_score)
        screen.blit(text_speed, textpos_speed)
        pygame.display.flip()

        # Render Scene
        screen.blit(background, (0,0))

        map_s.update(cam.x, cam.y)
        map_s.draw(screen)
        
        # Conditional renders/effects
        if (car.tracks):
            tracks_s.add(tracks.Track(car.x, car.y, car.dir))

        # Just render..
        tracks_s.update(cam.x, cam.y)
        tracks_s.draw(screen)
        
        player_s.update()
        player_s.draw(screen)

        traffic_s.update(cam.x, cam.y)
        traffic_s.draw(screen)

        # Check collision!!!
        collided_cars = pygame.sprite.spritecollide(car, traffic_s, False)
        if collided_cars:
            if car.speed > 0:
                for traffic_car in collided_cars:
                    traffic_car.impact(car.dir, car.speed)
                car.impact()        

        clock.tick(64)
        

def setup():
    """Initialization"""
    pygame.init()
    pygame.display.set_caption('Race of Math.')
    pygame.mouse.set_visible(False)

if __name__ == '__main__':
    setup()
    
    screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                      pygame.display.Info().current_h),
                                     pygame.FULLSCREEN)
    
    font = pygame.font.Font(None, 24)
    
    # New background surface
    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha()
    background.fill((26, 26, 26))
    
    # Enter the main loop.
    main()
    
    pygame.quit()
    sys.exit(0)
