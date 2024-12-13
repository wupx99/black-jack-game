import os

def rename_cards():
    # 定义映射关系
    suit_map = {
        'hearts': 'H',
        'diamonds': 'D',
        'clubs': 'C',
        'spades': 'S'
    }
    value_map = {
        'ace': 'A',
        'jack': 'J',
        'queen': 'Q',
        'king': 'K'
    }

    # 获取cards文件夹的路径
    cards_folder = 'cards'
    if not os.path.exists(cards_folder):
        print(f"Error: {cards_folder} folder not found.")
        return

    # 遍历文件夹中的所有文件
    for filename in os.listdir(cards_folder):
        if filename.endswith('.png'):
            # 分割文件名
            name_parts = filename.split('.')[0].split('_')
            if len(name_parts) != 3:  # 确保文件名格式正确
                print(f"Invalid filename: {filename}")
                continue

            value = name_parts[0]
            suit = name_parts[2]

            # 映射值
            if value in value_map:
                new_value = value_map[value]
            elif value.isdigit():
                new_value = value
            else:
                continue

            # 映射花色
            if suit in suit_map:
                new_suit = suit_map[suit]
            else:
                continue

            # 创建新文件名
            new_filename = f"{new_value}{new_suit}.png"

            # 重命名文件
            old_path = os.path.join(cards_folder, filename)
            new_path = os.path.join(cards_folder, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

    print("Renaming complete.")

# 运行重命名函数
rename_cards()
