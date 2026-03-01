import streamlit as st
import Semantic as sem
import Chatbot as chat
import CBR as cbr
import Map as mp

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Project Hub | Daniela", 
    page_icon="🌸", 
    layout="wide"
)

# --- Custom Pink Aesthetic (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5; }
    section[data-testid="stSidebar"] { background-color: #FFDBE5 !important; }
    h1, h2, h3 { color: #D02A77 !important; font-family: 'Segoe UI', sans-serif; }
    .stButton>button {
        width: 100%; border-radius: 25px; height: 3em;
        background-color: #FFB6C1; color: white; border: 2px solid #FFC1CC;
        font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #FF69B4; color: white; }
    .result-card {
        background-color: #FFDBE5; padding: 20px; border-radius: 15px;
        border: 2px solid #FFC1CC; color: #4B0082; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🌸 Daniela's AI Hub")
st.sidebar.markdown("---")
choice = st.sidebar.radio(
    "Navigation Menu:",
    ["Home", "Semantic Network", "AI Medical Chatbot", "Game Recommender (CBR)", "Maze Pathfinder"]
)
st.sidebar.markdown("---")
st.sidebar.write("📍 **Lawrence Tech University**")

# --- NAVIGATION LOGIC ---

if choice == "Home":
    st.title("🚀 Artificial Intelligence Portfolio")
    st.subheader("Welcome to Daniela's AI Project Hub!")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        This dashboard unifies the AI modules developed for your LTU coursework:
        * **Semantic Network:** Exploring knowledge representation and inheritance.
        * **Medical Chatbot:** A conversational interface for hospital appointments.
        * **CBR:** Finding solutions based on historical cases.
        * **Pathfinder:** BFS algorithm with 8-direction movement and multiple goals.
        """)
    with col2:
        st.image("https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=400", caption="Exploring AI Solutions")
elif choice == "Semantic Network":
    st.header("🧠 Knowledge Graph Explorer")
    st.write("Visualize how concepts are connected in your Semantic Network.")

    # --- NUEVA PARTE VISUAL ---
    with st.expander("🌐 View Full Knowledge Graph", expanded=True):
        dot_data = sem.get_graphviz_data()
        st.graphviz_chart(dot_data)
    
    st.markdown("---")
    
    # Mantener la parte de análisis detallado por nodo
    nodes = sem.get_options()
    selected = st.selectbox("Select a concept for detailed analysis:", nodes)
    
    if st.button("Analyze Properties"):
        results = sem.get_all_properties(selected)
        if results:
            st.markdown(f"### Results for **{selected}**")
            cols = st.columns(len(results))
            for i, (rel, values) in enumerate(results.items()):
                with cols[i % len(cols)]:
                    st.markdown(f'<div class="result-card"><small>{rel.upper()}</small><br><b>{", ".join(values)}</b></div>', unsafe_allow_html=True)

elif choice == "AI Medical Chatbot":
    st.header("🏥 Hospital AI Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your AI assistant. What is your full name to start?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        num_msgs = len(st.session_state.messages)
        with st.chat_message("assistant"):
            if num_msgs == 2:
                response = f"Nice to meet you, {prompt}. Which department do you need? (Pediatrics, Cardiology, Dentistry)"
            elif num_msgs == 4:
                response = "Understood. How urgent is your case? (1: Low, 2: Medium, 3: High)"
            elif num_msgs == 6:
                response = "Got it. Finally, do you prefer a Morning, Afternoon, or Evening shift?"
            else:
                response = "✨ Your appointment has been successfully scheduled! Is there anything else you need?"
                st.balloons()
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif choice == "Game Recommender (CBR)":
    st.header("🎮 Game Matchmaker")
    c1, c2, c3 = st.columns(3)
    with c1: act = st.slider("Action Level", 0, 10, 5)
    with c2: exp = st.slider("Exploration Level", 0, 10, 5)
    with c3: diff = st.slider("Difficulty Level", 0, 10, 5)
    
    if st.button("🔍 Find My Game"):
        match = cbr.find_best_case(act, exp, diff)
        st.balloons()
        st.markdown(f'<div class="result-card"><h2>🏆 Recommendation: {match["name"]}</h2><p><b>Genre:</b> {match["genre"]}</p></div>', unsafe_allow_html=True)

elif choice == "Maze Pathfinder":
    st.header("🗺️ 15x15 Matrix Pathfinder")
    st.write("Using BFS with 8 directions to find the closest goal.")

    # Get coordinate options from your explicit matrix
    options = mp.get_available_coords(mp.maze_15x15)

    st.subheader("Configuration")
    c1, c2, c3 = st.columns(3)
    with c1:
        start_str = st.selectbox("Start Point:", options, index=0)
    with c2:
        goal1_str = st.selectbox("Goal 1:", options, index=len(options)-1)
    with c3:
        goal2_str = st.selectbox("Goal 2:", options, index=len(options)-20)

    start_pos = eval(start_str)
    user_goals = [eval(goal1_str), eval(goal2_str)]

    if st.button("🚀 Find Path"):
        path = mp.bfs_pathfinder(mp.maze_15x15, start_pos, user_goals)
        
        if path:
            st.success(f"Success! Reached {path[-1]} in {len(path)} steps.")
            # Standard View
            img = mp.draw_fancy_maze(mp.maze_15x15, path, start_pos, user_goals)
            st.image(img, use_container_width=True) # Updated to container width
            st.balloons()
        else:
            st.error("No reachable path found.")