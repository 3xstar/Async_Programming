import time


def setup_raw_dicts():
    words_data: dict = {
        "part1.txt": "Лексема\nСемантика\nСинтаксис",
        "part2.txt": "Морфология\nПрагматика\nДискурс",
        "part3.txt": "Корпус\nТокенизация\nЛемматизация"
    }

    for filename, content in words_data.items():
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(content)
    return list(words_data.keys())


def fetch_ai_description(word: str) -> str:
    time.sleep(0.5)
    return f"{word.upper()}: [Generated AI description]"


def process_file_task(filename: str) -> str:
    """
    Функция-задача
    """

    with open(filename, 'r', encoding="utf-8") as f:
        words = f.read().split()

    # Создаем локальный event loop для текущего потока из пула
    descriptions: list = []
    for word in words:
        desc = fetch_ai_description(word)
        descriptions.append(desc)

    output_filename = filename.replace(".txt", "_proceed.txt")
    with open(output_filename, 'w', encoding="utf-8") as f:
        for d in descriptions:
            f.write(d + "\n")

    return f"Success {output_filename} ({len(descriptions)})"


def main():
    files = setup_raw_dicts()

    t0 = time.perf_counter()

    for filename in files:
        result = process_file_task(filename)
        print(result)

    print(f"Time (sequential): {time.perf_counter() - t0:.4f} sec.")


if __name__ == "__main__":
    main()