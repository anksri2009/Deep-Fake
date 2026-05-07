import streamlit as st
import time
import random
import hashlib
import threading
import queue
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. System Configuration & Clean CSS Theme
# ==========================================
st.set_page_config(page_title="NSMIDP: Command Center", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Clean, Professional, High-Contrast Theme */
    h1, h2, h3, h4 { color: #1e3a8a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Card Styles */
    .tech-card { background-color: #ffffff; border: 1px solid #e5e7eb; padding: 20px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); color: #1f2937; }
    .warning-card { background-color: #fef2f2; border-left: 5px solid #ef4444; padding: 15px; margin-bottom: 10px; color: #7f1d1d; border-radius: 4px; }
    .safe-card { background-color: #f0fdf4; border-left: 5px solid #10b981; padding: 15px; margin-bottom: 10px; color: #064e3b; border-radius: 4px; }
    
    /* Status Indicators */
    .shield-active { color: #065f46; font-weight: bold; background-color: #d1fae5; padding: 10px; border-radius: 6px; border: 1px solid #34d399; text-align: center; }
    .shield-inactive { color: #991b1b; font-weight: bold; background-color: #fee2e2; padding: 10px; border-radius: 6px; border: 1px solid #f87171; text-align: center; }
    
    /* Logs Console */
    .log-container { background-color: #f8fafc; color: #334155; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 0.85rem; height: 300px; overflow-y: auto; border: 1px solid #cbd5e1; }
    .log-entry { margin-bottom: 4px; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; }
    
    /* Metric label visibility fix */
    div[data-testid="stMetricLabel"] { color: #475569; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. State Management & Logging Engine
# ==========================================
if 'current_view' not in st.session_state: st.session_state.current_view = 'onboarding'
if 'is_authenticated' not in st.session_state: st.session_state.is_authenticated = False
if 'alert_queue' not in st.session_state: st.session_state.alert_queue = queue.Queue()
if 'shield_running' not in st.session_state: st.session_state.shield_running = False
if 'system_logs' not in st.session_state: st.session_state.system_logs = []
if 'network_traffic' not in st.session_state: st.session_state.network_traffic = pd.DataFrame(columns=["Timestamp", "IP", "Destination", "Status", "Bytes"])

def add_log(message, level="INFO"):
    timestamp = datetime.now().strftime('%H:%M:%S')
    color = "#059669" if level == "INFO" else "#dc2626" if level == "CRITICAL" else "#d97706"
    log_entry = f"<div class='log-entry'><span style='color:{color}; font-weight:bold;'>[{timestamp}] [{level}]</span> {message}</div>"
    st.session_state.system_logs.insert(0, log_entry)
    if len(st.session_state.system_logs) > 100: st.session_state.system_logs.pop()

# ==========================================
# 3. Network Sovereignty Monitor Engine
# ==========================================
def simulate_network_traffic():
    destinations = [
        ("14.139.245.1", "India (MeghRaj Cloud)", "ALLOWED"),
        ("164.100.1.1", "India (NIC Data Center)", "ALLOWED"),
        ("103.21.244.0", "India (Mumbai AWS Region)", "ALLOWED"),
        ("198.51.100.42", "United States (Unknown Server)", "BLOCKED"),
        ("114.114.114.114", "China (Foreign Node)", "BLOCKED"),
        ("46.228.199.1", "Russia (Unverified Node)", "BLOCKED")
    ]
    
    new_logs = []
    for _ in range(random.randint(1, 4)):
        ip, dest, status = random.choice(destinations)
        bytes_transferred = random.randint(1024, 80485) if status == "ALLOWED" else 0
        new_row = {
            "Timestamp": datetime.now().strftime('%H:%M:%S'),
            "IP": ip, "Destination": dest, "Status": status, "Bytes": bytes_transferred
        }
        new_logs.append(new_row)
        
        if status == "BLOCKED":
            add_log(f"FOREIGN EXFILTRATION BLOCKED: {ip} ({dest})", "CRITICAL")
    
    df_new = pd.DataFrame(new_logs)
    st.session_state.network_traffic = pd.concat([df_new, st.session_state.network_traffic]).head(50)

# ==========================================
# 4. Core AI Processing
# ==========================================
class MultiModalAIEngine:
    @staticmethod
    def analyze_file(file_bytes, filename):
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        add_log(f"Processing payload hash: {file_hash[:16]}...", "INFO")
        
        risk_factors = []
        threat_score = 0.05
        
        time.sleep(1.5) # Simulate analysis
        
        if random.random() > 0.6: 
            risk_factors.append("Frequency domain artifacts detected.")
            threat_score += 0.35
        if random.random() > 0.7: 
            risk_factors.append("Latent visual noise patterns identified.")
            threat_score += 0.45
            
        auth_score = max(0.0, 1.0 - threat_score)
        
        if threat_score > 0.80: cat, col = "CRITICAL THREAT", "#dc2626"
        elif threat_score > 0.40: cat, col = "#d97706", "#d97706"
        else: cat, col = "AUTHENTIC / SAFE", "#059669"
            
        if not risk_factors:
            risk_factors = ["Cryptographic provenance verified.", "No synthetic anomalies detected."]
            
        return auth_score, threat_score, cat, col, risk_factors

# ==========================================
# 5. Background Daemons
# ==========================================
def background_daemon(q, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(2, 5))
        simulate_network_traffic() 
        
        if random.random() < 0.10:
            q.put({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "threat": "Synthetic Telephony Spoofing (SS7 Protocol)",
                "confidence": f"{random.uniform(0.90, 0.99):.2%}"
            })

def start_shield():
    if not st.session_state.shield_running:
        st.session_state.stop_event = threading.Event()
        st.session_state.shield_thread = threading.Thread(target=background_daemon, args=(st.session_state.alert_queue, st.session_state.stop_event), daemon=True)
        st.session_state.shield_thread.start()
        st.session_state.shield_running = True
        add_log("Global Security Daemon ACTIVATED.", "INFO")

def stop_shield():
    if st.session_state.shield_running:
        st.session_state.stop_event.set()
        st.session_state.shield_running = False
        add_log("Global Security Daemon DEACTIVATED.", "CRITICAL")

# ==========================================
# 6. UI Views
# ==========================================
def view_onboarding():
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    if os.path.exists("logo.png"): st.image("logo.png", width=250)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>NSMIDP: SECURE LOGIN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>National Cognitive Security Infrastructure</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        if not st.session_state.is_authenticated:
            st.text_input("Officer ID / Mobile Number", placeholder="Enter credentials...")
            if st.button("Authenticate with DigiLocker", use_container_width=True, type="primary"):
                with st.spinner("Verifying identity..."): time.sleep(1)
                st.session_state.is_authenticated = True
                add_log("Authentication successful.")
                st.rerun()
        else:
            st.success("✅ ACCESS GRANTED.")
            st.markdown("### System Initialization")
            st.checkbox("Enable Volatile Memory Purge (DPDPA Check)", value=True, disabled=True)
            st.checkbox("Engage Data Sovereignty Firewall", value=True, disabled=True)
            
            if st.button("Access Dashboard", type="primary", use_container_width=True):
                st.session_state.current_view = 'dashboard'
                start_shield()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def view_dashboard():
    # Header Panel
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if os.path.exists("logo.png"): st.image("logo.png", width=80)
    with c2:
        st.markdown("<h2 style='margin-bottom:0;'>COMMAND DASHBOARD</h2>", unsafe_allow_html=True)
        st.caption("Node: LKO-01 | Latency: 12ms | Encryption: AES-256")
    with c3:
        if st.session_state.shield_running:
            st.markdown("<div class='shield-active'>🛡️ SYSTEM SHIELD: ONLINE</div>", unsafe_allow_html=True)
            if st.button("Deactivate Shield", use_container_width=True): stop_shield(); st.rerun()
        else:
            st.markdown("<div class='shield-inactive'>⚠️ SYSTEM SHIELD: OFFLINE</div>", unsafe_allow_html=True)
            if st.button("Activate Shield", use_container_width=True, type="primary"): start_shield(); st.rerun()

    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Deep Scan", "🌐 Data Sovereignty", "📞 Active Threats", "🖥️ System Logs"])

    # --- TAB 1: Universal Scanner ---
    with tab1:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        st.subheader("Universal Threat Intelligence Scanner")
        
        uploaded_file = st.file_uploader("Upload Media, Binary, or Document", type=None)
        
        if uploaded_file is not None:
            st.info("Parsing file signatures...")
            file_bytes = uploaded_file.read()
            auth_score, threat_score, cat, color, reasons = MultiModalAIEngine.analyze_file(file_bytes, uploaded_file.name)
            
            st.markdown(f"<h3 style='color:{color}; text-align:center; padding: 10px; border: 2px solid {color}; border-radius: 5px;'>STATUS: {cat}</h3>", unsafe_allow_html=True)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Authenticity Confidence", f"{auth_score:.1%}")
            m2.metric("Synthetic Probability", f"{threat_score:.1%}")
            m3.metric("Data Retention", "PURGED (0 Bytes)")
            
            st.markdown("#### Execution Trace:")
            for r in reasons:
                icon = "✅" if "verified" in r.lower() or "no anomalies" in r.lower() else "⚠️"
                st.write(f"`{icon} {r}`")
                
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2: SOVEREIGNTY MONITOR ---
    with tab2:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        st.subheader("Data Exfiltration Monitor")
        st.write("Tracking network interfaces to enforce domestic processing.")
        
        if st.session_state.shield_running:
            df = st.session_state.network_traffic
            
            if not df.empty:
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.write("Awaiting network packets...")
                
            if st.button("Refresh Network View"): 
                simulate_network_traffic()
                st.rerun()
        else:
            st.error("System Shield Offline. Network monitoring is disabled.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 3: TELEMETRY SHIELD ---
    with tab3:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        st.subheader("Active Endpoint Intercepts")
        
        alerts = []
        while not st.session_state.alert_queue.empty():
            alerts.append(st.session_state.alert_queue.get())
            
        if alerts:
            for alert in alerts:
                st.markdown(f"""
                    <div class='warning-card'>
                        <h4 style='margin:0; color:#991b1b;'>🚨 BACKGROUND INTERCEPT</h4>
                        <b>Threat Matrix:</b> {alert['threat']}<br>
                        <b>Confidence:</b> {alert['confidence']}<br>
                        <b>Timestamp:</b> {alert['timestamp']}<br>
                        <b>Action Taken:</b> Connection Terminated
                    </div>
                """, unsafe_allow_html=True)
        elif st.session_state.shield_running:
            st.markdown("<div class='safe-card'><b>✔️ Secure:</b> All communication channels are actively monitored. No active vishing detected.</div>", unsafe_allow_html=True)
        else:
            st.warning("Shield Offline. Vulnerable to real-time injections.")
            
        if st.button("Refresh Threat Feed"): st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 4: SYSTEM LOGS ---
    with tab4:
        st.markdown("<div class='tech-card'>", unsafe_allow_html=True)
        st.subheader("System Event Logs")
        
        log_html = "".join(st.session_state.system_logs) if st.session_state.system_logs else "No active logs."
        st.markdown(f"<div class='log-container'>{log_html}</div>", unsafe_allow_html=True)
        
        if st.button("Flush Cache"):
            st.session_state.system_logs = []
            st.session_state.network_traffic = pd.DataFrame(columns=["Timestamp", "IP", "Destination", "Status", "Bytes"])
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    if st.session_state.current_view == 'onboarding':
        view_onboarding()
    elif st.session_state.current_view == 'dashboard':
        view_dashboard()