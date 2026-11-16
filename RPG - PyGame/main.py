import pygame
import sys
import random
import os
import time
from threading import Thread
from characters import avatar_list, boss_list, enemies_list, npc_list
from colors import *
from menu import GameMenu
from status_bars import CharacterStatus

# Initialize PyGame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1160
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeons and the Ur-Dragon")

# Font setup
font = pygame.font.SysFont('Arial', 28, bold=True)
title_font = pygame.font.SysFont('Arial', 40, bold=True)


def play_music_loop():
    songs = [
        "AudioCoffee Band - Cinematic Galactic.mp3",
        "ArcSound - Dark Horror Nightmare.mp3",
        "BlackTrendMusic - Epic.mp3",
        "Lowtone Music - Cinematic Soundtrack.mp3",
        "Lowtone Music - Dark Trailer.mp3",
        "Lowtone Music - Epic Action.mp3",
        "Lowtone Music - Fantasy Teaser.mp3",
        "Lowtone Music - Get Up & Fight.mp3",
        "Lowtone Music - This is War - Cinematic Epic.mp3",
        "UNIVERSFIELD - Gloomy Depths.mp3",
    ]

    music_dir = os.path.join(os.path.dirname(__file__), "..", "Music")
    playlist = [os.path.normpath(os.path.join(music_dir, song)) for song in songs]
    playlist = [song for song in playlist if os.path.exists(song)]
    if not playlist:
        return

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error:
        return

    pygame.mixer.music.set_volume(0.8)

    def queue_songs(song_list):
        random.shuffle(song_list)
        pygame.mixer.music.load(song_list[0])
        for song in song_list[1:]:
            pygame.mixer.music.queue(song)
        pygame.mixer.music.play()

    queue_songs(playlist.copy())

    while True:
        if not pygame.mixer.music.get_busy():
            queue_songs(playlist.copy())
        time.sleep(5)

class Battle:
    def __init__(self, player_characters, enemies):
        self.player_characters = player_characters
        self.enemies = enemies
        self.current_turn = 1
        self.action_cooldown = 0
        self.action_wait_time = 90
        self.game_over = 0
        self.all_fighters = player_characters + enemies
        self.turn_order = []
        self.current_fighter = None
        self.selected_target_index = 0
        self.selected_spell_index = 0
        self.last_action_text = "Press LEFT/RIGHT to select a target, SPACE to act."
        self.reset_turn_order()

    def get_alive_players(self):
        return [fighter for fighter in self.player_characters if fighter.hp > 0]

    def get_alive_enemies(self):
        return [fighter for fighter in self.enemies if fighter.hp > 0]

    def reset_turn_order(self):
        self.turn_order = sorted(
            [fighter for fighter in self.all_fighters if fighter.hp > 0],
            key=lambda fighter: fighter.speed,
            reverse=True,
        )
        self.current_fighter = self.turn_order[0] if self.turn_order else None
        self.selected_target_index = 0
        self.selected_spell_index = self.get_default_spell_index(self.current_fighter)

    def advance_turn(self):
        if self.is_battle_over():
            self.current_fighter = None
            return

        if not self.turn_order:
            self.reset_turn_order()
            return

        self.turn_order.pop(0)
        if not self.turn_order:
            self.current_turn += 1
            self.reset_turn_order()
            return

        self.current_fighter = self.turn_order[0]
        if self.current_fighter in self.player_characters:
            alive_enemies = self.get_alive_enemies()
            if alive_enemies:
                self.selected_target_index %= len(alive_enemies)
            self.selected_spell_index = self.get_default_spell_index(self.current_fighter)

    def is_battle_over(self):
        return not self.get_alive_enemies() or not self.get_alive_players()

    def get_selected_enemy(self):
        alive_enemies = self.get_alive_enemies()
        if not alive_enemies:
            return None
        self.selected_target_index %= len(alive_enemies)
        return alive_enemies[self.selected_target_index]

    def cycle_target(self, direction):
        alive_enemies = self.get_alive_enemies()
        if not alive_enemies:
            return
        self.selected_target_index = (self.selected_target_index + direction) % len(alive_enemies)

    def cycle_spell(self, direction):
        if not self.current_fighter or not self.current_fighter.spells:
            return
        self.selected_spell_index = (self.selected_spell_index + direction) % len(self.current_fighter.spells)

    def get_selected_spell(self):
        if not self.current_fighter or not self.current_fighter.spells:
            return None
        self.selected_spell_index %= len(self.current_fighter.spells)
        return self.current_fighter.spells[self.selected_spell_index]

    def get_default_spell_index(self, fighter):
        if not fighter or not fighter.spells:
            return 0

        for index, spell in enumerate(fighter.spells):
            if spell.effect_type == "damage":
                return index
        return 0

    def select_enemy_spell(self, enemy):
        if not enemy.spells:
            return None
        spells = list(enemy.spell_weights.keys())
        weights = list(enemy.spell_weights.values())
        return random.choices(spells, weights=weights, k=1)[0]

    def choose_enemy_target(self):
        alive_allies = self.get_alive_players()
        if not alive_allies:
            return None

        sorted_by_hp = sorted(alive_allies, key=lambda fighter: fighter.hp)
        sorted_by_mgk_def = sorted(alive_allies, key=lambda fighter: fighter.mgk_def)
        sorted_by_attack = sorted(alive_allies, key=lambda fighter: fighter.strength, reverse=True)

        low_hp_ally = sorted_by_hp[0]
        if low_hp_ally.hp < (low_hp_ally.max_hp // 2) and low_hp_ally.mgk_def < low_hp_ally.df:
            return low_hp_ally

        low_mgk_ally = sorted_by_mgk_def[0]
        high_attack_ally = sorted_by_attack[0]
        priority_targets = [low_mgk_ally] if low_mgk_ally == high_attack_ally else [low_mgk_ally, high_attack_ally]
        return random.choice(priority_targets)

    def perform_attack(self, attacker, target):
        critical_chance = 0.2
        critical_multiplier = 2
        min_attack = max(1, attacker.strength // 2)
        max_attack = max(min_attack, attacker.strength)
        raw_damage = random.randint(min_attack, max_attack)
        if attacker in self.enemies:
            effective_defense = max(0, int(target.df * 0.6))
            damage = max(8, raw_damage - effective_defense)
        else:
            effective_defense = max(0, int(target.df * 0.5))
            damage = max(5, raw_damage - effective_defense)
        is_critical = random.random() < critical_chance

        if damage < 0:
            damage = 0

        if is_critical and damage > 0:
            damage *= critical_multiplier

        target.hp = max(0, target.hp - damage)
        attacker.action = 1
        attacker.frame_index = 0
        target.action = 2 if target.hp > 0 else 3
        target.frame_index = 0

        if damage == 0:
            self.last_action_text = f"{attacker.name}'s attack could not get through {target.name}'s defense."
        elif is_critical:
            self.last_action_text = f"Critical hit! {attacker.name} hits {target.name} for {damage}."
        else:
            self.last_action_text = f"{attacker.name} hits {target.name} for {damage}."

    def _apply_damage_animation(self, targets):
        for target in targets:
            target.action = 2 if target.hp > 0 else 3
            target.frame_index = 0

    def _select_spell_target(self, caster, spell):
        is_player = caster in self.player_characters
        allies = self.get_alive_players() if is_player else self.get_alive_enemies()
        enemies = self.get_alive_enemies() if is_player else self.get_alive_players()
        aoe_spells = {"Meteor", "Quake", "Ultima", "Flare", "Breath of Fire", "Pandemonium"}

        if spell.effect_type == "damage":
            if spell.name in aoe_spells:
                return enemies
            return self.get_selected_enemy() if is_player else self.choose_enemy_target()

        if spell.effect_type in {"healing", "buff"}:
            return min(allies, key=lambda fighter: fighter.hp / fighter.max_hp) if allies else caster

        if spell.effect_type == "revival":
            fallen = [fighter for fighter in (self.player_characters if is_player else self.enemies) if fighter.hp <= 0]
            return fallen[0] if fallen else caster

        return None

    def perform_magic(self, caster, spell):
        target = self._select_spell_target(caster, spell)
        if target is None:
            self.last_action_text = f"{caster.name} has no valid target for {spell.name}."
            return

        if caster.mp < spell.mp:
            self.last_action_text = f"{caster.name} does not have enough MP for {spell.name}."
            return

        previous_mp = caster.mp
        caster.mp -= spell.mp
        caster.action = 1
        caster.frame_index = 0

        targets = target if isinstance(target, list) else [target]
        hp_before = {combatant: combatant.hp for combatant in targets}

        caster.cast_magic(target, spell, spend_mp=False)
        mp_spent = previous_mp - caster.mp

        if spell.effect_type == "damage":
            self._apply_damage_animation(targets)
            total_damage = sum(max(0, hp_before[combatant] - combatant.hp) for combatant in targets)
            if len(targets) > 1:
                self.last_action_text = f"{caster.name} casts {spell.name} for {total_damage} total damage (-{mp_spent} MP, {caster.mp} MP left)."
            else:
                self.last_action_text = f"{caster.name} casts {spell.name} on {targets[0].name} for {total_damage} (-{mp_spent} MP, {caster.mp} MP left)."
        elif spell.effect_type == "healing":
            healed_amount = max(0, targets[0].hp - hp_before[targets[0]])
            self.last_action_text = f"{caster.name} casts {spell.name}, healing {targets[0].name} for {healed_amount} (-{mp_spent} MP, {caster.mp} MP left)."
        elif spell.effect_type == "buff":
            self.last_action_text = f"{caster.name} casts {spell.name} on {targets[0].name} (-{mp_spent} MP, {caster.mp} MP left)."
        elif spell.effect_type == "revival":
            self.last_action_text = f"{caster.name} casts {spell.name} on {targets[0].name} (-{mp_spent} MP, {caster.mp} MP left)."
        else:
            self.last_action_text = f"{caster.name} casts {spell.name} (-{mp_spent} MP, {caster.mp} MP left)."

    def perform_enemy_action(self):
        enemy = self.current_fighter
        if enemy is None:
            return True

        if enemy.spells:
            magic_priority = enemy.mgk_atk / (enemy.mgk_atk + max(1, enemy.atk))
            if random.random() < magic_priority:
                spell = self.select_enemy_spell(enemy)
                if spell:
                    self.perform_magic(enemy, spell)
                    if self.is_battle_over():
                        return True
                    self.advance_turn()
                    return False

        target = self.choose_enemy_target()
        if target is None:
            return True
        self.perform_attack(enemy, target)
        if self.is_battle_over():
            return True
        self.advance_turn()
        return False

    def handle_event(self, event):
        if self.current_fighter is None:
            return True

        if event.type == pygame.KEYDOWN:
            if self.current_fighter in self.player_characters:
                if event.key == pygame.K_LEFT:
                    self.cycle_target(-1)
                elif event.key == pygame.K_RIGHT:
                    self.cycle_target(1)
                elif event.key == pygame.K_UP:
                    self.cycle_spell(-1)
                elif event.key == pygame.K_DOWN:
                    self.cycle_spell(1)
                elif event.key == pygame.K_m:
                    spell = self.get_selected_spell()
                    if spell is None:
                        self.last_action_text = f"{self.current_fighter.name} has no spells."
                        return False
                    self.perform_magic(self.current_fighter, spell)
                    if self.is_battle_over():
                        return True
                    self.advance_turn()
                elif event.key == pygame.K_SPACE:
                    target = self.get_selected_enemy()
                    if target is None:
                        return True
                    self.perform_attack(self.current_fighter, target)
                    if self.is_battle_over():
                        return True
                    self.advance_turn()
            elif event.key == pygame.K_SPACE:
                return self.perform_enemy_action()
        
        return False

    def draw(self, surface):
        def draw_side(fighters, side):
            for index, fighter in enumerate(fighters[:4]):
                if fighter.hp <= 0:
                    continue

                fighter.update()
                if not fighter.current_frame:
                    continue

                frame_width = fighter.render_width or fighter.current_frame.get_width()
                frame_height = fighter.render_height or fighter.current_frame.get_height()

                row = index // 2
                col = index % 2

                if side == "allies":
                    base_positions = [
                        (70, SCREEN_HEIGHT - 210),   # back-left
                        (190, SCREEN_HEIGHT - 210),  # back-right
                        (120, SCREEN_HEIGHT - 90),   # front-left
                        (255, SCREEN_HEIGHT - 90),   # front-right
                    ]
                else:
                    base_positions = [
                        (SCREEN_WIDTH - 335, SCREEN_HEIGHT - 210),  # back-left
                        (SCREEN_WIDTH - 205, SCREEN_HEIGHT - 210),  # back-right
                        (SCREEN_WIDTH - 290, SCREEN_HEIGHT - 90),   # front-left
                        (SCREEN_WIDTH - 145, SCREEN_HEIGHT - 90),   # front-right
                    ]

                slot_index = (row * 2) + col
                anchor_x, ground_y = base_positions[slot_index]
                fighter.xcoord = anchor_x
                fighter.ycoord = ground_y - frame_height
                fighter.draw(surface)

                if fighter == self.current_fighter:
                    pygame.draw.rect(
                        surface,
                        bcolors.GREEN,
                        (
                            fighter.xcoord - 5,
                            fighter.ycoord - 5,
                            frame_width + 10,
                            frame_height + 10,
                        ),
                        2,
                    )

                if self.current_fighter in self.player_characters and fighter == self.get_selected_enemy():
                    pygame.draw.rect(
                        surface,
                        bcolors.YELLOW,
                        (
                            fighter.xcoord - 10,
                            fighter.ycoord - 10,
                            frame_width + 20,
                            frame_height + 20,
                        ),
                        2,
                    )

        draw_side(self.player_characters, "allies")
        draw_side(self.enemies, "enemies")

class Game:
    def __init__(self):
        self.state = "menu"
        self.selected_characters = []
        self.current_enemy_index = 0
        self.battle = None
        self.menu = GameMenu(self.start_battle)
        self.character_statuses = []
        self.enemy_statuses = []
        self.font = pygame.font.SysFont('Arial', 28, bold=True)
        self.battle_background = None
        self.music_thread = Thread(target=play_music_loop, daemon=True)
        self.music_thread.start()

    def load_battle_assets(self):
        if self.battle_background is not None:
            return

        background_path = os.path.join(
            os.path.dirname(__file__),
            "Images",
            "Background",
            "Eerie Cave Background1.png",
        )

        try:
            background = pygame.image.load(background_path)
            if pygame.display.get_surface() is not None:
                background = background.convert()
            self.battle_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            self.battle_background = None

    def draw_character_selection(self):
        screen.fill(bcolors.BLACK)
        title = title_font.render("Select 2-3 Characters", True, bcolors.WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        y_offset = 150
        for i, character in enumerate(avatar_list):
            color = bcolors.GREEN if character in self.selected_characters else bcolors.WHITE
            text = font.render(f"{i+1}. {character.name} - HP: {character.hp} MP: {character.mp}", True, color)
            screen.blit(text, (100, y_offset))
            y_offset += 40

        if len(self.selected_characters) >= 2:
            start_text = font.render("Press SPACE to start battle", True, bcolors.WHITE)
            screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT - 100))

    def handle_character_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                index = event.key - pygame.K_1
                if index < len(avatar_list):
                    character = avatar_list[index]
                    if character in self.selected_characters:
                        self.selected_characters.remove(character)
                    elif len(self.selected_characters) < 3:
                        self.selected_characters.append(character)
            elif event.key == pygame.K_SPACE and len(self.selected_characters) >= 2:
                self.start_battle()

    def start_battle(self, selected_characters=None):
        self.load_battle_assets()

        if selected_characters is not None:
            chosen_party = list(selected_characters)
        else:
            chosen_party = list(self.selected_characters)

        ally_count = min(max(0, 4 - len(chosen_party)), len(npc_list))
        random_allies = random.sample(npc_list, ally_count)
        party_templates = chosen_party + random_allies
        self.selected_characters = [character.create_fighter(flip=False) for character in party_templates]

        enemy_count = min(4, len(enemies_list))
        random_enemies = random.sample(enemies_list, enemy_count)
        self.enemies = [enemy.create_fighter(flip=True) for enemy in random_enemies]
        
        # Initialize battle with preloaded characters and enemies
        self.battle = Battle(self.selected_characters, self.enemies)
        self.state = "battle"
        
        # Create status displays for characters and enemies
        self.character_statuses = []
        self.enemy_statuses = []
        
        # Position character status bars
        y_offset = 48
        player_spacing = max(46, 288 // max(1, len(self.selected_characters)))
        for character in self.selected_characters:
            self.character_statuses.append(CharacterStatus(character, 50, y_offset))
            y_offset += player_spacing
            
        # Position enemy status bars
        y_offset = 48
        enemy_spacing = max(46, 288 // max(1, len(self.enemies)))
        for enemy in self.enemies:
            self.enemy_statuses.append(CharacterStatus(enemy, SCREEN_WIDTH - 248, y_offset))
            y_offset += enemy_spacing

    def draw_status_bars(self):
        # Draw character status bars
        for status in self.character_statuses:
            status.draw(screen)
            
        # Draw enemy status bars
        for status in self.enemy_statuses:
            status.draw(screen)

    def draw_battle_info(self):
        # Draw current turn information
        if self.battle and self.battle.current_fighter:
            current_fighter = self.battle.current_fighter
            turn_text = self.font.render(
                f"Turn {self.battle.current_turn}: {current_fighter.name}",
                True,
                bcolors.WHITE,
            )
            screen.blit(turn_text, (SCREEN_WIDTH//2 - turn_text.get_width()//2, 10))
            
            # Draw instructions
            if current_fighter in self.battle.player_characters:
                instructions_text = "LEFT/RIGHT target, UP/DOWN spell, SPACE attack, M cast"
            else:
                instructions_text = "Press SPACE to resolve the enemy turn"

            instructions = self.font.render(instructions_text, True, bcolors.WHITE)
            screen.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, SCREEN_HEIGHT - 55))

            selected_spell = self.battle.get_selected_spell() if current_fighter in self.battle.player_characters else None
            if selected_spell:
                spell_text = self.font.render(
                    f"Selected Spell: {selected_spell.name} ({selected_spell.mp} MP)",
                    True,
                    bcolors.WHITE,
                )
                screen.blit(spell_text, (SCREEN_WIDTH//2 - spell_text.get_width()//2, SCREEN_HEIGHT - 82))

            action_text = self.font.render(self.battle.last_action_text, True, bcolors.WHITE)
            screen.blit(action_text, (SCREEN_WIDTH//2 - action_text.get_width()//2, SCREEN_HEIGHT - 28))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                
                if self.state == "battle":
                    if self.battle.handle_event(event):
                        self.current_enemy_index += 1
                        if self.current_enemy_index < len(enemies_list) + len(boss_list):
                            self.start_battle()
                        else:
                            self.state = "game_over"

            if self.state == "menu":
                self.menu.update(events)
                screen.fill(bcolors.BLACK)
                self.menu.draw(screen)
            elif self.state == "battle":
                if self.battle_background:
                    screen.blit(self.battle_background, (0, 0))
                else:
                    screen.fill(bcolors.BLACK)
                self.battle.draw(screen)
                self.draw_status_bars()
                self.draw_battle_info()
            elif self.state == "game_over":
                screen.fill(bcolors.BLACK)
                text = pygame.font.SysFont('Arial', 40, bold=True).render("Game Over!", True, bcolors.WHITE)
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 
