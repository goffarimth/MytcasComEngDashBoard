#🎓 MyTCAS ComEng Dashboard
แดชบอร์ดวิเคราะห์ข้อมูลหลักสูตร วิศวกรรมคอมพิวเตอร์ และ ปัญญาประดิษฐ์ (AI) จากระบบ TCAS โดยดึงข้อมูลอัตโนมัติ พร้อมแสดงผลแบบอินเตอร์แอคทีฟผ่านเว็บแอป

📌 จุดประสงค์ของโปรเจกต์
แสดงข้อมูล TCAS ของหลักสูตรวิศวกรรมคอมพิวเตอร์ และ AI

ประเมินค่าใช้จ่ายที่เกี่ยวข้องกับการศึกษาในหลักสูตรนั้น ๆ

🛠 เทคโนโลยีที่ใช้
Python

Playwright – สำหรับการ scrape ข้อมูลจากเว็บไซต์

Pandas – สำหรับจัดการข้อมูลเชิงตาราง

Streamlit – สำหรับสร้าง Dashboard แบบ Web UI

📁 โครงสร้างโปรเจกต์
MytcasComEngDashBoard/
├── scraping/
│   └── extractor.py       # ไฟล์หลักสำหรับดึงข้อมูลจาก MyTCAS
├── data/
│   └── result_tcas_20250728_002531.xlsx          # ไฟล์ข้อมูลที่ scrape มาเก็บไว้
├── dashboard/
│   └── app.py           # Streamlit web app สำหรับแสดงผล Dashboard
├── requirements.txt     # รายการ dependency ที่ใช้
└── README.md

🚀 วิธีติดตั้งและใช้งาน
1. Clone โปรเจกต์
```bash
git clone https://github.com/goffarimth/MytcasComEngDashBoard.git
cd MytcasComEngDashBoard
```
2. สร้าง Virtual Environment และติดตั้งไลบรารี
```bash
python -m venv venv
source venv/bin/activate  # หรือ venv\Scripts\activate บน Windows
pip install -r requirements.txt
```
3. ดึงข้อมูลจากเว็บไซต์ (Scraping)
```bash
python extractor.py
```
💡 หมายเหตุ: การใช้งาน playwright ครั้งแรก อาจต้องติดตั้ง browser dependencies เพิ่มเติมด้วยคำสั่ง
playwright install

4. รัน Dashboard
```bash
streamlit run app.py
```
