import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Hospital Infection Spread Simulator (SIR Model + Hygiene Intervention)")

st.write("""
Interactive simulation of hospital-acquired infections using the SIR model.
Adjust parameters to observe how infection spreads and how hygiene affects outcomes.
""")

st.sidebar.header("Input Parameters")

N = st.sidebar.slider("Total Population (N)", 50, 1000, 200)
I0 = st.sidebar.slider("Initial Infected (I0)", 1, 50, 5)
R0 = st.sidebar.slider("Initial Recovered (R0)", 0, 50, 0)

beta = st.sidebar.slider("Infection Rate (β)", 0.1, 1.0, 0.4)
gamma = st.sidebar.slider("Recovery Rate (γ)", 0.05, 0.5, 0.1)
h = st.sidebar.slider("Hygiene Effect (h)", 0.0, 1.0, 0.3)

days = st.sidebar.slider("Simulation Days", 10, 200, 60)

S0 = N - I0 - R0

S = [S0]
I = [I0]
R = [R0]

for t in range(days):
    beta_eff = beta * (1 - h)

    new_infections = beta_eff * S[-1] * I[-1] / N
    new_recoveries = gamma * I[-1]

    S.append(S[-1] - new_infections)
    I.append(I[-1] + new_infections - new_recoveries)
    R.append(R[-1] + new_recoveries)

S = np.array(S)
I = np.array(I)
R = np.array(R)

st.subheader("Infection Spread Graph")

fig, ax = plt.subplots()
ax.plot(S, label="Susceptible")
ax.plot(I, label="Infected")
ax.plot(R, label="Recovered")
ax.set_xlabel("Days")
ax.set_ylabel("Population")
ax.legend()

st.pyplot(fig)

st.subheader("Key Metrics")

peak_infected = int(np.max(I))
peak_day = int(np.argmax(I))
final_recovered = int(R[-1])

col1, col2, col3 = st.columns(3)

col1.metric("Peak Infected", peak_infected)
col2.metric("Peak Day", peak_day)
col3.metric("Final Recovered", final_recovered)

st.subheader("Model Explanation")

st.write("""
### SIR Model Equations

dS/dt = -β(SI/N)  
dI/dt = β(SI/N) - γI  
dR/dt = γI  

Where:
- S = Susceptible
- I = Infected
- R = Recovered
- β = Infection rate
- γ = Recovery rate
""")

st.write("""
### Hygiene Intervention

Effective infection rate:

β_effective = β × (1 - h)

- h = 0 → No hygiene
- h = 0.5 → Moderate hygiene
- h = 1 → Perfect hygiene (no infection spread)
""")

st.write("""
### Interpretation

- Increasing β → faster infection spread  
- Increasing γ → faster recovery  
- Increasing h → reduces infection rate  

This helps hospitals plan infection control strategies.
""")

