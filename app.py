
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Student Engagement Intelligence System", layout="wide")

# Title
st.title(" Student Engagement Intelligence System")
st.markdown("**PragyanAI — Analyzing student behavior to predict placement outcomes**")

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/pragyanaischool/VTU_Internship_DataSets/refs/heads/main/student_data_engament_Project_8.csv"
    df = pd.read_csv(url)
    return df

df = load_data()
st.success("Dataset loaded successfully!")

# Create engineered features immediately after loading
df["Engagement_Score"] = (df["Attendance_%"] + df["Login_Frequency"] + 
                          df["Time_Spent_Hours"] + df["Videos_Watched"] + 
                          df["Quiz_Score"] + df["Doubts_Raised"])

df["Learning_Effectiveness"] = df["Quiz_Score"] * df["Video_Completion_%"] / 100

df["Interaction_Score"] = (df["Doubts_Raised"] + df["Doubts_Resolved"] + 
                           df["Hackathons"] + df["Workshops"])

# Sidebar
st.sidebar.title("Navigation")
section = st.sidebar.selectbox("Choose Section", [
    "Overview",
    "Engagement Analysis", 
    "Student Segmentation",
    "Risk Detection"
])

# Overview Section
if section == "Overview":
    st.header(" Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", "50,000")
    col2.metric("Placement Rate", "60.26%")
    col3.metric("Features", "19")
    
    st.subheader("Sample Data")
    st.dataframe(df.head(10))

# Engagement Analysis Section
if section == "Engagement Analysis":
    st.header(" Engagement Analysis")
    
    
    st.subheader("Attendance vs Placement")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.boxplot(x="Placement_Status", y="Attendance_%", data=df, ax=ax)
    ax.set_xlabel("Placement Status (0=Not Placed, 1=Placed)")
    ax.set_ylabel("Attendance %")
    st.pyplot(fig)
    
    st.subheader("Quiz Score vs Placement")
    fig2, ax2 = plt.subplots(figsize=(8,4))
    sns.boxplot(x="Placement_Status", y="Quiz_Score", data=df, ax=ax2)
    ax2.set_xlabel("Placement Status (0=Not Placed, 1=Placed)")
    ax2.set_ylabel("Quiz Score")
    st.pyplot(fig2)

# Student Segmentation Section
if section == "Student Segmentation":
    st.header("Student Segmentation")
    
    # Create segments
    def categorize_student(row):
        if row['Engagement_Score'] > 300 and row['Quiz_Score'] > 75:
            return 'High Performer'
        elif row['Engagement_Score'] > 300 and row['Quiz_Score'] <= 75:
            return 'Active but Confused'
        elif row['Engagement_Score'] <= 300 and row['Quiz_Score'] > 75:
            return 'Passive Learner'
        else:
            return 'Disengaged'
    
    df['Student_Segment'] = df.apply(categorize_student, axis=1)
    
    # Show counts
    segment_counts = df['Student_Segment'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Segment Distribution")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.countplot(x="Student_Segment", data=df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Segment Counts")
        st.dataframe(segment_counts)

# Risk Detection Section
if section == "Risk Detection":
    st.header(" Risk Detection")
    
    # Define risk
    def detect_risk(row):
        if row['Attendance_%'] < 60 and row['Quiz_Score'] < 50:
            return 'High Risk'
        elif row['Attendance_%'] < 70 or row['Quiz_Score'] < 60:
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    df['Risk_Level'] = df.apply(detect_risk, axis=1)
    
    # Show risk counts
    risk_counts = df['Risk_Level'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Distribution")
        fig, ax = plt.subplots(figsize=(6,4))
        sns.countplot(x="Risk_Level", data=df, 
                     order=['High Risk', 'Medium Risk', 'Low Risk'], ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Risk Counts")
        st.dataframe(risk_counts)
    
    # Show high risk students
    st.subheader(" High Risk Students Sample")
    high_risk = df[df['Risk_Level'] == 'High Risk'][
        ['Attendance_%', 'Quiz_Score', 'Doubts_Raised', 'Placement_Status']
    ].head(10)
    st.dataframe(high_risk)