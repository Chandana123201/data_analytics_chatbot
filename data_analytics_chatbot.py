import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google import genai
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()

# Load API key safely from environment variable
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Streamlit App Setup ---
st.set_page_config(page_title="Data Analytics Chatbot", layout="centered")
st.title("🤖 Data Analytics Chatbot")
st.write("Ask me anything about your data or general analytics!")

# --- CSV Upload Section ---
st.subheader("📂 Upload your CSV file")
uploaded_file = st.file_uploader("Choose your file", type=["csv"])

# --- Load Demo Dataset Button ---
if st.button("📊 Load Demo Dataset (Sales Data)"):
    demo_data = {
        'Date': ['05-01-2025', '07-01-2025', '09-01-2025', '12-01-2025', '15-01-2025', '18-01-2025', '20-01-2025', '22-01-2025'],
        'Region': ['North', 'South', 'East', 'West', 'North', 'East', 'South', 'West'],
        'Product': ['Laptop', 'Smartphone', 'Tablet', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 'Headphones'],
        'Units Sold': [20, 45, 30, 15, 40, 80, 100, 60],
        'Unit Price': [75000, 25000, 30000, 60000, 10000, 2000, 1500, 3000],
        'Total Sales': [1500000, 1125000, 900000, 900000, 400000, 160000, 150000, 180000],
        'Profit': [250000, 180000, 120000, 100000, 75000, 30000, 25000, 40000]
    }
    df = pd.DataFrame(demo_data)
    st.session_state["data"] = df
    st.success("✅ Demo dataset loaded successfully!")

# --- Handle Uploaded CSV ---
elif uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.session_state["data"] = df
    st.success("✅ File uploaded successfully!")
    st.write("### 📄 Data Preview:")
    st.dataframe(df.head())

# --- Textbox always visible ---
question = st.text_input("💬 Ask your question (about data or analytics):")

if question:
    if "data" in st.session_state:
        df = st.session_state["data"]
        prompt = f"""
        You are a data analyst. Analyze this dataset and answer clearly.
        Columns: {list(df.columns)}.
        Question: "{question}".
        """
    else:
        prompt = f"""
        You are a data analytics expert.
        The user asked: "{question}".
        Provide a clear and helpful explanation or answer.
        """

    # --- Generate response from Gemini ---
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt]
        )
        insight = response.text
        st.write("### 🧠 AI Insight:")
        st.write(insight)
    except Exception as e:
        st.error(f"⚠️ Gemini API error: {str(e)}")
        insight = "Error generating AI response."

    # --- Optional Auto Visualization ---
    chart_generated = False
    chart_path = None
    if "data" in st.session_state:
        q = question.lower()
        df = st.session_state["data"]
        if "sales" in q and "profit" in q:
            possible_sales = [col for col in df.columns if "sale" in col.lower()]
            possible_profit = [col for col in df.columns if "profit" in col.lower()]
            if possible_sales and possible_profit:
                plt.figure(figsize=(8, 6))
                sns.scatterplot(data=df, x=possible_sales[0], y=possible_profit[0])
                plt.title("Sales vs Profit")
                plt.grid(True)
                chart_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                plt.savefig(chart_path)
                st.pyplot(plt)
                chart_generated = True
            else:
                st.warning("Couldn’t find suitable 'sales' or 'profit' columns.")

    # --- PDF Report Generation ---
    if st.button("📄 Download Analysis as PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            c = canvas.Canvas(tmpfile.name, pagesize=A4)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 800, "Data Analytics Report")
            c.setFont("Helvetica", 12)
            c.drawString(100, 770, f"Question: {question}")
            c.drawString(100, 750, "AI Insight:")
            text_obj = c.beginText(100, 730)
            for line in insight.split("\n"):
                text_obj.textLine(line)
            c.drawText(text_obj)

            # Add chart if generated
            if chart_generated and os.path.exists(chart_path):
                c.drawImage(chart_path, 80, 400, width=400, height=300)

            c.save()

            with open(tmpfile.name, "rb") as f:
                st.download_button(
                    label="⬇️ Click to Download PDF",
                    data=f,
                    file_name="data_analysis_report.pdf",
                    mime="application/pdf"
                )

else:
    st.info("💡 Tip: Upload a CSV or use demo data to get dataset-based insights.")
