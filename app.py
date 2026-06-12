import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "journal_entries.json"

# ----------------------------
# Load Entries
# ----------------------------
def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# ----------------------------
# Save Entries
# ----------------------------
def save_entries(entries):
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=4)

entries = load_entries()

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="StoryLeaf",
    page_icon="📖",
    layout="wide"
)

st.title("📖 StoryLeaf")
st.markdown("Capture memories, thoughts, and daily reflections.")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Add Entry",
        "View Entries",
        "Search Entries",
        "Statistics"
    ]
)

# ==================================================
# ADD ENTRY
# ==================================================
if menu == "Add Entry":

    st.header("✍️ New Journal Entry")

    title = st.text_input("Title")

    mood = st.selectbox(
        "Mood",
        [
            "😊 Happy",
            "😌 Calm",
            "😐 Neutral",
            "😔 Sad",
            "😡 Angry",
            "😴 Tired"
        ]
    )

    journal_text = st.text_area(
        "Write your thoughts",
        height=250
    )

    if st.button("Save Entry"):

        if title.strip() == "" or journal_text.strip() == "":
            st.error("Title and Journal Entry are required.")
        else:

            new_entry = {
                "id": len(entries) + 1,
                "title": title,
                "mood": mood,
                "content": journal_text,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            entries.append(new_entry)
            save_entries(entries)

            st.success("Journal entry saved successfully!")

# ==================================================
# VIEW ENTRIES
# ==================================================
elif menu == "View Entries":

    st.header("📚 All Journal Entries")

    if not entries:
        st.info("No journal entries found.")

    else:

        entries = sorted(
            entries,
            key=lambda x: x["date"],
            reverse=True
        )

        for entry in entries:

            with st.expander(
                f"{entry['title']} | {entry['date']}"
            ):

                st.write(f"**Mood:** {entry['mood']}")
                st.write(entry["content"])

                if st.button(
                    f"Delete Entry {entry['id']}",
                    key=entry["id"]
                ):
                    updated = [
                        e for e in load_entries()
                        if e["id"] != entry["id"]
                    ]

                    save_entries(updated)
                    st.success("Entry deleted.")
                    st.rerun()

# ==================================================
# SEARCH
# ==================================================
elif menu == "Search Entries":

    st.header("🔍 Search Journal Entries")

    keyword = st.text_input(
        "Search by title or content"
    )

    if keyword:

        results = []

        for entry in entries:

            if (
                keyword.lower() in entry["title"].lower()
                or keyword.lower() in entry["content"].lower()
            ):
                results.append(entry)

        st.subheader(
            f"Results Found: {len(results)}"
        )

        for entry in results:

            with st.expander(
                f"{entry['title']} | {entry['date']}"
            ):
                st.write(f"**Mood:** {entry['mood']}")
                st.write(entry["content"])

# ==================================================
# STATISTICS
# ==================================================
elif menu == "Statistics":

    st.header("📊 Journal Statistics")

    total_entries = len(entries)

    st.metric(
        "Total Entries",
        total_entries
    )

    if total_entries > 0:

        moods = {}

        for entry in entries:
            mood = entry["mood"]
            moods[mood] = moods.get(mood, 0) + 1

        st.subheader("Mood Distribution")

        st.bar_chart(moods)

        latest = sorted(
            entries,
            key=lambda x: x["date"],
            reverse=True
        )[0]

        st.subheader("Latest Entry")

        st.write(f"**Title:** {latest['title']}")
        st.write(f"**Date:** {latest['date']}")
        st.write(f"**Mood:** {latest['mood']}")

    else:
        st.info("No data available yet.")