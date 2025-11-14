#!/usr/bin/env python3

import player_actions
import utils


def process_command(game_state, command_line):
    parts = command_line.split()
    command = parts[0] if parts else ''

    match command:
        case 'look':
            utils.describe_current_room(game_state)
        case 'inventory':
            player_actions.show_inventory(game_state)
        case 'help':
            utils.show_help()
        case 'quit' | 'exit':
            print("До свидания!")
            game_state['game_over'] = True
        case 'go':
            if len(parts) > 1:
                player_actions.move_player(game_state, parts[1])
            else:
                print("Укажите направление (north, south, east, west).")
        case 'take':
            if len(parts) > 1:
                player_actions.take_item(game_state, parts[1])
            else:
                print("Укажите предмет, который хотите поднять.")
        case 'use':
            if len(parts) > 1:
                player_actions.use_item(game_state, parts[1])
            else:
                print("Укажите предмет из инвентаря.")
        case 'solve':
            current_room = game_state['current_room']
            if current_room == 'treasure_room':
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")

def main():
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    while not game_state['game_over']:
        command = player_actions.get_input()
        process_command(game_state, command)

if __name__ == '__main__':
    main()
