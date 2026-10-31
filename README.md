# Typing Speed and Accuracy Analyzer

A Python-based web application built using **Streamlit** that measures typing speed, accuracy, and typing performance over time.

The application allows users to take typing tests at different difficulty levels, analyze their mistakes, and track their improvement through performance tables and graphs.

## Features

- **Multiple Difficulty Levels:** Choose between Easy, Medium, and Hard typing tests.
- **Random Passages:** Generate random sentences for typing practice.
- **Typing Speed Calculation:** Calculate typing speed in Words Per Minute (WPM).
- **Accuracy Measurement:** Calculate typing accuracy as a percentage.
- **Character Analysis:** Identify correct, incorrect, missing, and extra characters.
- **Accuracy Analysis Table:** View a detailed breakdown of typing performance.
- **Performance Tracking:** Save previous typing test results automatically.
- **Personal Best:** Track your highest typing speed and accuracy.
- **Performance Graphs:** Visualize typing speed and accuracy trends over multiple attempts.
- **Difficulty-wise Analysis:** Compare average accuracy and typing speed across difficulty levels.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| SQLite | Store typing test history |
| Pandas | Data processing and analysis |
| Matplotlib / Streamlit Charts | Performance visualization |
| Random | Random passage selection |

## Project Structure

```text
Typing-Speed-Analyzer/
│
├── app.py
├── typing_results.db
├── requirements.txt
└── README.md
```

**Note:** `typing_results.db` is automatically created when the application runs for the first time. It does not need to be uploaded to GitHub.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Typing-Speed-Analyzer.git
```

### 2. Navigate to the Project Folder

```bash
cd Typing-Speed-Analyzer
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Alternatively:

```bash
pip install streamlit pandas
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser.

## How It Works

1. Select a difficulty level: Easy, Medium, or Hard.
2. Choose a sentence or select a random passage.
3. Click **Start New Test**.
4. Type the displayed passage in the typing area.
5. Click **Submit Test** to calculate your results.
6. View your WPM, accuracy, and character analysis.
7. Check your performance history and graphs to monitor improvement.

## Performance Calculations

**1. Words Per Minute (WPM)**

The typing speed is calculated using the standard five-characters-per-word convention.

\[
WPM = \frac{\text{Characters Typed}/5}{\text{Time in Minutes}}
\]

**2. Typing Accuracy**

\[
Accuracy = \frac{\text{Correct Characters}}{\text{Total Passage Characters}}\times100
\]

**3. Character Analysis**

The application tracks:
- Correct characters
- Incorrect characters
- Missing characters
- Extra characters

## Database

The application uses SQLite to store typing test results.

The database records:
- Test date and time
- Difficulty level
- Typing passage
- Time taken
- Typing speed (WPM)
- Accuracy percentage
- Correct characters
- Incorrect characters
- Missing characters
- Extra characters

This allows users to review previous attempts and track their progress across multiple sessions.

## Project Objective

The main objective of this project is to develop an interactive typing analysis system that helps users improve their typing speed and accuracy.

By combining real-time typing tests, database integration, data analysis, and graphical visualization, the application provides a simple way to measure and monitor typing performance.

## Developed Using

**Python | Streamlit | SQLite | Pandas**

