import streamlit as st 
import json 
import os 

file  = "notes.json"

def load_notes():
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # If file is empty or broken
    return {}  # file doesn't exist


def save_notes(notes):
    with open(file, "w") as f:
        json.dump(notes, f, indent=4)

st.title("📝 Notes Taker")

# Load existing notes
notes = load_notes()
tags = ["personal","important","urgent"]

note_header = st.text_input("Header of note")
note_input = st.text_area("Enter your note")
tag = st.multiselect("Choose a tag!",list(tags))



if st.button("Add Note"):
    if note_header and note_input:
        notes[note_header] = {
            "content" : note_input,
            "tag" : [tags]
        }
        save_notes(notes)
        st.success(f"Note '{note_header}' added successfully!")
    else:
        st.warning("Please fill both fields.")

# implementing the search feature. 

# search  = st.text_input(" ## Search the task",placeholder="Ex. Shopping List")
# if search == "":
#     st.info("Search the keyword above to find your task!")
# else :
#     for header in notes:




st.markdown("### 📚 Your Notes")

if notes:
    for header, content in notes.items():
        with st.expander(header):
            st.write(content)
else:
    st.info("No notes yet. Add some above!")

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

edit = st.button("Edit a task")
if edit:
    st.session_state.edit_mode= True

if st.session_state.edit_mode:
    edit_header = st.selectbox("Choose: ", list(notes.keys()))
    
    new_data = st.text_area("Edit the content below:", value=notes[edit_header])
    if st.button("Update Note"):
        notes[edit_header] = new_data
        save_notes(notes)
        st.success(f"Note '{edit_header}' updated successfully!")
        st.session_state.edit_mode = False
            

if "delete_mode" not in st.session_state:
    st.session_state.delete_mode = False

delete = st.button("Delete a task")
if delete:
    st.session_state.delete_mode = True 

if st.session_state.delete_mode:
    
    delete_header = st.selectbox("Choose the header: ",list(notes.keys()))
    st.text_area("Content in the above file is: ",value = notes[delete_header])
    deletebutton = st.button("Confirm deletion")
    if deletebutton:
        notes.pop(delete_header)
        save_notes(notes)
        st.success(f"Note deleted successfully!")
        st.session_state.delete_mode = False 
            
               
