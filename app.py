import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import string
import random
import pandas as pd

# ============================================================
# PAGE CONFIG & SESSION STATE
# ============================================================
st.set_page_config(page_title="RouteXpert AI", layout="wide")

# Initialize session state for traffic if it doesn't exist
if 'init_traffic' not in st.session_state:
    st.session_state.init_traffic = {l: random.randint(2, 18) for l in string.ascii_uppercase}

def randomize_traffic():
    st.session_state.init_traffic = {l: random.randint(2, 18) for l in string.ascii_uppercase}

# ============================================================
# HEADER & SIDEBAR
# ============================================================
st.title("🚦 RouteXpert: Symbolic AI Traffic Management")
st.markdown("An explainable AI (XAI) system featuring **Weighted Priority Scoring** and emergency preemption.")

with st.sidebar:
    st.header("🛠️ Configuration")
    num_intersections = st.slider("Number of Intersections", 2, 10, 5)
    intersections = list(string.ascii_uppercase[:num_intersections])
    
    if st.button("🔀 Randomize Initial Traffic"):
        randomize_traffic()
    
    st.subheader("Manual Traffic Input")
    traffic_input = {}
    for n in intersections:
        traffic_input[n] = st.number_input(f"Traffic at {n}", 0, 30, st.session_state.init_traffic.get(n, 5))

    st.header("🚑 Emergency Protocol")
    emergency_flag = st.toggle("Emergency Vehicle Present?")
    if emergency_flag:
        e_source = st.selectbox("Current Location", intersections)
        e_dest = st.selectbox("Destination", intersections, index=len(intersections)-1)

# ============================================================
# NETWORK & SIMULATION LOGIC
# ============================================================
G = nx.DiGraph()
G.add_nodes_from(intersections)
for i in range(num_intersections - 1):
    G.add_edge(intersections[i], intersections[i + 1])
    if i + 2 < num_intersections:
        G.add_edge(intersections[i], intersections[i + 2])

pos = nx.circular_layout(G) if num_intersections <= 6 else nx.spring_layout(G, seed=42)

def run_simulation():
    current_traffic = traffic_input.copy()
    cycle_data = []

    for cycle in range(1, 6):
        signal_state = {n: "RED" for n in intersections}
        xai = {n: [] for n in intersections}
        locked_green_nodes = set()
        phase = "Normal"
        corridor = []

        # 1. Emergency Preemption Module (Absolute Priority)
        if emergency_flag and cycle <= 3:
            phase = "Emergency"
            try:
                corridor = nx.shortest_path(G, e_source, e_dest)
                for n in corridor:
                    signal_state[n] = "GREEN"
                    locked_green_nodes.add(n)
                    xai[n].append("Emergency corridor; ABSOLUTE priority granted.")
            except nx.NetworkXNoPath:
                signal_state[e_source] = "GREEN"
                locked_green_nodes.add(e_source)
                xai[e_source].append("No path found; granting local emergency priority.")

        # 2. Rule Engine (WEIGHTED PRIORITY ENGINE)
        for n in intersections:
            if n in locked_green_nodes: continue
            
            # -- Step A: Calculate Initial Weight --
            priority_score = current_traffic[n]
            
            # -- Step B: Apply Downstream Penalty (Spillback Risk) --
            downstream_traffic = max([current_traffic.get(x, 0) for x in G.successors(n)] + [0])
            if downstream_traffic > 8:
                priority_score -= 10  # Massive penalty to prevent gridlocking the next node
                
            # -- Step C: CRITICAL OVERRIDE (The Fix) --
            # If traffic hits 15+, we ignore the downstream penalty to prevent local network collapse
            if current_traffic[n] >= 15:
                priority_score += 20 

            # -- Step D: Decision Thresholds --
            if priority_score >= 15:
                signal_state[n] = "GREEN"
                xai[n].append(f"CRITICAL OVERRIDE (Score: {priority_score}); forced GREEN to prevent total node collapse.")
            elif priority_score >= 8:
                signal_state[n] = "GREEN"
                xai[n].append(f"High priority (Score: {priority_score}); GREEN granted for flow.")
            elif priority_score < 0:
                signal_state[n] = "RED"
                xai[n].append(f"Spillback penalty applied (Score: {priority_score}); RED to protect downstream.")
            elif current_traffic[n] < 4:
                signal_state[n] = "RED"
                xai[n].append(f"Low traffic (Score: {priority_score}); GREEN avoided to save cycle time.")
            else:
                signal_state[n] = "RED"
                xai[n].append(f"Moderate traffic (Score: {priority_score}); holding RED.")

        cycle_data.append({
            "cycle": cycle, "signal": signal_state.copy(),
            "traffic": current_traffic.copy(), "corridor": corridor,
            "xai": xai, "phase": phase
        })

        # Update traffic for next cycle (Simulation step)
        for n in intersections:
            change = random.choice([-4, -3, -2]) if signal_state[n] == "GREEN" else random.choice([0, 1, 2])
            current_traffic[n] = max(0, current_traffic[n] + change)
            
    return cycle_data

data_results = run_simulation()

# ============================================================
# UI TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["📊 Visual Simulation", "🧠 Explainability (XAI)", "📈 Advanced Analytics"])

with tab1:
    st.subheader("Network Pulse")
    cols = st.columns(5)
    
    for i, data in enumerate(data_results):
        fig, ax = plt.subplots(figsize=(5, 5))
        node_colors = ["#2ecc71" if data["signal"][n] == "GREEN" else "#e74c3c" for n in intersections]
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, ax=ax, edgecolors="black")
        nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.3, width=1.5, ax=ax)
        
        if data["corridor"]:
            path_edges = list(zip(data['corridor'], data['corridor'][1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="#3498db", width=4, ax=ax)
            
        labels = {n: f"{n}\n{data['traffic'][n]}v" for n in intersections}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=9, font_weight="bold", ax=ax)
        ax.set_title(f"Cycle {data['cycle']}\nPhase: {data['phase']}", fontsize=10)
        ax.axis("off")
        cols[i].pyplot(fig)
    
    st.info("💡 Green circles represent active flow. Blue lines indicate the prioritized emergency corridor.")

with tab2:
    st.subheader("Human-Readable Logic Logs (Weighted Engine)")
    for data in data_results:
        with st.expander(f"Cycle {data['cycle']} Logic Breakdown ({data['phase']} Phase)"):
            c1, c2 = st.columns(2)
            for idx, n in enumerate(intersections):
                target_col = c1 if idx < len(intersections)/2 else c2
                color = "green" if data['signal'][n] == "GREEN" else "red"
                target_col.markdown(f"**Intersection {n}** (:{color}[{data['signal'][n]}]) | Traffic: {data['traffic'][n]}")
                for reason in data["xai"][n]:
                    target_col.caption(f"↳ {reason}")

with tab3:
    st.subheader("System Performance Evaluation")
    
    # High-Level Metrics
    m1, m2, m3 = st.columns(3)
    total_waiting = sum([sum(d["traffic"].values()) for d in data_results])
    m1.metric("Total Traffic Processed", f"{total_waiting} vehicles")
    
    avg_green_util = sum([list(d["signal"].values()).count("GREEN") for d in data_results]) / 5
    m2.metric("Avg. Green Utilization", f"{avg_green_util} nodes")
    
    emergency_impact = "Active" if emergency_flag else "Inactive"
    m3.metric("Emergency Priority", emergency_impact)

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        # Congestion Over Time
        st.write("**Congestion vs Decision Cycle**")
        congestion_at_red = [sum(d["traffic"][n] for n in intersections if d["signal"][n] == "RED") for d in data_results]
        fig_cong, ax_cong = plt.subplots(figsize=(6, 4))
        ax_cong.plot(range(1, 6), congestion_at_red, marker='o', color='#e74c3c', linewidth=2)
        ax_cong.set_ylabel("Vehicles Waiting at RED")
        ax_cong.set_xlabel("Decision Cycle")
        ax_cong.grid(True, alpha=0.3)
        st.pyplot(fig_cong)

        # Emergency Phase Comparison
        st.write("**Emergency vs Normal Phase Performance**")
        em_vals = [sum(d["traffic"].values()) for d in data_results if d["phase"] == "Emergency"]
        norm_vals = [sum(d["traffic"].values()) for d in data_results if d["phase"] == "Normal"]
        avg_em = sum(em_vals)/len(em_vals) if em_vals else 0
        avg_norm = sum(norm_vals)/len(norm_vals) if norm_vals else 0
        
        fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
        ax_bar.bar(["Emergency Phase", "Normal Phase"], [avg_em, avg_norm], color=["#3498db", "#95a5a6"])
        ax_bar.set_ylabel("Avg. Total Network Traffic")
        ax_bar.grid(axis='y', alpha=0.3)
        st.pyplot(fig_bar)

    with col_right:
        # Signal Utilization 
        st.write("**Signal Utilization Across Cycles**")
        green_counts = [list(d["signal"].values()).count("GREEN") for d in data_results]
        red_counts = [list(d["signal"].values()).count("RED") for d in data_results]
        cycles = range(1, 6)

        fig_util, ax_util = plt.subplots(figsize=(8, 5))
        ax_util.plot(cycles, green_counts, marker='o', label='GREEN Signals', linewidth=2)
        ax_util.plot(cycles, red_counts, marker='o', label='RED Signals', linewidth=2)
        
        ax_util.set_xlabel("Decision Cycle")
        ax_util.set_ylabel("Number of Intersections")
        ax_util.set_ylim(0, num_intersections + 0.5) 
        ax_util.set_xticks(cycles)
        ax_util.grid(True, linestyle='-', alpha=0.7)
        ax_util.legend()
        
        st.pyplot(fig_util)

        # Traffic Heatmap Table
        st.write("**Intersection Traffic Heatmap**")
        df_heat = pd.DataFrame([d["traffic"] for d in data_results], index=[f"Cycle {i+1}" for i in range(5)])
        st.dataframe(df_heat.style.background_gradient(cmap='YlOrRd', axis=None), use_container_width=True)
