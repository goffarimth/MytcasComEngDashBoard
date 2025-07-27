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
