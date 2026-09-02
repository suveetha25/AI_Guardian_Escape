"""
=========================================
AI Guardian Escape
main.py

Main Game Controller
=========================================
"""

import sys
import pygame

from settings import *
from menu import Menu
from map import AdventureMap
from level import Level
from player import Player
from guardian import Guardian
from ui import UI
from powerups import create_powerups
from effects import FadeEffect, PortalGlow, MagicAura, FlashEffect
from particles import create_particles, snow_effect, fire_effect, sparkle, portal_glow


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = SPLASH
        self.previous_state = MENU

        self.menu = Menu()
        self.adventure_map = AdventureMap()
        self.ui = UI()

        self.fade = FadeEffect()
        self.portal_glow = PortalGlow()
        self.magic_aura = MagicAura()
        self.flash = FlashEffect()
        self.particles = create_particles()

        self.level = None
        self.player = None
        self.guardian = None
        self.powerups = None

        self.current_level_number = FOREST
        self.completed_levels = set()
        self.level_complete_timer = 0
        self.splash_timer = FPS * 2

        self.big_font = pygame.font.SysFont("arial", 52, bold=True)
        self.medium_font = pygame.font.SysFont("arial", 32, bold=True)
        self.small_font = pygame.font.SysFont("arial", 24)

        self.debug_mode = False
        self.damage_cooldown = 0

        self.start_level(FOREST)

    # =====================================
    # Start / Reset Level
    # =====================================
    def start_level(self, level_number):
        self.current_level_number = level_number
        self.level = Level(level_number)
        self.player = Player()
        self.guardian = Guardian(level_number)
        self.powerups = create_powerups()

        self.portal_glow = PortalGlow()
        self.magic_aura = MagicAura()
        self.flash = FlashEffect()
        self.particles = create_particles()

        self.damage_cooldown = 0

        if hasattr(self.adventure_map, "selected"):
            for index, level in enumerate(self.adventure_map.levels):
                if level["id"] == level_number:
                    self.adventure_map.selected = index
                    break

    # =====================================
    # Unlock Next Level
    # =====================================
    def unlock_next_level(self, completed_level):
        if completed_level == FOREST:
            self.adventure_map.unlock(CASTLE)
        elif completed_level == CASTLE:
            self.adventure_map.unlock(SNOW)
        elif completed_level == SNOW:
            self.adventure_map.unlock(VOLCANO)

    # =====================================
    # Return to Main Menu
    # =====================================
    def go_to_menu(self):
        self.state = MENU
        self.menu.selected = 0

    # =====================================
    # Particle Effects
    # =====================================
    def update_environment_particles(self):
        if self.current_level_number == SNOW:
            snow_effect(self.particles)
        elif self.current_level_number == VOLCANO:
            fire_effect(self.particles)

        if self.level and self.level.portal_open:
            portal_glow(self.particles, self.level.portal)

    # =====================================
    # Draw Splash
    # =====================================
    def draw_splash(self):
        self.screen.fill((10, 10, 25))

        title = self.big_font.render(
            "AI GUARDIAN ESCAPE",
            True,
            YELLOW
        )
        subtitle = self.medium_font.render(
            "The Magical Worlds",
            True,
            WHITE
        )
        text = self.small_font.render(
            "MSc Artificial Intelligence Mini Project",
            True,
            CYAN
        )

        self.screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 220)
        )
        self.screen.blit(
            subtitle,
            (WIDTH // 2 - subtitle.get_width() // 2, 300)
        )
        self.screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, 380)
        )

    # =====================================
    # Draw Pause Screen
    # =====================================
    def draw_pause(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(170)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        paused = self.big_font.render("PAUSED", True, YELLOW)
        info1 = self.small_font.render("Press ESC to Resume", True, WHITE)
        info2 = self.small_font.render("Press M for Main Menu", True, WHITE)

        self.screen.blit(
            paused,
            (WIDTH // 2 - paused.get_width() // 2, 220)
        )
        self.screen.blit(
            info1,
            (WIDTH // 2 - info1.get_width() // 2, 320)
        )
        self.screen.blit(
            info2,
            (WIDTH // 2 - info2.get_width() // 2, 360)
        )

    # =====================================
    # Draw Level Complete
    # =====================================
    def draw_level_complete(self):
        self.screen.fill((15, 40, 20))

        title = self.big_font.render("LEVEL COMPLETE", True, GREEN)
        level_name = self.medium_font.render(
            f"{self.level.name}",
            True,
            WHITE
        )
        stars = self.medium_font.render(
            f"Stars Earned : {self.level.get_stars()}",
            True,
            YELLOW
        )
        score = self.small_font.render(
            f"Score : {self.player.score}",
            True,
            WHITE
        )

        self.screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 180)
        )
        self.screen.blit(
            level_name,
            (WIDTH // 2 - level_name.get_width() // 2, 270)
        )
        self.screen.blit(
            stars,
            (WIDTH // 2 - stars.get_width() // 2, 340)
        )
        self.screen.blit(
            score,
            (WIDTH // 2 - score.get_width() // 2, 395)
        )

        msg = self.small_font.render(
            "Preparing next screen...",
            True,
            CYAN
        )
        self.screen.blit(
            msg,
            (WIDTH // 2 - msg.get_width() // 2, 470)
        )

    # =====================================
    # Draw Game Over
    # =====================================
    def draw_game_over(self):
        self.screen.fill((40, 10, 10))

        title = self.big_font.render("GAME OVER", True, RED)
        line1 = self.small_font.render(
            "You were caught by the AI Guardian or ran out of time.",
            True,
            WHITE
        )
        line2 = self.small_font.render(
            "Press R to Retry or M for Main Menu",
            True,
            YELLOW
        )

        self.screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 220)
        )
        self.screen.blit(
            line1,
            (WIDTH // 2 - line1.get_width() // 2, 320)
        )
        self.screen.blit(
            line2,
            (WIDTH // 2 - line2.get_width() // 2, 380)
        )

    # =====================================
    # Draw Congratulations
    # =====================================
    def draw_congratulations(self):
        self.screen.fill((20, 25, 60))

        title = self.big_font.render("CONGRATULATIONS!", True, YELLOW)
        line1 = self.medium_font.render(
            "You escaped all magical worlds.",
            True,
            WHITE
        )
        line2 = self.small_font.render(
            "Press ENTER for Credits or ESC for Main Menu",
            True,
            CYAN
        )

        self.screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 200)
        )
        self.screen.blit(
            line1,
            (WIDTH // 2 - line1.get_width() // 2, 300)
        )
        self.screen.blit(
            line2,
            (WIDTH // 2 - line2.get_width() // 2, 390)
        )

    # =====================================
    # Draw Credits
    # =====================================
    def draw_credits(self):
        self.screen.fill(BLACK)

        lines = [
            ("CREDITS", YELLOW, self.big_font),
            ("", WHITE, self.small_font),
            ("Project: AI Guardian Escape", WHITE, self.medium_font),
            ("Subtitle: The Magical Worlds", WHITE, self.medium_font),
            ("Built with Python and Pygame", CYAN, self.small_font),
            ("MSc Artificial Intelligence Mini Project", WHITE, self.small_font),
            ("", WHITE, self.small_font),
            ("Press ESC to return to Main Menu", GREEN, self.small_font),
        ]

        y = 120
        for text, colour, font in lines:
            image = font.render(text, True, colour)
            self.screen.blit(
                image,
                (WIDTH // 2 - image.get_width() // 2, y)
            )
            y += 55

    # =====================================
    # Gameplay Update
    # =====================================
    def update_gameplay(self):
        self.player.move(self.level.walls)
        self.player.update()
        self.level.update(self.player)
        self.guardian.update(self.player, self.level.walls)
        self.powerups.update(self.player)

        self.portal_glow.update()
        self.flash.update()

        if self.player.is_invisible:
            self.magic_aura.update()

        self.update_environment_particles()
        self.particles.update()

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.guardian.caught_player(self.player) and self.damage_cooldown == 0:
            self.player.take_damage()
            self.flash.trigger()
            sparkle(self.particles, self.player.rect.centerx, self.player.rect.centery)
            self.damage_cooldown = FPS

            if self.player.health <= 0:
                self.state = GAME_OVER

        if self.level.time_up():
            self.state = GAME_OVER

        if self.level.reached_portal(self.player):
            sparkle(self.particles, self.level.portal.centerx, self.level.portal.centery)
            self.completed_levels.add(self.current_level_number)
            self.unlock_next_level(self.current_level_number)
            self.level_complete_timer = FPS * 2
            self.state = LEVEL_COMPLETE

    # =====================================
    # Gameplay Draw
    # =====================================
    def draw_gameplay(self):
        self.level.draw(self.screen)
        self.powerups.draw(self.screen)

        if self.level.portal_open:
            self.portal_glow.draw(self.screen, self.level.portal)

        self.particles.draw(self.screen)

        self.player.draw(self.screen)

        if self.player.is_invisible:
            self.magic_aura.draw(self.screen, self.player)

        self.guardian.draw(self.screen)
        self.ui.draw(self.screen, self.player, self.guardian, self.level)

        if self.debug_mode:
            self.ui.draw_debug(self.screen, self.guardian, self.player)

        self.flash.draw(self.screen)

    # =====================================
    # Event Handling
    # =====================================
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.debug_mode = not self.debug_mode

                if self.state == MENU:
                    self.handle_menu_events(event)

                elif self.state == HELP:
                    if event.key == pygame.K_ESCAPE:
                        self.state = MENU

                elif self.state == SETTINGS_MENU:
                    if event.key == pygame.K_ESCAPE:
                        self.state = MENU

                elif self.state == MAP:
                    self.handle_map_events(event)

                elif self.state == PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.previous_state = PLAYING
                        self.state = PAUSE

                elif self.state == PAUSE:
                    if event.key == pygame.K_ESCAPE:
                        self.state = PLAYING
                    elif event.key == pygame.K_m:
                        self.go_to_menu()

                elif self.state == GAME_OVER:
                    if event.key == pygame.K_r:
                        self.start_level(self.current_level_number)
                        self.state = PLAYING
                    elif event.key == pygame.K_m:
                        self.go_to_menu()

                elif self.state == CONGRATULATIONS:
                    if event.key == pygame.K_RETURN:
                        self.state = CREDITS
                    elif event.key == pygame.K_ESCAPE:
                        self.go_to_menu()

                elif self.state == CREDITS:
                    if event.key == pygame.K_ESCAPE:
                        self.go_to_menu()

    # =====================================
    # Menu Events
    # =====================================
    def handle_menu_events(self, event):
        if event.key == pygame.K_UP:
            self.menu.move_up()

        elif event.key == pygame.K_DOWN:
            self.menu.move_down()

        elif event.key == pygame.K_RETURN:
            choice = self.menu.get_selected()

            if choice == "Play":
                self.start_level(FOREST)
                self.state = PLAYING

            elif choice == "Adventure Map":
                self.state = MAP

            elif choice == "How To Play":
                self.state = HELP

            elif choice == "Settings":
                self.state = SETTINGS_MENU

            elif choice == "Exit":
                self.running = False

    # =====================================
    # Map Events
    # =====================================
    def handle_map_events(self, event):
        if event.key == pygame.K_LEFT:
            self.adventure_map.move_left()

        elif event.key == pygame.K_RIGHT:
            self.adventure_map.move_right()

        elif event.key == pygame.K_ESCAPE:
            self.state = MENU

        elif event.key == pygame.K_RETURN:
            if self.adventure_map.can_play():
                selected_level = self.adventure_map.get_level()
                self.start_level(selected_level)
                self.state = PLAYING

    # =====================================
    # State Update
    # =====================================
    def update(self):
        if self.state == SPLASH:
            self.splash_timer -= 1
            if self.splash_timer <= 0:
                self.state = MENU

        elif self.state == PLAYING:
            self.update_gameplay()

        elif self.state == LEVEL_COMPLETE:
            self.level_complete_timer -= 1
            if self.level_complete_timer <= 0:
                if self.current_level_number == VOLCANO:
                    self.state = CONGRATULATIONS
                else:
                    self.state = MAP

        self.fade.update()

    # =====================================
    # State Draw
    # =====================================
    def draw(self):
        if self.state == SPLASH:
            self.draw_splash()

        elif self.state == MENU:
            self.menu.draw(self.screen)

        elif self.state == HELP:
            self.menu.draw_help(self.screen)

        elif self.state == SETTINGS_MENU:
            self.menu.draw_settings(self.screen)

        elif self.state == MAP:
            self.adventure_map.draw(self.screen)

        elif self.state == PLAYING:
            self.draw_gameplay()

        elif self.state == PAUSE:
            self.draw_gameplay()
            self.draw_pause()

        elif self.state == LEVEL_COMPLETE:
            self.draw_level_complete()

        elif self.state == GAME_OVER:
            self.draw_game_over()

        elif self.state == CONGRATULATIONS:
            self.draw_congratulations()

        elif self.state == CREDITS:
            self.draw_credits()

        self.fade.draw(self.screen)
        pygame.display.flip()

    # =====================================
    # Game Loop
    # =====================================
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()