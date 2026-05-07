# 🚦 RouteXpert: Symbolic AI Traffic Management

> **Intelligent traffic signal optimization with explainable AI (XAI)**
> 
> RouteXpert uses symbolic AI and weighted priority scoring to optimize traffic flow across urban intersections, with special handling for emergency vehicles.

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 🎯 Overview

RouteXpert is an intelligent traffic management system that:

- **Optimizes signal timing** using weighted priority scoring algorithm
- **Visualizes traffic flow** across dynamic intersection networks
- **Handles emergencies** with automatic preemption for ambulances, fire trucks, and police
- **Explains decisions** with transparent XAI-based scoring system
- **Simulates scenarios** with customizable traffic patterns and network topologies

Perfect for urban planning, traffic research, and emergency response optimization.

---

## ✨ Key Features

### 🚨 Emergency Management
- Real-time detection of emergency vehicles
- Automatic priority routing to destination
- Clear signal visualization for emergency paths

### 🛣️ Smart Traffic Optimization
- **Weighted Priority Scoring**: Combines wait time, queue length, and congestion
- **Dynamic adjustments**: Responsive to changing traffic conditions
- **Multi-intersection support**: Scale from 2 to 10+ intersections

### 📊 Interactive Dashboard
- Live traffic visualization with NetworkX graphs
- Customizable intersection configuration
- Real-time traffic adjustment controls
- Emergency scenario testing

### 🤖 Explainable AI
- Transparent scoring methodology
- Detailed decision breakdowns
- Educational insight into traffic algorithms

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Graph Processing** | NetworkX |
| **Visualization** | Matplotlib, Pandas |
| **Language** | Python 3.8+ |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/TIRTHANATH20/RouteXpert-AI.git
cd RouteXpert-AI

# 2. Create virtual environment (optional but recommended)
python -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 🚀 Usage

### Basic Workflow

1. **Configure Network**
   - Use sidebar slider to set number of intersections (2-10)
   - Adjust initial traffic levels for each intersection
   - Click "Randomize Traffic" to generate random patterns

2. **Visualize Traffic**
   - View interactive graph showing intersections and traffic levels
   - Monitor queue lengths and wait times in real-time
   - See which signals are active

3. **Test Emergency Scenarios**
   - Toggle "Emergency Vehicle Present?"
   - Select current location and destination
   - Watch system automatically optimize routes

4. **Analyze Results**
   - Review scoring breakdowns
   - Compare different traffic scenarios
   - Export visualization for reports

---

## 📊 Algorithm Overview

### Weighted Priority Scoring

RouteXpert uses a transparent scoring system:

```
Priority Score = (w₁ × Wait Time) + (w₂ × Queue Length) + (w₃ × Congestion)
```

Where:
- **w₁, w₂, w₃** = Configurable weights
- **Wait Time** = Average time vehicles waiting at intersection
- **Queue Length** = Number of vehicles in queue
- **Congestion** = Overall network traffic density

Signals with highest priority scores turn green first.

### Emergency Preemption

When emergency vehicle active:
1. Calculate shortest path to destination
2. Set all signals on path to green
3. Suppress conflicting directions
4. Return to normal operation after vehicle passes

---

## 🎮 Interactive Features

### Sidebar Controls
- **Intersection Count**: Dynamically adjust network size
- **Traffic Input**: Set custom traffic levels per intersection
- **Randomize**: Generate random traffic patterns
- **Emergency Toggle**: Test emergency scenarios
- **Route Selection**: Choose emergency vehicle path

### Main Display
- **Network Graph**: Visual representation of intersections
- **Traffic Stats**: Real-time congestion metrics
- **Signal Status**: Current green/red signal states
- **Priority Queue**: Ranking of intersections by priority

---

## 📈 Use Cases

- **Urban Planning**: Model and optimize city traffic flows
- **Emergency Response**: Plan optimal routes for ambulances and fire trucks
- **Traffic Research**: Study intersection optimization algorithms
- **Education**: Learn about graph theory and AI decision-making
- **Simulation**: Test scenarios before real-world deployment

---

## 🔧 Configuration

Edit `app.py` to customize:

```python
# Adjust weights in priority scoring
WEIGHT_WAIT_TIME = 0.4
WEIGHT_QUEUE_LENGTH = 0.35
WEIGHT_CONGESTION = 0.25

# Modify simulation speed
SIMULATION_SPEED = 1.0

# Change emergency vehicle parameters
EMERGENCY_SPEED_FACTOR = 2.5
```

---

## 📝 Example Scenarios

### Scenario 1: Peak Hour Optimization
1. Set 5 intersections
2. Set traffic levels 15-20 across all
3. Watch system distribute green signals based on priorities

### Scenario 2: Emergency Response
1. Set 3 intersections in line
2. Set traffic 10-15 at each
3. Toggle emergency, select ambulance route
4. Observe automatic signal preemption

### Scenario 3: Network Scaling
1. Gradually increase intersection count
2. Observe algorithm performance
3. Test limits and optimization strategies

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make improvements with clear commit messages
4. Push and create Pull Request

### Potential Enhancements
- [ ] Machine learning prediction models
- [ ] Real-world traffic data integration
- [ ] Multi-modal transport support
- [ ] Advanced visualization options
- [ ] Performance benchmarking
- [ ] API endpoint for external systems

---

## 📚 Learning Resources

- **NetworkX Documentation**: https://networkx.org/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Traffic Engineering Basics**: https://en.wikipedia.org/wiki/Traffic_engineering_(transportation)
- **Graph Algorithms**: https://en.wikipedia.org/wiki/Graph_algorithm

---

## ⚙️ Troubleshooting

### Application won't start
```bash
# Verify dependencies
pip install --upgrade -r requirements.txt

# Clear Streamlit cache
streamlit cache clear
```

### Slow performance with many intersections
- Reduce number of intersections to 5-6
- Simplify visualization options
- Increase simulation time step

### Traffic visualization not updating
- Check NetworkX installation: `pip install --upgrade networkx`
- Restart Streamlit app
- Clear browser cache

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Tirtha Nath** ([@TIRTHANATH20](https://github.com/TIRTHANATH20))
- Computer Science Engineer
- AI/ML Enthusiast
- Traffic Systems Research

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for interactive visualization
- Graph algorithms powered by [NetworkX](https://networkx.org/)
- Inspired by real-world traffic management challenges

---

## 📮 Contact & Support

- **GitHub**: [@TIRTHANATH20](https://github.com/TIRTHANATH20)
- **Issues**: [Report bugs here](https://github.com/TIRTHANATH20/RouteXpert-AI/issues)
- **Email**: [tirthanath2006@gmail.com](mailto:tirthanath2006@gmail.com)

---

<p align="center">
  <sub>🚦 Making traffic smarter, one intersection at a time</sub>
</p>
