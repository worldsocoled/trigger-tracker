# Trigger Tracker

**Trigger Tracker** is a Python-based application designed to help users log and reflect on their personal triggers throughout the day. By capturing details such as the trigger itself, surrounding events, and emotional responses, the app makes it easier to identify patterns and share insights with a therapist.

This project demonstrates practical Python skills, data handling, modular design, and data visualization.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Technologies](#technologies)
- [Future Improvements](#future-improvements)
- [License](#license)
- [Contact](#contact)

## Features

✅ Log triggers in real time with timestamps  
✅ Record context: *what happened before, during, and after*  
✅ Track emotional responses and intensity levels  
✅ View daily/weekly summaries and stats  
✅ Export logs to CSV for therapist review  
✅ Clean, intuitive command-line interface  
✅ Local data storage with privacy in mind

## Demo

```bash
$ python main.py

Welcome to Trigger Tracker!

Enter the trigger: Anxiety at work  
What happened before?: Boss gave unexpected feedback  
What happened after?: Felt overwhelmed, avoided coworkers  
How did you feel?: Stressed, tense  
Intensity (1-10): 7  

Trigger saved at: 2025-09-14 14:32
```

Later, you can generate reports:

```bash
$ python main.py --stats
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/trigger-tracker.git
cd trigger-tracker
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the program:
```bash
python main.py
```

Follow the prompts to log a trigger. Data is stored in `data/triggers.csv`.

To see stats:
```bash
python main.py --stats
```

To export your logs for a therapist:
```bash
python main.py --export
```

## Folder Structure

```
trigger_tracker/
│
├── main.py            # Main CLI program
├── utils/             # Helper modules
│   ├── helpers.py     # Input/output helpers
│   ├── stats.py       # Pattern analysis and reports
│   └── export.py      # CSV export functionality
├── data/              # Stored logs and exported data
├── README.md          # Project documentation
└── requirements.txt   # Dependencies
```

## Technologies

- Python 3.x
- pandas (data handling)
- matplotlib / seaborn (visualization)
- CSV/JSON for storage

## Future Improvements

- Add GUI with Tkinter or PyQt
- Mobile-friendly app for real-time logging
- Encrypted storage for sensitive data
- AI-powered pattern detection & insights

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

📧 **Email:** worldsocoledwebartistry@gmail.com  
💼 **LinkedIn:** [linkedin.com/in/nichole-higgins423](https://www.linkedin.com/in/nichole-higgins423/)

Feel free to reach out for questions, feedback, or collaboration opportunities!
