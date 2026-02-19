# 🎬 本地自動字幕產生流程說明

本專案提供一個 **完全本地端、免費** 的影片轉字幕流程：

1. 影片轉音檔
2. 音量統一與音訊前處理
3. 使用 Whisper 產生含時間戳字幕（SRT）

整個流程皆在本機執行，無需 API 費用。

---

# 📦 系統需求

- Windows
- Python 3.11
- FFmpeg
- openai-whisper

---

# 🔧 安裝步驟

## 1️⃣ 建立虛擬環境（Python 3.11）

```bat
py -3.11 -m venv whisper-venv
whisper-venv\Scripts\activate
pip install -U pip
pip install openai-whisper
```

## 2️⃣ 安裝 FFmpeg

建議使用：

```powershell
winget install Gyan.FFmpeg
```

確認是否安裝成功：

```powershell
ffmpeg -version
```

---

🚀 使用流程

整體流程架構

影片 (input.mp4)
   ↓
`audio_preprocess.py`
   ↓
統一音量後的音檔 (input_clean.wav)
   ↓
`auto_caption.py`
   ↓
字幕 (input_clean.srt) + 文字稿 (input_clean.txt)

### 🎧 第一步：音訊前處理（音量統一）

功能：

- 從影片抽取音訊
- 去除低頻雜訊
- 去除高頻雜訊
- 自動放大小聲片段（動態標準化）

執行指令：

```powershell
python audio_preprocess.py "input.mp4" --mono
```

輸出資料夾：

```
out_audio/
    input_raw.wav
    input_clean.wav
```

說明：

- `input_raw.wav`：原始音檔
- `input_clean.wav`：音量統一後音檔（建議用此檔做辨識）

### 📝 第二步：產生字幕與文字稿

執行指令：

```powershell
python auto_caption.py "out_audio\input_clean.wav" --model small --language zh
```

輸出資料夾：

```
out/
    input_clean.txt
    input_clean.srt
```

說明：

- `.txt`：完整文字稿
- `.srt`：含時間戳字幕檔

### 🧠 模型建議

模型	速度	準確度
---	---	---
small	快	良好
medium	中	較佳（中文推薦）
large	慢	最佳

範例：

```powershell
python auto_caption.py "out_audio\input_clean.wav" --model medium --language zh
```

### 🔊 音訊處理策略說明

音訊處理使用：

- `highpass` + `lowpass` + `dynaudnorm`

功能說明：

- `highpass`：去除低頻轟聲
- `lowpass`：去除高頻嘶聲
- `dynaudnorm`：自動放大小聲段落，使整段音量更平均

---

# 📂 專案結構

```
Auto_caption/
│
├── audio_preprocess.py
├── auto_caption.py
├── whisper-venv/
├── out_audio/
└── out/
```
