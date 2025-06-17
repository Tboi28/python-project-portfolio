import streamlit as st
import random
import time

# Title
st.title("🪙 Coin Flip Simulator with History")

# Spinning GIF URL
SPIN_GIF = "https://media.tenor.com/Ug6o1EYhU0IAAAAC/coin-flip.gif"
HEADS_IMG = "https://upload.wikimedia.org/wikipedia/commons/1/1f/2006_Quarter_Proof.png"
TAILS_IMG = "https://upload.wikimedia.org/wikipedia/commons/6/60/US_Quarter_Reverse_Proof.png"

# Initialize session state if not set
if 'history' not in st.session_state:
    st.session_state.history = []

# Flip button
if st.button("Flip the Coin"):
    # Show spinning animation
    with st.spinner("Flipping..."):
        st.image(SPIN_GIF, width=200)
        time.sleep(2)

    # Perform the flip
    result = random.choice(['Heads', 'Tails'])
    st.session_state.history.append(result)

    # Show result
    st.subheader(f"🪙 It's {result}!")
    st.image(HEADS_IMG if result == 'Heads' else TAILS_IMG, width=200)

# Display flip history
if st.session_state.history:
    st.markdown("---")
    st.subheader("📊 Flip History & Counts")

    heads_count = st.session_state.history.count('Heads')
    tails_count = st.session_state.history.count('Tails')

    st.write(f"Total Flips: {len(st.session_state.history)}")
    st.write(f"Heads: {heads_count}")
    st.write(f"Tails: {tails_count}")

    # Bar chart
    st.bar_chart({
        "Result": {
            "Heads": heads_count,
            "Tails": tails_count
        }
    })

    # Option to clear history
    if st.button("🔄 Reset History"):
        st.session_state.history = []
        st.experimental_rerun()
