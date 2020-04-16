from src.Chest import Chest
from src.Character import Character
from src.Fountain import Fountain
from src.InfoBox import InfoBox
from src.Menus import *
from src.Mission import MissionType
from src.Player import Player
from src.Portal import Portal
from src.fonts import *
from src.constants import *

MAP_WIDTH = TILE_SIZE * 20
MAP_HEIGHT = TILE_SIZE * 10

ACTION_MENU_WIDTH = 200
ITEM_MENU_WIDTH = 550
ITEM_INFO_MENU_WIDTH = 800
ITEM_DELETE_MENU_WIDTH = 350
STATUS_MENU_WIDTH = 300
STATUS_INFO_MENU_WIDTH = 500
EQUIPMENT_MENU_WIDTH = 500


def create_shop_menu(items, gold):
    entries = []
    row = []
    for i, it in enumerate(items):
        entry = {'type': 'item_button', 'item': it, 'price': it.price, 'index': i, 'id': BuyMenu.INTERAC_BUY}
        row.append(entry)
        if len(row) == 2:
            entries.append(row)
            row = []

    if row:
        entries.append(row)

    # Gold at end
    entry = [{'type': 'text', 'text': 'Your gold : ' + str(gold), 'font': ITEM_DESC_FONT}]
    entries.append(entry)

    return InfoBox("Shop - Buying", BuyMenu, "imgs/interface/PopUpMenu.png", entries,
                   ITEM_MENU_WIDTH, close_button=UNFINAL_ACTION, title_color=ORANGE)


def create_inventory_menu(items, gold, price=False):
    entries = []
    row = []
    method_id = SellMenu.INTERAC_SELL if price else InventoryMenu.INTERAC_ITEM
    for i, it in enumerate(items):
        entry = {'type': 'item_button', 'item': it, 'index': i, 'id': method_id}
        # Test if price should appeared
        if price and it:
            entry['price'] = it.price // 2 if it.price != 0 else 0
        row.append(entry)
        if len(row) == 2:
            entries.append(row)
            row = []
    if row:
        entries.append(row)

    # Gold at end
    entry = [{'type': 'text', 'text': 'Your gold : ' + str(gold), 'font': ITEM_DESC_FONT}]
    entries.append(entry)

    title = "Shop - Selling" if price else "Inventory"
    menu_id = SellMenu if price else InventoryMenu
    title_color = ORANGE if price else WHITE
    return InfoBox(title, menu_id, "imgs/interface/PopUpMenu.png", entries,
                   ITEM_MENU_WIDTH, close_button=UNFINAL_ACTION, title_color=title_color)


def create_equipment_menu(equipments):
    entries = []
    body_parts = [['head'], ['body'], ['left_hand', 'right_hand'], ['feet']]
    for part in body_parts:
        row = []
        for member in part:
            entry = {'type': 'item_button', 'item': None, 'index': -1, 'subtype': 'equip',
                     'id': InventoryMenu.INTERAC_ITEM}
            for i, eq in enumerate(equipments):
                if member == eq.body_part:
                    entry = {'type': 'item_button', 'item': eq, 'index': i, 'subtype': 'equip',
                             'id': InventoryMenu.INTERAC_ITEM}
            row.append(entry)
        entries.append(row)
    return InfoBox("Equipment", EquipmentMenu, "imgs/interface/PopUpMenu.png", entries,
                   EQUIPMENT_MENU_WIDTH, close_button=True)


def determine_hp_color(hp, hp_max):
    if hp == hp_max:
        return WHITE
    if hp >= hp_max * 0.75:
        return GREEN
    if hp >= hp_max * 0.5:
        return YELLOW
    if hp >= hp_max * 0.30:
        return ORANGE
    else:
        return RED


def create_status_menu(player):
    entries = [[{'type': 'text', 'color': GREEN, 'text': 'Name :', 'font': ITALIC_ITEM_FONT},
                {'type': 'text', 'text': player.get_formatted_name()}],
               [{'type': 'text', 'color': GREEN, 'text': 'Class :', 'font': ITALIC_ITEM_FONT},
                {'type': 'text', 'text': player.get_formatted_classes()}],
               [{'type': 'text', 'color': GREEN, 'text': 'Race :', 'font': ITALIC_ITEM_FONT},
                {'type': 'text', 'text': player.get_formatted_race()}],
               [{'type': 'text', 'color': GREEN, 'text': 'Level :', 'font': ITALIC_ITEM_FONT},
                {'type': 'text', 'text': str(player.lvl)}],
               [{'type': 'text', 'color': GOLD, 'text': '   XP :', 'font': ITALIC_ITEM_FONT},
                {'type': 'text', 'text': str(player.xp) + ' / ' + str(player.xp_next_lvl)}],
               [{'type': 'text', 'color': WHITE, 'text': 'STATS', 'font': MENU_SUB_TITLE_FONT,
                 'margin': (10, 0, 10, 0)}],
               [{'type': 'text', 'color': WHITE, 'text': 'HP :'},
                {'type': 'text', 'text': str(player.hp) + ' / ' + str(player.hp_max),
                 'color': determine_hp_color(player.hp, player.hp_max)}],
               [{'type': 'text', 'color': WHITE, 'text': 'MOVE :'},
                {'type': 'text', 'text': str(player.max_moves)}],
               [{'type': 'text', 'color': WHITE, 'text': 'ATTACK :'},
                {'type': 'text', 'text': str(player.strength)}],
               [{'type': 'text', 'color': WHITE, 'text': 'DEFENSE :'},
                {'type': 'text', 'text': str(player.defense)}],
               [{'type': 'text', 'color': WHITE, 'text': 'MAGICAL RES :'},
                {'type': 'text', 'text': str(player.res)}],
               [{'type': 'text', 'color': WHITE, 'text': 'ALTERATIONS', 'font': MENU_SUB_TITLE_FONT,
                 'margin': (10, 0, 10, 0)}]]

    alts = player.alterations

    if not alts:
        entries.append([{'type': 'text', 'color': WHITE, 'text': 'None'}])

    for alt in alts:
        entries.append([{'type': 'text_button', 'name': alt.get_formatted_name(), 'id': StatusMenu.INFO_ALTERATION,
                         'color': WHITE, 'color_hover': TURQUOISE, 'obj': alt}])

    return InfoBox("Status", StatusMenu, "imgs/interface/PopUpMenu.png", entries,
                   STATUS_MENU_WIDTH, close_button=UNFINAL_ACTION)


def create_player_menu(player, buildings, interact_entities, missions, foes):
    entries = [[{'name': 'Inventory', 'id': CharacterMenu.INV}],
               [{'name': 'Equipment', 'id': CharacterMenu.EQUIPMENT}],
               [{'name': 'Status', 'id': CharacterMenu.STATUS}], [{'name': 'Wait', 'id': CharacterMenu.WAIT}]]

    # Options flags
    chest_option = False
    portal_option = False
    fountain_option = False
    talk_option = False

    case_pos = (player.pos[0], player.pos[1] - TILE_SIZE)
    if (0, 0) < case_pos < (MAP_WIDTH, MAP_HEIGHT):
        for building in buildings:
            if building.pos == case_pos:
                entries.insert(0, [{'name': 'Visit', 'id': CharacterMenu.VISIT}])
                break

    for ent in interact_entities:
        if abs(ent.pos[0] - player.pos[0]) + abs(ent.pos[1] - player.pos[1]) == TILE_SIZE:
            print("Ent : " + str(ent.pos))
            print("Player : " + str(player.pos))
            if isinstance(ent, Chest) and not ent.opened and not chest_option:
                entries.insert(0, [{'name': 'Open', 'id': CharacterMenu.OPEN_CHEST}])
                chest_option = True
            if isinstance(ent, Portal) and not portal_option:
                entries.insert(0, [{'name': 'Use Portal', 'id': CharacterMenu.USE_PORTAL}])
                portal_option = True
            if isinstance(ent, Fountain) and not fountain_option:
                entries.insert(0, [{'name': 'Drink', 'id': CharacterMenu.DRINK}])
                fountain_option = True
            if isinstance(ent, Character) and not isinstance(ent, Player) and not talk_option:
                entries.insert(0, [{'name': 'Talk', 'id': CharacterMenu.TALK}])
                talk_option = True

    # Check if player is on mission position
    for mission in missions:
        if mission.type is MissionType.POSITION:
            if mission.pos_is_valid(player.pos):
                entries.insert(0, [{'name': 'Take', 'id': CharacterMenu.TAKE}])

    # Check if player could attack something, according to weapon range
    w_range = [1] if player.get_weapon() is None else player.get_weapon().reach
    end = False
    for foe in foes:
        for reach in w_range:
            if abs(foe.pos[0] - player.pos[0]) + abs(foe.pos[1] - player.pos[1]) == TILE_SIZE * reach:
                entries.insert(0, [{'name': 'Attack', 'id': CharacterMenu.ATTACK}])
                end = True
                break
        if end:
            break

    for row in entries:
        for entry in row:
            entry['type'] = 'button'

    return InfoBox("Select an action", CharacterMenu, "imgs/interface/PopUpMenu.png",
                   entries, ACTION_MENU_WIDTH, el_rect_linked=player.get_rect())


def create_main_menu(initialization_phase, pos):
    # Transform pos tuple into rect
    tile = pg.Rect(pos[0], pos[1], 1, 1)
    entries = [[{'name': 'Save', 'id': MainMenu.SAVE}],
               [{'name': 'Suspend', 'id': MainMenu.SUSPEND}]]

    if initialization_phase:
        entries.append([{'name': 'Start', 'id': MainMenu.START}])
    else:
        entries.append([{'name': 'End Turn', 'id': MainMenu.END_TURN}])

    for row in entries:
        for entry in row:
            entry['type'] = 'button'

    return InfoBox("Main Menu", MainMenu, "imgs/interface/PopUpMenu.png", entries,
                   ACTION_MENU_WIDTH, el_rect_linked=tile)