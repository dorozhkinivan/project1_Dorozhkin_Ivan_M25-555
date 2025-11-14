import constants
import player_actions


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

    question, correct_answer = room['puzzle']
    print(question)
    user_answer = player_actions.get_input("Ваш ответ: ")

    if user_answer == correct_answer:
        print("Правильно! Загадка решена.")
        room['puzzle'] = None  # Убираем загадку
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]

    if 'treasure_chest' not in room['items']:
        return  # Сундук уже открыт или отсутствует

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
            if user_code == room['puzzle'][1]:
                print("Код верен! Сундук открывается.")
                room['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук остаётся запертым.")
        else:
            print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
