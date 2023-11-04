import streamlit as st

def horizontal_radio(options, key):
    cols = st.columns(len(options))  # Create a column for each option
    selected_option = st.session_state.get(key, None)  # Retrieve the current selection from the session state

    # Iterate over each option and column pair
    for i, (option, col) in enumerate(zip(options, cols)):
        with col:
            # Check if this option is the currently selected one
            is_selected = (option == selected_option)
            
            # Style for selected button
            if is_selected:
                st.button(option, key=f"{key}_{i}", help="Selected")  # The help text can indicate the button's state
            else:
                # Style for non-selected button
                if st.button(option, key=f"{key}_{i}"):
                    selected_option = option  # Update the selected option in the session state
                    st.session_state[key] = selected_option  # Save the current selection

    return selected_option


def vertical_radio(options, key):
    selected_option = st.session_state.get(key, None)  # Retrieve the current selection from the session state

    # Iterate over each option
    for i, option in enumerate(options):
        # Check if this option is the currently selected one
        is_selected = (option == selected_option)
        
        # Style for selected button
        if is_selected:
            st.button(option, key=f"{key}_{i}", help="Selected", disabled=True)  # Disabled for visual cue
        else:
            # Style for non-selected button
            if st.button(option, key=f"{key}_{i}"):
                selected_option = option  # Update the selected option in the session state
                st.session_state[key] = selected_option  # Save the current selection

    return selected_option