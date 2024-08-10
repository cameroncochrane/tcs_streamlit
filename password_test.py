import streamlit as st

# Set the correct password
correct_password = "hello"

# Function to check the password
def check_password():
    st.session_state["password_correct"] = st.session_state["password"] == correct_password

def input_password():
    st.text_input("Enter the password", type="password", on_change=check_password, key="password")
    st.button("Submit")
    # Ask the user for the password


# Input for the password
if "password_correct" not in st.session_state:
    # Ask the user for the password
    input_password()
else:
    # Check if the password is correct
    if st.session_state["password_correct"]:
        st.write("Welcome")
        
    else:
        st.write("Incorrect password.")
        # Optionally, clear the incorrect password input
        st.session_state.pop("password_correct")
        input_password()

