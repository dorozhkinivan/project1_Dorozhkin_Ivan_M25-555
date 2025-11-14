import constants
import utils


def get_input(prompt="> "):
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    current_room = game_state['current_room']
    room_exits = constants.ROOMS[current_room]['exits']

    if direction in room_exits:
        game_state['current_room'] = room_exits[direction]
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room_items = constants.ROOMS[current_room]['items']

    if item_name in room_items:
        game_state['player_inventory'].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")

def use_item(game_state, item_name):
    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Стало светлее. Вы видите больше деталей вокруг.")
    elif item_name == 'sword':
        print("Вы чувствуете уверенность, держа меч в руках.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print("Вы открыли бронзовую шкатулку и нашли ржавый ключ!")
        else:
            print("Шкатулка уже открыта, внутри пусто.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
