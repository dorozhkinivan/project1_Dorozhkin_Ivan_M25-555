import math

from labyrinth_game import constants, player_actions


def pseudo_random(seed, modulo):
    value = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = value - math.floor(value)
    result = int(fractional_part * modulo)
    return result

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']

    if inventory:
        index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли: {lost_item}")
    else:
        damage_roll = pseudo_random(game_state['steps_taken'], 10)
        if damage_roll < 3:
            print("Вы не смогли устоять перед ловушкой. Игра окончена!")
            game_state['game_over'] = True
        else:
            print("Вам удалось уцелеть, несмотря на ловушку.")

def random_event(game_state):
    event_roll = pseudo_random(game_state['steps_taken'], 10)
    if event_roll != 0:
        return

    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)

    current_room = game_state['current_room']
    inventory = game_state['player_inventory']

    if event_type == 0:
        print("Вы заметили на полу монетку!")
        constants.ROOMS[current_room]['items'].append('coin')
    elif event_type == 1:
        print("Вы слышите странный шорох...")
        if 'sword' in inventory:
            print("Вы взмахнули мечом, и шорох прекратился.")
    elif event_type == 2:
        if current_room == 'trap_room' and 'torch' not in inventory:
            print("Пол начинает опасно трещать под ногами!")
            trigger_trap(game_state)

def describe_current_room(game_state):
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room['description'])

    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))

    exits = ", ".join(room['exits'].keys())
    print("Выходы:", exits)

    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]

    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return

    question, correct_answers = room['puzzle']
    print(question)
    user_answer = player_actions.get_input("Ваш ответ: ")

    if user_answer in correct_answers:
        print("Правильно! Загадка решена.")
        room['puzzle'] = None
    else:
        print("Неверно. Попробуйте снова.")
        if room_name == 'trap_room':
            trigger_trap(game_state)

def attempt_open_treasure(game_state):
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]

    if 'treasure_chest' not in room['items']:
        return

    inventory = game_state['player_inventory']

    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        choice = player_actions.get_input(
            "Сундук заперт. Хотите попробовать ввести код? (да/нет): "
        )
        if choice == 'да':
            user_code = player_actions.get_input("Введите код: ")
            if user_code in room['puzzle'][1]:
                print("Код верен! Сундук открывается.")
                room['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук остаётся запертым.")
        else:
            print("Вы отступаете от сундука.")

def show_help(commands):
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"{cmd:<16} - {desc}")