
import streamlit as st
import datetime as dt
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Hospital Appointment Scheduler", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 30px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'base_url' not in st.session_state:
    st.session_state.base_url = 'http://localhost:4444'

# Main header
st.markdown("<h1 class='main-header'>🏥 Hospital Appointment Scheduler</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='main-header'>Natore Hospital Management System</h3>", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.session_state.base_url = st.text_input(
        "Backend URL",
        value=st.session_state.base_url,
        help="Enter your FastAPI backend URL (e.g., http://localhost:8000)"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Quick Info")
    st.info("""
    This application allows you to:
    - 📅 Schedule new appointments
    - ❌ Cancel existing appointments
    - 📊 View all active appointments
    """)

# Main tabs
tab1, tab2, tab3 = st.tabs(["📅 Schedule Appointment", "❌ Cancel Appointment", "📊 View Appointments"])

# ===== TAB 1: SCHEDULE APPOINTMENT =====
with tab1:
    st.header("Schedule a New Appointment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patient Information")
        with st.form("schedule_form"):
            patient_name = st.text_input(
                "👤 Patient Name",
                placeholder="Enter full name",
                help="Full name of the patient"
            )
            
            reason = st.text_area(
                "📝 Reason for Appointment",
                placeholder="Describe the reason for visit",
                height=100,
                help="What is the appointment for?"
            )
            
            appt_date = st.date_input(
                "📅 Appointment Date",
                value=dt.date.today() + dt.timedelta(days=1),
                min_value=dt.date.today(),
                help="Select the appointment date"
            )
            
            appt_time = st.time_input(
                "🕐 Appointment Time",
                value=dt.time(9, 0),
                help="Select the appointment time"
            )
            
            start_time = dt.datetime.combine(appt_date, appt_time)
            
            submit_schedule = st.form_submit_button(
                "✅ Schedule Appointment",
                use_container_width=True
            )
    
    with col2:
        st.subheader("Preview")
        if st.session_state.get('preview_data'):
            preview = st.session_state.preview_data
            st.info(f"""
            **Patient:** {preview['name']}
            
            **Reason:** {preview['reason']}
            
            **Time:** {preview['time']}
            """)
        else:
            st.info("Fill in the form to see preview")
    
    # Handle schedule appointment submission
    if submit_schedule:
        if not patient_name or not reason:
            st.markdown('<div class="error-box">❌ Please fill in all required fields!</div>', unsafe_allow_html=True)
        else:
            with st.spinner("📤 Scheduling appointment..."):
                try:
                    response = requests.post(
                        f"{st.session_state.base_url}/schedule_appointments/",
                        json={
                            "patient_name": patient_name,
                            "reason": reason,
                            "start_time": start_time.isoformat()
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown(f"""
                        <div class="success-box">
                        ✅ <b>Appointment Scheduled Successfully!</b><br>
                        Appointment ID: {data.get('id', 'N/A')}<br>
                        Patient: {data.get('patient_name', 'N/A')}<br>
                        Time: {data.get('start_time', 'N/A')}<br>
                        Status: Active
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">❌ Error: {response.text}</div>', unsafe_allow_html=True)
                        
                except requests.exceptions.ConnectionError:
                    st.markdown(f'<div class="error-box">❌ Connection Error: Cannot reach backend at {st.session_state.base_url}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

# ===== TAB 2: CANCEL APPOINTMENT =====
with tab2:
    st.header("Cancel an Appointment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cancellation Details")
        with st.form("cancel_form"):
            cancel_patient_name = st.text_input(
                "👤 Patient Name",
                placeholder="Enter patient name",
                help="Name of the patient whose appointment to cancel"
            )
            
            cancel_appt_date = st.date_input(
                "📅 Appointment Date",
                value=dt.date.today(),
                help="The appointment date to cancel"
            )
            
            cancel_appt_time = st.time_input(
                "🕐 Appointment Time",
                value=dt.time(9, 0),
                help="The appointment time to cancel"
            )
            
            cancel_date = dt.datetime.combine(cancel_appt_date, cancel_appt_time)
            
            submit_cancel = st.form_submit_button(
                "❌ Cancel Appointment",
                use_container_width=True
            )
    
    with col1:
        st.warning("⚠️ This action will mark the appointment as canceled.")
    
    # Handle cancel appointment submission
    if submit_cancel:
        if not cancel_patient_name:
            st.markdown('<div class="error-box">❌ Please fill in all required fields!</div>', unsafe_allow_html=True)
        else:
            with st.spinner("🔄 Canceling appointment..."):
                try:
                    response = requests.post(
                        f"{st.session_state.base_url}/cancel_appointment/",
                        json={
                            "patient_name": cancel_patient_name,
                            "date": cancel_date.isoformat()
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown(f"""
                        <div class="success-box">
                        ✅ <b>Appointment Canceled Successfully!</b><br>
                        Appointment ID: {data.get('id', 'N/A')}<br>
                        Patient: {data.get('patient_name', 'N/A')}<br>
                        Original Time: {data.get('start_time', 'N/A')}<br>
                        Status: Canceled
                        </div>
                        """, unsafe_allow_html=True)
                    elif response.status_code == 404:
                        st.markdown('<div class="error-box">❌ Appointment not found or already canceled!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-box">❌ Error: {response.text}</div>', unsafe_allow_html=True)
                        
                except requests.exceptions.ConnectionError:
                    st.markdown(f'<div class="error-box">❌ Connection Error: Cannot reach backend at {st.session_state.base_url}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

# ===== TAB 3: VIEW APPOINTMENTS =====
with tab3:
    st.header("Active Appointments")
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with st.spinner("📊 Loading appointments..."):
        try:
            response = requests.get(
                f"{st.session_state.base_url}/list_appointments/",
                timeout=10
            )
            
            if response.status_code == 200:
                appointments = response.json()
                
                if not appointments:
                    st.markdown('<div class="info-box">ℹ️ No active appointments found.</div>', unsafe_allow_html=True)
                else:
                    # Convert to DataFrame for better display
                    df_data = []
                    for appt in appointments:
                        df_data.append({
                            'ID': appt.get('id'),
                            'Patient Name': appt.get('patient_name'),
                            'Reason': appt.get('reason'),
                            'Appointment Time': appt.get('start_time'),
                            'Status': '✅ Active' if not appt.get('canceled') else '❌ Canceled',
                            'Created': appt.get('created_at')
                        })
                    
                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Summary statistics
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Appointments", len(appointments))
                    with col2:
                        st.metric("Upcoming (Next 7 days)", sum(1 for a in appointments if (datetime.fromisoformat(a.get('start_time')) - datetime.now()).days <= 7))
                    with col3:
                        st.metric("Status", "Operational ✅")
            else:
                st.markdown(f'<div class="error-box">❌ Error: {response.text}</div>', unsafe_allow_html=True)
                
        except requests.exceptions.ConnectionError:
            st.markdown(f'<div class="error-box">❌ Connection Error: Cannot reach backend at {st.session_state.base_url}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 12px;">
    <p>🏥 Natore Hospital Appointment System | Version 1.0</p>
    <p>Powered by FastAPI & Streamlit</p>
</div>
""", unsafe_allow_html=True)
