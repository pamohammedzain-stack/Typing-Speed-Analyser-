
import random
import sqlite3
import time
from datetime import datetime
from itertools import zip_longest

import pandas as pd
import streamlit as st

# -------------------- PAGE SETTINGS --------------------

st.set_page_config(
    page_title="Typing Speed Analyzer",
    page_icon="⌨️",
    layout="wide"
)

st.title("Typing Speed and Accuracy Analyzer")
st.write("Measure your typing speed, accuracy, and progress over time.")

# -------------------- PASSAGE LIBRARY --------------------

PASSAGES = {
    "Easy": [
        "The sun rises in the east every morning.",
        "Practice makes a person better at any skill.",
        "I enjoy learning Python and solving problems.",
        "Reading books helps us gain new knowledge.",
        "A good habit can improve our daily life."
    ],
    "Medium": [
        "Programming improves logical thinking and problem solving skills.",
        "Consistency and regular practice are important for learning.",
        "Python is useful for automation, data analysis, and development.",
        "Typing accurately is just as important as typing quickly.",
        "Small improvements every day can produce excellent results."
    ],
    "Hard": [
        "Algorithms, data structures, and debugging are essential programming skills.",
        "Artificial intelligence can analyze information and identify complex patterns.",
        "Efficient software requires careful planning, testing, and optimization.",
        "Accuracy decreases when users prioritize speed without sufficient practice.",
        "Developers should consider reliability, readability, and performance."
    ]
}

DB_NAME = "typing_results.db"

# -------------------- DATABASE --------------------

def create_database():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_date TEXT,
            difficulty TEXT,
            passage TEXT,
            duration REAL,
            wpm REAL,
            accuracy REAL,
            correct_chars INTEGER,
            incorrect_chars INTEGER,
            missing_chars INTEGER,
            extra_chars INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_result(result):
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO results (
            test_date, difficulty, passage, duration, wpm,
            accuracy, correct_chars, incorrect_chars,
            missing_chars, extra_chars
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        result["date"],
        result["difficulty"],
        result["passage"],
        result["duration"],
        result["wpm"],
        result["accuracy"],
        result["correct"],
        result["incorrect"],
        result["missing"],
        result["extra"]
    ))

    conn.commit()
    conn.close()


def load_history():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM results ORDER BY id DESC",
        conn
    )

    conn.close()
    return df


create_database()

# -------------------- SESSION STATE --------------------

if "started_at" not in st.session_state:
    st.session_state.started_at = None

if "active_passage" not in st.session_state:
    st.session_state.active_passage = ""

if "active_difficulty" not in st.session_state:
    st.session_state.active_difficulty = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "test_number" not in st.session_state:
    st.session_state.test_number = 0

# -------------------- TEST SETTINGS --------------------

st.header("1. Choose Your Typing Test")

difficulty = st.selectbox(
    "Select difficulty level",
    ["Easy", "Medium", "Hard"]
)

passage_choice = st.selectbox(
    "Choose a sentence",
    ["Random passage"] + PASSAGES[difficulty]
)

if st.button("Start New Test", type="primary"):
    if passage_choice == "Random passage":
        selected_passage = random.choice(PASSAGES[difficulty])
    else:
        selected_passage = passage_choice

    st.session_state.active_passage = selected_passage
    st.session_state.active_difficulty = difficulty
    st.session_state.started_at = time.time()
    st.session_state.last_result = None
    st.session_state.test_number += 1

    # Clear the previous typing input for the new test.
    st.session_state.pop("typed_text", None)

    st.rerun()

# -------------------- TYPING AREA --------------------

if st.session_state.started_at is not None:
    st.header("2. Type the Passage")

    st.info(
        f"Difficulty: {st.session_state.active_difficulty}"
    )

    st.code(st.session_state.active_passage)

    typed_text = st.text_area(
        "Type the passage exactly as shown above:",
        height=150,
        key="typed_text",
        placeholder="Start typing here..."
    )

    if st.button("Submit Test", type="primary"):
        target = st.session_state.active_passage
        typed = typed_text

        elapsed = max(
            time.time() - st.session_state.started_at,
            0.01
        )

        # Compare characters at matching positions.
        pairs = list(
            zip_longest(target, typed, fillvalue=None)
        )

        correct = sum(
            1 for a, b in pairs
            if a is not None and b is not None and a == b
        )

        incorrect = sum(
            1 for a, b in pairs
            if a is not None and b is not None and a != b
        )

        missing = max(len(target) - len(typed), 0)
        extra = max(len(typed) - len(target), 0)

        # Accuracy is based on correctly typed target characters.
        accuracy = (
            correct / len(target) * 100
            if target else 0
        )

        # Standard WPM uses five typed characters per word.
        wpm = (len(typed) / 5) / (elapsed / 60)

        result = {
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "difficulty": st.session_state.active_difficulty,
            "passage": target,
            "duration": round(elapsed, 2),
            "wpm": round(wpm, 2),
            "accuracy": round(accuracy, 2),
            "correct": correct,
            "incorrect": incorrect,
            "missing": missing,
            "extra": extra
        }

        save_result(result)

        st.session_state.last_result = result
        st.session_state.started_at = None

        # Clear the text input after submission.
        st.session_state.pop("typed_text", None)

        st.rerun()

# -------------------- LATEST RESULT --------------------

if st.session_state.last_result is not None:
    result = st.session_state.last_result

    st.header("3. Your Test Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Typing Speed",
        f'{result["wpm"]} WPM'
    )

    col2.metric(
        "Accuracy",
        f'{result["accuracy"]}%'
    )

    col3.metric(
        "Time Taken",
        f'{result["duration"]} seconds'
    )

    st.subheader("Accuracy Analysis Table")

    accuracy_table = pd.DataFrame({
        "Measurement": [
            "Total passage characters",
            "Characters typed",
            "Correct characters",
            "Incorrect characters",
            "Missing characters",
            "Extra characters",
            "Overall accuracy"
        ],
        "Value": [
            len(result["passage"]),
            len(result["passage"]) - result["missing"] + result["extra"],
            result["correct"],
            result["incorrect"],
            result["missing"],
            result["extra"],
            f'{result["accuracy"]}%'
        ]
    })

    st.dataframe(
        accuracy_table,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Accuracy = correctly typed characters divided by total "
        "passage characters, multiplied by 100. Missing and extra "
        "characters are tracked separately."
    )

    if result["accuracy"] >= 95:
        st.success("Excellent accuracy! Keep practising.")
    elif result["accuracy"] >= 80:
        st.info("Good effort. Practise to improve your accuracy.")
    else:
        st.warning(
            "Focus on typing accurately before increasing your speed."
        )

# -------------------- PERFORMANCE HISTORY --------------------

st.header("4. Performance History")

history = load_history()

if not history.empty:
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Tests Completed",
        len(history)
    )

    col2.metric(
        "Personal Best WPM",
        f'{history["wpm"].max():.2f}'
    )

    col3.metric(
        "Personal Best Accuracy",
        f'{history["accuracy"].max():.2f}%'
    )

    # -------------------- ACCURACY BY DIFFICULTY --------------------

    st.subheader("Accuracy Table by Difficulty")

    accuracy_summary = (
        history.groupby("difficulty")
        .agg(
            Tests=("id", "count"),
            Average_Accuracy=("accuracy", "mean"),
            Best_Accuracy=("accuracy", "max"),
            Average_WPM=("wpm", "mean")
        )
        .reindex(["Easy", "Medium", "Hard"])
        .dropna(how="all")
        .reset_index()
    )

    accuracy_summary = accuracy_summary.rename(columns={
        "difficulty": "Difficulty",
        "Average_Accuracy": "Average Accuracy (%)",
        "Best_Accuracy": "Best Accuracy (%)",
        "Average_WPM": "Average WPM"
    })

    st.dataframe(
        accuracy_summary.round(2),
        use_container_width=True,
        hide_index=True
    )

    # -------------------- PERFORMANCE GRAPHS --------------------

    st.subheader("Performance Trends")

    chart_data = history.sort_values("id").reset_index(drop=True)
    chart_data["Test Number"] = range(1, len(chart_data) + 1)

    tab1, tab2 = st.tabs([
        "Typing Speed Trend",
        "Accuracy Trend"
    ])

    with tab1:
        st.line_chart(
            chart_data.set_index("Test Number")["wpm"],
            y_label="Words Per Minute"
        )

    with tab2:
        st.line_chart(
            chart_data.set_index("Test Number")["accuracy"],
            y_label="Accuracy (%)"
        )

    # -------------------- PREVIOUS ATTEMPTS --------------------

    st.subheader("Previous Test Attempts")

    display_history = history.rename(columns={
        "test_date": "Date",
        "difficulty": "Difficulty",
        "duration": "Duration (seconds)",
        "wpm": "WPM",
        "accuracy": "Accuracy (%)",
        "correct_chars": "Correct",
        "incorrect_chars": "Incorrect",
        "missing_chars": "Missing",
        "extra_chars": "Extra"
    })

    st.dataframe(
        display_history[
            [
                "Date",
                "Difficulty",
                "Duration (seconds)",
                "WPM",
                "Accuracy (%)",
                "Correct",
                "Incorrect",
                "Missing",
                "Extra"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

else:
    st.write(
        "No test history yet. Complete a typing test to see "
        "your accuracy table and performance graphs."
    )

# -------------------- FOOTER --------------------

st.divider()

st.caption(
    "Typing Speed and Accuracy Analyzer | "
    "Python | Streamlit | SQLite | Pandas"
)
