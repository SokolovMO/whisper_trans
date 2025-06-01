import whisper
from pathlib import Path
from datetime import datetime
import sys

def select_model_interactively():
    models = ["tiny", "base", "small", "medium", "large"]
    print("📦 выбери модель Whisper:\n")
    for i, name in enumerate(models, start=1):
        print(f"{i}. {name}")
    try:
        choice = int(input("\nВведите номер модели (1-5): "))
        if 1 <= choice <= 5:
            return models[choice - 1]
        else:
            print("⚠️ неверный выбор, используется модель по умолчанию: base")
            return "base"
    except:
        print("⚠️ не удалось прочитать выбор, используется модель по умолчанию: base")
        return "base"

def transcribe_audio(file_path: Path, model_name="base"):
    print(f"\n📂 выбранный файл: {file_path}")
    if not file_path.exists():
        print(f"❌ файл не найден: {file_path}")
        return

    try:
        print(f"📦 загружаем модель whisper: {model_name}")
        model = whisper.load_model(model_name)

        print("🧠 начинаем транскрибацию...")
        result = model.transcribe(str(file_path))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("results_transcribe")
        output_dir.mkdir(exist_ok=True)
        output_plain = output_dir / f"{file_path.stem}_{timestamp}_transcription.txt"
        output_timed = output_dir / f"{file_path.stem}_{timestamp}_with_timestamps.txt"
        # output_plain = file_path.with_name(f"{file_path.stem}_{timestamp}_transcription.txt")
        output_timed = file_path.with_name(f"{file_path.stem}_{timestamp}_with_timestamps.txt")

        with open(output_plain, "w", encoding="utf-8") as f:
            f.write(result["text"])

        with open(output_timed, "w", encoding="utf-8") as f:
            for segment in result.get("segments", []):
                f.write(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}\n")

        print(f"✅ транскрибация завершена.\n📝 сохранено:\n- {output_plain.name}\n- {output_timed.name}")

    except Exception as e:
        print(f"❌ ошибка: {e}")

def main():
    args = sys.argv[1:]

    if not args:
        print("❗ перетащи аудиофайл на скрипт, или передай путь в аргументах\n")
        return

    file_path = Path(args[0])

    if len(args) > 1:
        model_name = args[1]
    else:
        model_name = select_model_interactively()

    transcribe_audio(file_path, model_name=model_name)

if __name__ == "__main__":
    main()
