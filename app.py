import streamlit as st
import json
import os

file = "notes.json"

def load_notes():
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_notes(notes):
    with open(file, "w") as f:
        json.dump(notes, f, indent=4)

st.title("📝 Notes Taker")

notes = load_notes()
tags = ["personal", "important", "urgent"]

# Add new note
note_header = st.text_input("Header of note")
note_input = st.text_area("Enter your note")
custom_tag = st.text_input("Add a new custom tag (optional)")

if custom_tag and custom_tag not in tags:
    tags.append(custom_tag)

tag = st.multiselect("Choose a tag!", list(tags))

if st.button("Add Note"):
    if note_header and note_input:
        notes[note_header] = {
            "content": note_input,
            "tag": tag  # ✅ correct type (list of strings)
        }
        save_notes(notes)
        st.success(f"Note '{note_header}' added successfully!")
    else:
        st.warning("Please fill both fields.")

# Show all notes
st.markdown("### 📚 Your Notes")

if notes:
    for header, content in notes.items():
        with st.expander(header):
            st.write("✍️", content["content"])
            st.write("🏷️ Tags:", ", ".join(content["tag"]))
else:
    st.info("No notes yet. Add some above!")

# Edit mode
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if st.button("Edit a task"):
    st.session_state.edit_mode = True

if st.session_state.edit_mode:
    edit_header = st.selectbox("Choose a note to edit", list(notes.keys()))
    new_data = st.text_area("Edit the content below:", value=notes[edit_header]["content"])
    if st.button("Update Note"):
        notes[edit_header]["content"] = new_data
        save_notes(notes)
        st.success(f"Note '{edit_header}' updated successfully!")
        st.session_state.edit_mode = False

# Delete mode
if "delete_mode" not in st.session_state:
    st.session_state.delete_mode = False

if st.button("Delete a task"):
    st.session_state.delete_mode = True

if st.session_state.delete_mode:
    delete_header = st.selectbox("Choose the header to delete", list(notes.keys()))
    st.text_area("Content:", value=notes[delete_header]["content"])
    if st.button("Confirm deletion"):
        notes.pop(delete_header)
        save_notes(notes)
        st.success(f"Note deleted successfully!")
        st.session_state.delete_mode = False
