# Guitar Practice Routine Processor

A utility to process guitar practice routines from images or manual input into structured JSON format.

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract OCR (for image processing):
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

## Usage

### Manual Entry
```bash
python routine_processor.py manual
```

**Continuous Entry Mode**: The manual entry now runs in continuous mode, allowing you to add multiple routines in one session:
- After adding each routine, you can immediately start entering the next one
- Type 'q' or 'quit' at any prompt to exit
- Press Ctrl+C to quit at any time
- State defaults to "not_completed" if you just press Enter

### Image Processing
```bash
python routine_processor.py image path/to/image.jpg
```

### Custom JSON File
```bash
python routine_processor.py --json-file my_routines.json manual
```

## JSON Structure

The app generates JSON in this format:
```json
[
  {
    "text": "Practice major scales",
    "category": "daily",
    "tags": ["scales", "technique"],
    "state": "not_completed"
  }
]
```

### Categories
- `daily`: Daily practice routines
- `one_day`: One-time practice items
- `two_three_days`: Multi-day practice goals
- `one_week`: Weekly practice objectives

### States
- `not_completed`: Not yet practiced
- `in_progress`: Currently working on
- `completed`: Finished practicing

## Features

- **Continuous Manual Entry**: Add multiple routines in one session with easy exit options
- **Smart Defaults**: State defaults to "not_completed" for faster entry
- **Append Mode**: If JSON file exists, new routines are appended
- **Create Mode**: If JSON file doesn't exist, creates new file
- **OCR Processing**: Extracts text from images using Tesseract
- **Auto-categorization**: Basic keyword-based categorization
- **Tag Extraction**: Automatically generates relevant tags