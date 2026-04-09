"""
Модуль сканирования штрих-кодов через RTSP-поток с мобильного устройства
"""

import cv2
import os
from pyzbar import pyzbar
from PIL import Image
import webbrowser
import time

# НАСТРОЙКИ ПОДКЛЮЧЕНИЯ
STREAM_ADDRESS = 'rtsp://adm:1q2w3e4r@192.168.0.3:8080/h264_pcm.sdp'
SCAN_INTERVAL = 3           # Интервал между обработкой одинаковых кодов (сек)
RECONNECT_LIMIT = 5         # Лимит попыток восстановления соединения


def setup_video_stream(stream_url, max_retries=RECONNECT_LIMIT):
    """
    Подключение к видеопотоку с механизмом повторных попыток
    Возвращает объект VideoCapture или None при неудаче
    """
    for attempt in range(1, max_retries + 1):
        print(f"[{attempt}/{max_retries}] Устанавливаю соединение с камерой...")
        camera = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
        time.sleep(2)  # Ожидание инициализации потока
        
        if camera.isOpened():
            print("Соединение с видеопотоком установлено")
            return camera
        else:
            camera.release()
            print("Ошибка подключения. Проверьте:")
            print(f"  • Адрес потока: {stream_url}")
            print("  • Оба устройства в одной сети Wi-Fi")
            print("  • Трансляция активна на смартфоне")
            if attempt < max_retries:
                print(f"  • Повторная попытка через 3 сек...\n")
                time.sleep(3)
    return None


def process_detected_code(code_value, code_format, prev_code, last_scan_ts):
    """
    Обработка распознанного штрих-кода с защитой от дублей
    Возвращает обновлённые значения последних данных и времени
    """
    current_ts = time.time()
    
    if code_value and code_value != prev_code:
        if current_ts - last_scan_ts >= SCAN_INTERVAL:
            print(f"\n Найдено совпадение!")
            print(f"  Артикул: {code_value}")
            print(f"  Формат: {code_format}")
            print("   " + "─" * 40)
            
            # Формируем ссылку для поиска информации о товаре
            product_link = f"https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode={code_value}"
            print(f"  Переход: {product_link[:55]}...")
            
            webbrowser.open(product_link, new=2)
            
            return code_value, current_ts
    return prev_code, last_scan_ts


def run_barcode_scanner():
    """Основной цикл работы сканера штрих-кодов"""
    
    # Инициализация видеопотока
    video_capture = setup_video_stream(STREAM_ADDRESS)
    if not video_capture:
        print("\n Критическая ошибка: не удалось подключиться к источнику видео")
        return
    
    print(" Сканер активен. Для завершения нажмите ESC")
    
    # Состояние для отслеживания дубликатов
    previous_code = ""
    last_scan_timestamp = 0
    
    try:
        while True:
            success, current_frame = video_capture.read()
            if not success:
                print(" Потеря сигнала. Попытка восстановления...")
                video_capture.release()
                time.sleep(1)
                video_capture = setup_video_stream(STREAM_ADDRESS)
                if not video_capture:
                    break
                continue
            
            # Подготовка изображения для распознавания
            rgb_image = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
            
            # Поиск штрих-кодов в кадре
            detected_codes = pyzbar.decode(rgb_image)
            
            for code in detected_codes:
                # Координаты области с кодом
                pos_x, pos_y, width, height = code.rect
                
                # Визуальное выделение зоны распознавания
                cv2.rectangle(current_frame, (pos_x, pos_y), 
                             (pos_x + width, pos_y + height), (0, 255, 0), 2)
                
                # Извлечение данных из кода
                try:
                    code_content = code.data.decode('utf-8')
                    code_kind = code.type
                except UnicodeDecodeError:
                    continue
                
                # Обработка с фильтрацией дублей
                previous_code, last_scan_timestamp = process_detected_code(
                    code_content, code_kind, previous_code, last_scan_timestamp
                )
                
                # Отображение значения кода на видео
                display_y = max(25, pos_y - 12)
                cv2.putText(current_frame, code_content, (pos_x, display_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Показ обработанного кадра
            cv2.imshow('Сканер кодов [RTSP]', current_frame)
            
            # Обработка команды выхода
            if cv2.waitKey(1) & 0xFF == 27:
                print("\n Завершение работы по команде пользователя")
                break
                
    except KeyboardInterrupt:
        print("\n Прервано сочетанием клавиш Ctrl+C")
    finally:
        # Корректное освобождение ресурсов
        if video_capture:
            video_capture.release()
        cv2.destroyAllWindows()
        print(" Ресурсы освобождены. Работа завершена.")


# Точка входа в программу
if __name__ == "__main__":
    run_barcode_scanner()
