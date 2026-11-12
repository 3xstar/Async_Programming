import asyncio
import concurrent.futures
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


async def fetch_ai_description(word: str) -> str:
    await asyncio.sleep(0.5)
    return f"{word.upper()}: [Generated AI description]"

async def async_proceed_words(words: list) -> list:
    tasks = [fetch_ai_description(w) for w in words]
    return await asyncio.gather(*tasks)

def process_file_task(filename: str) -> str:
    """
    Функция-задача для передачи в ThreadPoolExecutor
    """
    with open(filename, 'r', encoding="utf-8") as f:
        words = f.read().split()

    # Создаем локальный event loop для текущего потока из пула
    desc = asyncio.run(async_proceed_words(words))

    output_filename = filename.replace(".txt", "_proceed.txt")
    with open(output_filename, 'w', encoding="utf-8") as f:
        for d in desc:
            f.write(d + "\n")

    return f"Success {output_filename} ({len(desc)})"


def main():
    files = setup_raw_dicts()

    t0 = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Метод map автоматически распределяет файлы по доступным потокам
        # и возвращает результаты в том же порядке, в котором были переданы
        # файлы        
        result = executor.map(process_file_task, files)

        for res in result:
            print(res)

        print(f"Time (ThreadPoolExecutor + async): {time.perf_counter() - t0} sec.")


if __name__ == "__main__":
    main()