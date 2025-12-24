import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
import os
import re
from datetime import datetime

# --- ФУНКЦИЯ: Очистка имени файла ---
def clean_filename(text):
    # Убираем http, https, www чтобы имя файла было короче
    text = text.replace("https://", "").replace("http://", "").replace("www.", "")
    # Заменяем все странные символы на нижнее подчеркивание
    slug = re.sub(r'[^a-zA-Z0-9а-яА-Я]', '_', text)
    # Обрезаем, чтобы имя не было бесконечным (макс 40 символов)
    return slug[:40]

# --- ФУНКЦИЯ: Генерация кодов ---
def start_generation():
    # 1. Получаем текст из поля ввода
    raw_text = text_area.get("1.0", tk.END)
    
    # 2. Разбиваем текст на отдельные строки и убираем пустые
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

    if not lines:
        messagebox.showwarning("Ошибка", "Вы не ввели ни одной ссылки!")
        return

    # 3. Спрашиваем, куда сохранить
    folder_selected = filedialog.askdirectory(title="Выберите папку для сохранения картинок")
    if not folder_selected:
        return # Если пользователь нажал Отмена

    # 4. Создаем папку с текущей датой внутри выбранной папки
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = os.path.join(folder_selected, f"QR_Result_{timestamp}")
    os.makedirs(save_path, exist_ok=True)

    # 5. Запускаем цикл по всем ссылкам
    count = 0
    qr_tool = qrcode.QRCode(box_size=10, border=4) # Настройки QR

    for i, url in enumerate(lines):
        try:
            # Очищаем инструмент перед новым кодом
            qr_tool.clear()
            qr_tool.add_data(url)
            qr_tool.make(fit=True)
            
            # Создаем картинку (черный код на белом фоне)
            img = qr_tool.make_image(fill_color="black", back_color="white")

            # Придумываем имя файла: 001_google_com.png
            safe_name = clean_filename(url)
            filename = f"{i+1:03d}_{safe_name}.png"
            full_path = os.path.join(save_path, filename)
            
            # Сохраняем
            img.save(full_path)
            count += 1
        except Exception as e:
            print(f"Не удалось создать QR для {url}: {e}")

    # 6. Сообщаем об успехе
    status_label.config(text=f"Готово! Создано файлов: {count}")
    messagebox.showinfo("Успех", f"Готово!\nВаши QR-коды лежат в папке:\n{save_path}")

# --- НАСТРОЙКА ИНТЕРФЕЙСА (ОКНА) ---
root = tk.Tk()
root.title("Генератор QR")
root.geometry("500x450")

# Надпись
lbl = tk.Label(root, text="Вставьте список ссылок (каждая с новой строки):", font=("Arial", 11))
lbl.pack(pady=10)

# Поле для ввода (Text Area)
text_area = tk.Text(root, height=15, width=50)
text_area.pack(padx=10)

# Кнопка
btn = tk.Button(root, text="Сгенерировать и Сохранить", command=start_generation, 
                bg="#28a745", fg="white", font=("Arial", 12, "bold"))
btn.pack(pady=15)

# Статус внизу
status_label = tk.Label(root, text="Ожидание...", fg="gray")
status_label.pack()

# Запуск окна
root.mainloop()