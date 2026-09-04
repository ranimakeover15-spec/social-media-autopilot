import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path

# UTF-8 Encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = Path(r"D:\Antigravity_Projects\social-media-autopilot")
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_VOICE_FILE = LOGS_DIR / "processed_voice_notes.json"
CLIENT_PROMOS_FILE = BASE_DIR / "content_vault" / "client_custom_promos.json"
CLIENT_PROMOS_FILE.parent.mkdir(parents=True, exist_ok=True)

TELEGRAM_BOT_TOKEN = "8997636217:AAGnU3XP9GgmiS60zitBnxe_4vy99n-F-ug"

class ClientVoiceListener:
    def __init__(self, bot_token: str = TELEGRAM_BOT_TOKEN):
        self.bot_token = bot_token
        self.processed_ids = self._load_processed_ids()

    def _load_processed_ids(self) -> set:
        if PROCESSED_VOICE_FILE.exists():
            try:
                data = json.loads(PROCESSED_VOICE_FILE.read_text(encoding="utf-8"))
                return set(data.get("processed_ids", []))
            except Exception:
                return set()
        return set()

    def _save_processed_id(self, update_id: int):
        self.processed_ids.add(update_id)
        PROCESSED_VOICE_FILE.write_text(
            json.dumps({"processed_ids": list(self.processed_ids), "last_sync": time.strftime("%Y-%m-%d %H:%M:%S")}, indent=2),
            encoding="utf-8"
        )

    def send_telegram_reply(self, chat_id: int, text: str):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": chat_id, "text": text}
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Telegram reply error: {e}")

    def transcribe_audio_file(self, audio_path: Path) -> str:
        wav_path = audio_path.with_suffix(".wav")
        cmd = [
            "ffmpeg", "-y", "-i", str(audio_path),
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
            str(wav_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not wav_path.exists():
            print(f"FFmpeg conversion error: {res.stderr}")
            return ""

        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.AudioFile(str(wav_path)) as source:
                audio_data = r.record(source)
            
            try:
                text_hi = r.recognize_google(audio_data, language="hi-IN")
                print(f"Hindi Transcription: \"{text_hi}\"")
                return text_hi
            except Exception:
                try:
                    text_en = r.recognize_google(audio_data, language="en-IN")
                    print(f"English Transcription: \"{text_en}\"")
                    return text_en
                except Exception:
                    return ""
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return ""
        finally:
            if wav_path.exists():
                try: wav_path.unlink()
                except Exception: pass

    def apply_client_instructions(self, transcript: str, sender_name: str, chat_id: int) -> dict:
        t_lower = transcript.lower()
        applied_changes = []

        promos = {}
        if CLIENT_PROMOS_FILE.exists():
            try:
                promos = json.loads(CLIENT_PROMOS_FILE.read_text(encoding="utf-8"))
            except Exception:
                promos = {}

        import re
        price_match = re.findall(r"(?:₹|rs\.?|rupees|rupaye)?\s*(\d{2,5})", t_lower)
        if any(w in t_lower for w in ["offer", "discount", "price", "rupaye", "hazaar", "rate"]):
            if price_match:
                new_price = price_match[0]
                promos["custom_price_badge"] = f"Special Offer ₹{new_price}"
                applied_changes.append(f"नया स्पेशल ऑफर प्राइस: ₹{new_price}")
            if any(w in t_lower for w in ["%", "percent", "pratishat", "off"]):
                pct_match = re.findall(r"(\d{1,2})\s*(?:%|percent)", t_lower)
                if pct_match:
                    promos["custom_discount_badge"] = f"{pct_match[0]}% OFF Special Discount"
                    applied_changes.append(f"डिस्काउंट बैज: {pct_match[0]}% OFF")

        if any(w in t_lower for w in ["haircut", "hair cut", "bal", "cutting"]):
            promos["primary_focus"] = "HAIRCUT & HAIR STYLING"
            applied_changes.append("मुख्य सर्विस फोकस: Trendy Haircut & Styling")
        elif any(w in t_lower for w in ["bridal", "dulhan", "shaadi", "bride"]):
            promos["primary_focus"] = "ROYAL BRIDAL MAKEUP"
            applied_changes.append("मुख्य सर्विस फोकस: Royal Bridal Makeup")
        elif any(w in t_lower for w in ["hydra", "facial", "glow", "skin"]):
            promos["primary_focus"] = "HYDRA FACIAL & GLOW"
            applied_changes.append("मुख्य सर्विस फोकस: Hydra Facial & Instant Glow")
        elif any(w in t_lower for w in ["threading", "upper lips", "forehead", "eyebrow"]):
            promos["primary_focus"] = "PERFECT THREADING & SHAPING"
            applied_changes.append("मुख्य सर्विस फोकस: Perfect Threading, Forehead & Upper Lips")

        promos["latest_transcript"] = transcript
        promos["updated_by"] = sender_name
        promos["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        if applied_changes:
            promos["active_custom_changes"] = applied_changes

        CLIENT_PROMOS_FILE.write_text(json.dumps(promos, indent=2, ensure_ascii=False), encoding="utf-8")

        changes_summary = "\n".join([f"• {c}" for c in applied_changes]) if applied_changes else "• आपके सामान्य निर्देश सिस्टम में दर्ज कर लिए गए हैं।"
        
        reply_msg = (
            f"👑 Rani Makeover AI Autopilot\n\n"
            f"🙏 नमस्ते {sender_name} जी! आपका वॉइस संदेश सुन लिया गया है:\n\n"
            f"🎙️ आपने कहा: \"{transcript}\"\n\n"
            f"✅ सिस्टम में अपडेट किए गए बदलाव:\n{changes_summary}\n\n"
            f"🎬 अगले वीडियो पोस्ट (YouTube Shorts & Instagram Reels) में यह बदलाव ऑटोमैटिक लागू हो जाएंगे!"
        )

        self.send_telegram_reply(chat_id, reply_msg)
        return {"transcript": transcript, "changes": applied_changes}

    def check_and_process_all_voice_notes(self):
        print("=" * 70)
        print("🎧 SCANNING TELEGRAM BOT FOR CLIENT VOICE NOTES & INSTRUCTIONS")
        print("=" * 70)

        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates?limit=50"
        try:
            res = requests.get(url, timeout=15).json()
        except Exception as e:
            print(f"Failed to reach Telegram Bot: {e}")
            return []

        if not res.get("ok"):
            print("Telegram API returned error:", res)
            return []

        updates = res.get("result", [])
        processed_count = 0

        for upd in updates:
            upd_id = upd.get("update_id")
            if upd_id in self.processed_ids:
                continue

            msg = upd.get("message", {})
            sender = msg.get("from", {}).get("first_name", "Client")
            chat_id = msg.get("chat", {}).get("id")
            
            voice = msg.get("voice")
            audio = msg.get("audio")
            text = msg.get("text")

            if voice or audio:
                f_obj = voice or audio
                file_id = f_obj.get("file_id")
                print(f"Found New Voice Note from {sender} (Chat ID: {chat_id}, Duration: {f_obj.get('duration')}s)")

                f_info = requests.get(f"https://api.telegram.org/bot{self.bot_token}/getFile?file_id={file_id}", timeout=10).json()
                if f_info.get("ok"):
                    file_path_rel = f_info["result"]["file_path"]
                    dl_url = f"https://api.telegram.org/file/bot{self.bot_token}/{file_path_rel}"
                    local_voice = TEMP_DIR / f"voice_{upd_id}.oga"

                    r_dl = requests.get(dl_url, timeout=30)
                    local_voice.write_bytes(r_dl.content)
                    print(f"Downloaded voice note: {local_voice.name}")

                    transcript = self.transcribe_audio_file(local_voice)
                    if transcript:
                        result = self.apply_client_instructions(transcript, sender, chat_id)
                        print(f"Successfully processed & replied to {sender}: {result}")
                    else:
                        print("Could not transcribe voice note")
                        self.send_telegram_reply(
                            chat_id,
                            f"🙏 नमस्ते {sender} जी! आपका वॉइस नोट प्राप्त हुआ। क्या आप इसे थोड़ा स्पष्ट बोलकर दोबारा भेज सकते हैं या लिखकर बता सकते हैं?"
                        )

                    if local_voice.exists():
                        try: local_voice.unlink()
                        except Exception: pass

                self._save_processed_id(upd_id)
                processed_count += 1

            elif text and not text.startswith("/start"):
                t_lower = text.lower()
                keywords = ["price", "offer", "haircut", "facial", "bridal", "change", "badal", "discount", "service"]
                if any(kw in t_lower for kw in keywords):
                    print(f"Found Text Instruction from {sender}: \"{text}\"")
                    result = self.apply_client_instructions(text, sender, chat_id)
                    print(f"Processed text instruction: {result}")
                    self._save_processed_id(upd_id)
                    processed_count += 1

        print(f"Voice & Instruction scan completed. Processed: {processed_count} item(s).")
        return processed_count

if __name__ == "__main__":
    listener = ClientVoiceListener()
    listener.check_and_process_all_voice_notes()
