import sys
import time
import requests

def measure_speed(url: str, iterations: int = 10, chunk_size: int = 65536) -> None:
    """
    Замеряет скорость скачивания, выполняя последовательные запросы к URL.
    
    :param url: Адрес для скачивания (например, большой файл).
    :param iterations: Количество последовательных запросов.
    :param chunk_size: Размер чанка для потоковой загрузки (64 КБ по умолчанию).
    """
    print(f"🚀 Начинаем замер скорости для: {url}")
    print(f"📊 Количество запросов: {iterations}\n")
    
    total_bytes = 0
    total_time = 0.0
    
    session = requests.Session()
    # Отключаем keep-alive для честного замера каждого отдельного соединения
    session.headers.update({"Connection": "close"})

    for i in range(1, iterations + 1):
        try:
            start_time = time.perf_counter()
            request_bytes = 0
            
            # Добавляем заголовки настоящего браузера, чтобы серверы не блокировали скрипт
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/octet-stream, */*"
            }
            
            # Используем stream=True, чтобы не загружать весь файл в оперативную память
            with session.get(url, stream=True, timeout=120, headers=headers) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        request_bytes += len(chunk)
                        
            end_time = time.perf_counter()
            request_time = end_time - start_time
            
            total_bytes += request_bytes
            total_time += request_time
            
            print(f"✅ Запрос {i}: {request_bytes / (1024**2):.2f} МБ за {request_time:.3f} сек")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при выполнении запроса {i}: {e}")
            sys.exit(1)
            
    # Расчёты
    avg_time = total_time / iterations
    total_megabytes = total_bytes / (1024**2)
    total_megabits = total_bytes * 8 / (1024**2)
    
    # Скорость = Общий объём / Общее время
    speed_mbps = total_megabits / total_time
    speed_mbs = total_megabytes / total_time
    
    print("\n" + "="*50)
    print("📈 РЕЗУЛЬТАТЫ ЗАМЕРА:")
    print(f"Общий объём скачанных данных : {total_megabytes:.2f} МБ ({total_bytes:,} байт)")
    print(f"Общее время выполнения         : {total_time:.3f} сек")
    print(f"Среднее время одного запроса   : {avg_time:.3f} сек")
    print(f"Средняя скорость скачивания    : {speed_mbps:.2f} Мбит/с (или {speed_mbs:.2f} МБ/с)")
    print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Использование: python speed_test.py <URL> [количество_запросов]")
        print("📌 Пример: python speed_test.py https://speedtest.selectel.ru/100MB 10")
        sys.exit(1)
        
    target_url = sys.argv[1]
    num_iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    measure_speed(target_url, num_iterations)