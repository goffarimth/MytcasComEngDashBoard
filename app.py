import streamlit as st
import pandas as pd
import altair as alt

# โหลดข้อมูล
df = pd.read_excel("result_tcas_20250728_002531.xlsx")

st.set_page_config(page_title="Dashboard หลักสูตรวิศวกรรมคอมฯ", layout="wide")

# ==== TCAS68 STYLE (CSS) ====
st.markdown("""
    <style>
        /* พื้นหลังทั้งหน้า */
        body {
            background-color: #e3f2fd;
        }

        /* พื้นที่เนื้อหาหลัก */
        .main {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1rem;
        }

        /* แถบด้านข้าง */
        .sidebar .sidebar-content {
            background-color: #01579b;
            color: white;
        }

        /* ตัวหนังสือใน sidebar */
        .sidebar .sidebar-content h1, 
        .sidebar .sidebar-content h2, 
        .sidebar .sidebar-content label, 
        .sidebar .sidebar-content span,
        .sidebar .sidebar-content .stTextInput>div>div>input {
            color: white !important;
        }

        /* ปุ่ม */
        .stButton>button {
            background-color: #00acc1;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #00838f;
            color: white;
        }

        /* Expander */
        .streamlit-expanderHeader {
            font-weight: bold;
            color: #01579b;
        }
    </style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.title("🎓 Dashboard หลักสูตรวิศวกรรมคอมพิวเตอร์ และ AI")
st.markdown("ข้อมูลจาก [mytcas.com](https://www.mytcas.com)")

# ==== FILTERS (SIDEBAR) ====
st.sidebar.header("🔍 ตัวกรองข้อมูล")

# 1. ค้นหาด้วยคำค้นในชื่อหลักสูตร
search_text = st.sidebar.text_input("🔎 ค้นหาจากชื่อหลักสูตร/มหาวิทยาลัย/คณะ", "")

# 2. เลือกประเภทสาขาวิชา
selected_saka = st.sidebar.selectbox("📙 เลือกสาขาวิชา", ["ทั้งหมด"] + sorted(df["คำค้น"].unique()))

# 3. เลือกประเภทหลักสูตร
selected_course_type = st.sidebar.selectbox("📘 ประเภทหลักสูตร", ["ทั้งหมด"] + sorted(df["ประเภทหลักสูตร"].unique()))

# 4. เลือกมหาวิทยาลัย
selected_univ = st.sidebar.selectbox("🏫 เลือกมหาวิทยาลัย", ["ทั้งหมด"] + sorted(df["มหาวิทยาลัย"].unique()))

# ==== APPLY FILTER ====
filtered_df = df.copy()

if search_text:
    filtered_df = filtered_df[
        filtered_df["ชื่อหลักสูตร"].str.contains(search_text, case=False, na=False) |
        (filtered_df["มหาวิทยาลัย"].str.contains(search_text, case=False, na=False) |
         filtered_df["คณะ"].str.contains(search_text, case=False, na=False))]

if selected_course_type != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["ประเภทหลักสูตร"] == selected_course_type]

if selected_univ != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["มหาวิทยาลัย"] == selected_univ]

if selected_saka != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df["คำค้น"] == selected_saka]

# ==== PREPARE DISPLAY ====
filtered_df["หลักสูตร"] = filtered_df["มหาวิทยาลัย"] + " | " + filtered_df["ชื่อหลักสูตร"]
filtered_df = filtered_df.sort_values(by="ค่าใช้จ่าย", ascending=True)

# ==== BAR CHART ====
st.subheader("📊 กราฟแสดงค่าใช้จ่ายของหลักสูตร (บาท/เทอม)")
if filtered_df.empty:
    st.warning("ไม่พบข้อมูลที่ตรงกับเงื่อนไข กรุณาลองเปลี่ยนตัวกรอง")
else:
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("ค่าใช้จ่าย:Q", title="ค่าใช้จ่าย (บาท/เทอม)"),
        y=alt.Y("หลักสูตร:N", sort='-x', title=None,
                axis=alt.Axis(labelFontSize=14)),
        color=alt.Color("มหาวิทยาลัย:N", legend=None),
        tooltip=["มหาวิทยาลัย", "ชื่อหลักสูตร", "ประเภทหลักสูตร", "ค่าใช้จ่าย"]
    ).properties(height=1000)

    st.altair_chart(chart, use_container_width=True)

# ==== DATA TABLE ====
with st.expander("📄 ตารางข้อมูลหลักสูตร"):
    st.dataframe(
        filtered_df[["มหาวิทยาลัย", "ชื่อหลักสูตร", "ค่าใช้จ่าย", "ประเภทหลักสูตร", "ลิงก์"]],
        use_container_width=True
    )
