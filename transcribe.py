import customtkinter as ctk
import whisper
from tkinter import filedialog
from pathlib import Path
from datetime import datetime
import threading

ctk.set_appearance_mode("System")  # "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # можно blue, green, dark-blue и др.

class WhisperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎙 Whisper Транскрибация")
        self.geometry("500x300")
        self.resizable(False, False)

        self.model_name = ctk.StringVar(value="base")
        self.file_path = None

        self.create_widgets()

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="Выбор модели Whisper", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title.pack(pady=10)

        self.model_option = ctk.CTkOptionMenu(
            self, values=["tiny", "base", "small", "medium", "large"],
            variable=self.model_name
        )
        self.model_option.pack(pady=10)

        self.button_select = ctk.CTkButton(self, text="📂 Выбрать аудио файл", command=self.select_file)
        self.button_select.pack(pady=10)

        self.label_status = ctk.CTkLabel(self, text="Файл не выбран", wraplength=400)
        self.label_status.pack(pady=10)

        self.button_transcribe = ctk.CTkButton(self, text="🚀 Начать транскрибацию", command=self.start_transcription)
        self.button_transcribe.pack(pady=10)

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Выберите аудио файл",
            filetypes=[("Аудио файлы", "*.mp3 *.wav *.m4a *.flac *.ogg"), ("Все файлы", "*.*")]
        )
        if path:
            self.file_path = Path(path)
            self.label_status.configure(text=f"Выбран файл: {self.file_path.name}")
        else:
            self.label_status.configure(text="Файл не выбран")

    def start_transcription(self):
        if not self.file_path:
            self.label_status.configure(text="⚠️ Сначала выберите аудио файл")
            return

        self.label_status.configure(text="🔄 Транскрибация началась...")

        # отдельный поток, чтобы GUI не завис
        thread = threading.Thread(target=self.transcribe_audio)
        thread.start()

    def transcribe_audio(self):
        try:
            model = whisper.load_model(self.model_name.get())
            result = model.transcribe(str(self.file_path))

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            plain_txt = self.file_path.parent / f"{self.file_path.stem}_{timestamp}_transcription.txt"
            with open(plain_txt, "w", encoding="utf-8") as f:
                f.write(result["text"])

            with_timestamps = self.file_path.parent / f"{self.file_path.stem}_{timestamp}_with_timestamps.txt"
            with open(with_timestamps, "w", encoding="utf-8") as f:
                for segment in result.get("segments", []):
                    f.write(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}\n")

            self.label_status.configure(text=f"✅ Готово!\nСохранено:\n{plain_txt.name}\n{with_timestamps.name}")
        except Exception as e:
            self.label_status.configure(text=f"❌ Ошибка: {e}")

if __name__ == "__main__":
    app = WhisperApp()
    app.mainloop()
