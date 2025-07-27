import asyncio
import pandas as pd
from datetime import datetime
from playwright.async_api import async_playwright

class TCASScraperNewStyle:
    def __init__(self):
        self.base_url = "https://course.mytcas.com"
        self.results = []

    async def _get_search_input(self, page):
        selectors = [
            "input[placeholder*='มหาวิทยาลัย']",
            "input[placeholder*='ค้นหา']",
            "input[type='search']",
            "input.search-input",
            "#search-input"
        ]
        for selector in selectors:
            try:
                return await page.wait_for_selector(selector, timeout=3000)
            except:
                continue
        return None

    async def _get_result_items(self, page):
        selectors = [
            ".t-programs > li", ".program-list li", ".search-results li",
            ".results li", "[data-testid='program-item']"
        ]
        for selector in selectors:
            try:
                results = await page.query_selector_all(selector)
                if results:
                    return results
            except:
                continue
        return []

    async def _parse_program_item(self, li, keyword):
        try:
            text = await li.inner_text()
            anchor = await li.query_selector("a")
            if not anchor:
                return None
            href = await anchor.get_attribute("href")
            link = href if href.startswith("http") else f"{self.base_url}{href}"

            lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
            title = lines[0] if len(lines) > 0 else ""
            faculty = lines[1] if len(lines) > 1 else ""
            university = lines[2] if len(lines) > 2 else ""

            return {
                'keyword': keyword,
                'program_name': title,
                'faculty': faculty,
                'university': university,
                'url': link,
                'raw_text': text
            }
        except:
            return None

    async def _search_programs(self, page, keyword):
        await page.goto(self.base_url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(1)

        search_box = await self._get_search_input(page)
        if not search_box:
            print("❌ ไม่พบช่องค้นหา")
            return []

        await search_box.fill("")
        await search_box.fill(keyword)
        await search_box.press("Enter")
        await asyncio.sleep(2)

        items = await self._get_result_items(page)
        found = []
        for li in items:
            data = await self._parse_program_item(li, keyword)
            if data:
                found.append(data)
        return found

    async def _extract_details(self, page, program):
        try:
            await page.goto(program['url'], wait_until='networkidle', timeout=30000)
            await asyncio.sleep(1.5)

            def_field = lambda: "ไม่พบข้อมูล"
            info = {
                'คำค้น': program['keyword'],
                'ชื่อหลักสูตร': program['program_name'],
                'มหาวิทยาลัย': program['university'],
                'คณะ': program['faculty'],
                'ประเภทหลักสูตร': def_field(),
                'ค่าใช้จ่าย': def_field(),
                'ลิงก์': program['url'],
                'วันที่เก็บข้อมูล': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            fields = {
                'ประเภทหลักสูตร': ["dt:has-text('ประเภทหลักสูตร') + dd", ".program-type"],
                'ค่าใช้จ่าย': ["dt:has-text('ค่าใช้จ่าย') + dd", ".fee-info", ".tuition-fee"]
            }

            for field, selectors in fields.items():
                for selector in selectors:
                    try:
                        el = await page.query_selector(selector)
                        if el:
                            txt = (await el.inner_text()).strip()
                            if txt:
                                info[field] = txt
                                break
                    except:
                        continue

            self.results.append(info)
            print(f"✅ เก็บ: {info['ชื่อหลักสูตร'][:40]} | 💰 {info['ค่าใช้จ่าย']}")
        except Exception as e:
            print(f"⚠️ ดึงข้อมูลผิดพลาด: {str(e)}")

    async def run(self, keywords):
        print("🚀 เริ่มดึงข้อมูล TCAS ใหม่\n" + "-" * 50)

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context(locale="th-TH")
            page = await context.new_page()

            collected = []
            for kw in keywords:
                print(f"\n🔎 คำค้น: {kw}")
                programs = await self._search_programs(page, kw)
                collected.extend(programs)
                await asyncio.sleep(1)

            for i, program in enumerate(collected):
                print(f"\n[{i+1}/{len(collected)}] รายการ: {program['program_name'][:40]}")
                await self._extract_details(page, program)
                await asyncio.sleep(1)

            await browser.close()

    def export_excel(self, name="result_tcas"):
        if not self.results:
            print("⚠️ ไม่มีข้อมูล")
            return

        df = pd.DataFrame(self.results)

        # 🔍 ลบข้อมูลที่ซ้ำกันโดยพิจารณาเฉพาะ 3 คอลัมน์นี้
        before = len(df)
        df.drop_duplicates(subset=["ชื่อหลักสูตร", "คณะ", "มหาวิทยาลัย"], inplace=True)
        after = len(df)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"{name}_{timestamp}.xlsx"
        df.to_excel(fname, index=False, engine='openpyxl')

        print(f"\n💾 บันทึกไฟล์: {fname} | {after} รายการ (ลบซ้ำ {before - after} รายการ)")

        # แสดงสรุป
        print("\n📊 สถิติ:")
        print(df["คำค้น"].value_counts())
        print(f"💰 มีค่าใช้จ่าย: {df[df['ค่าใช้จ่าย'] != 'ไม่พบข้อมูล'].shape[0]}")


async def main():
    scraper = TCASScraperNewStyle()
        # 🔍 กำหนดคำค้นหาไว้ล่วงหน้า
    keywords = [
        "คณะวิศวกรรมศาสตร์ วิศวกรรมคอมพิวเตอร์",
        "คณะวิศวกรรมศาสตร์ วิศวกรรมปัญญาประดิษฐ์"  # ← เพิ่มคำนี้เข้ามา
    ]

    await scraper.run(keywords)
    scraper.export_excel()

if __name__ == "__main__":
    asyncio.run(main())
