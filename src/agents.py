"""
מערכת הסוכנים של LUMINA - לומינה
כוללת: DomainAgent, ManagerAgent, Orchestrator
"""

import os
import json
import time
import asyncio
from datetime import datetime
from typing import Optional
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

ORCHESTRATOR_MODEL = "claude-opus-4-6"
DOMAIN_AGENT_MODEL = "claude-sonnet-4-6"

WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search"}


class DomainAgent:
    """סוכן דומיין - מחקר מעמיק בתחום ספציפי"""

    def __init__(self, domain: dict, output_dir: str):
        self.domain = domain
        self.output_dir = output_dir

    def research(self) -> dict:
        """מריץ מחקר על הדומיין ומחזיר תוצאות"""
        domain_id = self.domain["id"]
        domain_name = self.domain["name_he"]
        emoji = self.domain["emoji"]

        print(f"\n{emoji} סוכן [{domain_name}] מתחיל מחקר...")

        messages = [{"role": "user", "content": self.domain["prompt"]}]
        full_response = ""

        # retry עם המתנה על rate limit
        for attempt in range(5):
            try:
                full_response = ""
                with client.messages.stream(
                    model=DOMAIN_AGENT_MODEL,
                    max_tokens=8000,
                    messages=messages,
                    system="""אתה יועץ עסקי ומחקרי מומחה לשוק הישראלי ופלטפורמות דיגיטליות.
אתה עוזר להקים LUMINA - פלטפורמה חברתית לגיל 65+ בישראל.
כתוב בעברית, ברורה ומאורגנת, עם כותרות וסעיפים.
ספק מידע מעמיק, מספרים ריאליים והמלצות פרקטיות.""",
                ) as stream:
                    for event in stream:
                        if (
                            event.type == "content_block_delta"
                            and hasattr(event.delta, "text")
                            and event.delta.type == "text_delta"
                        ):
                            full_response += event.delta.text
                            print(event.delta.text, end="", flush=True)
                break  # הצליח - צא מלולאת retry

            except anthropic.RateLimitError as e:
                wait = 65 * (attempt + 1)
                print(f"\n⏳ Rate limit - ממתין {wait} שניות... (ניסיון {attempt+1}/5)")
                time.sleep(wait)
            except anthropic.APIStatusError as e:
                if e.status_code >= 500:
                    wait = 30 * (attempt + 1)
                    print(f"\n⚠️ שגיאת שרת {e.status_code} - ממתין {wait} שניות...")
                    time.sleep(wait)
                else:
                    raise

        print(f"\n{emoji} סוכן [{domain_name}] סיים.")
        # המתנה בין סוכנים למניעת rate limit
        time.sleep(30)

        result = {
            "domain_id": domain_id,
            "domain_name_he": domain_name,
            "domain_name_en": self.domain["name_en"],
            "emoji": emoji,
            "content": full_response,
            "timestamp": datetime.now().isoformat(),
        }

        output_path = os.path.join(self.output_dir, f"{domain_id}.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {emoji} {domain_name}\n\n")
            f.write(f"*נוצר: {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n\n")
            f.write("---\n\n")
            f.write(full_response)

        print(f"  💾 נשמר: {output_path}")
        return result


class ManagerAgent:
    """מנהל סוכנים - מתאם מחקר בין מספר דומיינים קשורים"""

    def __init__(self, name: str, domains: list, output_dir: str):
        self.name = name
        self.domains = domains
        self.output_dir = output_dir
        self.results = []

    def run(self) -> list:
        """מריץ את כל סוכני הדומיין תחת ניהולו"""
        print(f"\n{'='*60}")
        print(f"🎯 מנהל [{self.name}] מפעיל {len(self.domains)} סוכנים")
        print(f"{'='*60}")

        for domain in self.domains:
            agent = DomainAgent(domain, self.output_dir)
            result = agent.research()
            self.results.append(result)

        print(f"\n✅ מנהל [{self.name}] סיים - {len(self.results)} תחומים נחקרו")
        return self.results


class OrchestratorAgent:
    """סוכן ראשי - מתאם את כל המנהלים ומסנתז את הממצאים"""

    def __init__(self, domains: list, output_dir: str):
        self.domains = domains
        self.output_dir = output_dir
        self.all_results = []

    def _split_into_groups(self) -> list:
        """מחלק את הדומיינים לקבוצות לפי מנהלים"""
        groups = [
            {
                "name": "מנהל עסקי-משפטי",
                "domain_ids": ["legal", "financial", "business_plan"],
            },
            {
                "name": "מנהל שיווק-טכנולוגיה-CRM",
                "domain_ids": ["marketing", "technology", "crm", "website_plan"],
            },
            {
                "name": "מנהל תוכן-קהילה-אימפקט",
                "domain_ids": ["content", "operations", "social_impact", "lesson_plans"],
            },
        ]

        domain_map = {d["id"]: d for d in self.domains}
        result_groups = []

        for group in groups:
            group_domains = [
                domain_map[did]
                for did in group["domain_ids"]
                if did in domain_map
            ]
            if group_domains:
                result_groups.append(
                    {"name": group["name"], "domains": group_domains}
                )

        return result_groups

    def run_sequential(self):
        """מריץ את כל המנהלים ברצף"""
        print("\n" + "=" * 70)
        print("🌟 LUMINA - מערכת מחקר עסקי מולטי-סוכן")
        print("=" * 70)
        print(f"📋 {len(self.domains)} תחומי מחקר | 3 מנהלי סוכנים")
        print("=" * 70)
        print("⏳ ממתין 90 שניות לאיפוס rate limit...")
        time.sleep(90)

        groups = self._split_into_groups()

        for group in groups:
            manager = ManagerAgent(
                name=group["name"],
                domains=group["domains"],
                output_dir=self.output_dir,
            )
            results = manager.run()
            self.all_results.extend(results)

        self._synthesize_report()
        self._build_website()

    def _synthesize_report(self):
        """סינתזת כל הממצאים לדוח מנהלים אחד"""
        print("\n" + "=" * 70)
        print("📊 מסנתז דוח מנהלים כולל...")
        print("=" * 70)

        summaries = "\n\n".join(
            [
                f"## {r['emoji']} {r['domain_name_he']}\n{r['content'][:1500]}..."
                for r in self.all_results
            ]
        )

        synthesis_prompt = f"""על בסיס המחקר הבא שנאסף על ידי סוכני הדומיין השונים של LUMINA,
צור דוח מנהלים מקיף בעברית:

{summaries}

הדוח צריך לכלול:
1. **תקציר מנהלים** - 5 שורות על ה-opportunity
2. **החלטות קריטיות** - 5 ההחלטות החשובות ביותר שיש לקבל
3. **Quick Wins** - 5 פעולות שאפשר להתחיל עכשיו (תוך 30 יום)
4. **לוח זמנים** - מפת דרך ל-12 חודשים
5. **סיכום סיכונים** - 3 הסיכונים הגדולים ביותר ואיך להתמודד
6. **הצעד הבא** - מה לעשות ראשון?

כתוב בצורה ברורה, פרקטית, ומוטת פעולה."""

        print("\n📝 דוח מנהלים:\n")
        synthesis_content = ""

        with client.messages.stream(
            model=ORCHESTRATOR_MODEL,
            max_tokens=4000,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": synthesis_prompt}],
        ) as stream:
            for event in stream:
                if (
                    event.type == "content_block_delta"
                    and hasattr(event.delta, "text")
                    and event.delta.type == "text_delta"
                ):
                    synthesis_content += event.delta.text
                    print(event.delta.text, end="", flush=True)

        report_path = os.path.join(self.output_dir, "00_executive_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 🌟 LUMINA - דוח מנהלים\n\n")
            f.write(f"*נוצר: {datetime.now().strftime('%d/%m/%Y %H:%M')}*\n\n")
            f.write("---\n\n")
            f.write(synthesis_content)
            f.write("\n\n---\n\n## תחומי המחקר שנאספו:\n\n")
            for r in self.all_results:
                f.write(f"- [{r['emoji']} {r['domain_name_he']}]({r['domain_id']}.md)\n")

        print(f"\n\n💾 דוח מנהלים נשמר: {report_path}")
        self._save_index()

    def _build_website(self):
        """מפעיל את WebsiteBuilderAgent אחרי סיום המחקר"""
        plan = next(
            (r["content"] for r in self.all_results if r["domain_id"] == "website_plan"),
            "",
        )
        builder = WebsiteBuilderAgent(
            research_results=self.all_results,
            website_plan=plan,
            output_dir=self.output_dir,
        )
        builder.build()

    def _save_index(self):
        """שומר אינדקס JSON של כל הממצאים"""
        index = {
            "project": "LUMINA - לומינה",
            "generated": datetime.now().isoformat(),
            "domains_researched": len(self.all_results),
            "domains": [
                {
                    "id": r["domain_id"],
                    "name_he": r["domain_name_he"],
                    "name_en": r["domain_name_en"],
                    "file": f"{r['domain_id']}.md",
                }
                for r in self.all_results
            ],
        }

        index_path = os.path.join(self.output_dir, "index.json")
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

        print(f"\n🎉 המחקר הושלם!")
        print(f"📁 כל הקבצים נשמרו ב: {self.output_dir}")
        print(f"\nקבצים שנוצרו:")
        print(f"  📋 00_executive_report.md - דוח מנהלים")
        for r in self.all_results:
            print(f"  {r['emoji']} {r['domain_id']}.md - {r['domain_name_he']}")


class WebsiteBuilderAgent:
    """סוכן בניית אתר - מייצר HTML/CSS/JS מלא לאתר LUMINA"""

    PAGES = [
        {
            "id": "index",
            "name": "דף בית",
            "prompt_addition": """צור דף בית מלא הכולל:
- Hero section עם headline "לומינה - החיים פורחים בכל גיל" ו-CTA "הצטרפי עכשיו"
- 4 כרטיסי פעילות (מדיטציה ויוגה, משחק, ציור, הסיפור שלי)
- סקציית יתרונות (3 יתרונות)
- המלצות (2-3 ציטוטים מדומים)
- Footer עם כל הפרטים""",
        },
        {
            "id": "activities",
            "name": "פעילויות",
            "prompt_addition": """צור עמוד פעילויות מלא הכולל:
- כותרת ראשית
- 4 כרטיסים גדולים עם תיאור מפורט לכל פעילות:
  1. מדיטציה ויוגה - תיאור, יתרונות, מתי
  2. משחק - תיאור, סוגי משחקים, יתרונות קוגניטיביים
  3. ציור - תיאור, מה תלמדו, לא צריך ניסיון
  4. הסיפור שלי - תיאור מרגש, כיצד זה עובד
- CTA בתחתית""",
        },
        {
            "id": "about",
            "name": "אודות",
            "prompt_addition": """צור עמוד אודות הכולל:
- סיפור LUMINA - למה הוקמה
- חזון ומשימה
- ערכים (3-4 ערכי מפתח)
- צוות (2-3 חברי צוות מדומים עם תפקידים)
- מספרים (חברים, שיעורים, ערים)""",
        },
        {
            "id": "join",
            "name": "הצטרפו",
            "prompt_addition": """צור עמוד הצטרפות הכולל:
- תמחור: חינמי (3 שיעורים/חודש), בסיסי (₪79/חודש), פרימיום (₪149/חודש)
- טבלת השוואה בין המסלולים
- טופס הרשמה פשוט (שם, טלפון, אימייל, עיר)
- הסבר על תהליך ההצטרפות""",
        },
        {
            "id": "contact",
            "name": "צור קשר",
            "prompt_addition": """צור עמוד צור קשר הכולל:
- טלפון ו-WhatsApp גדול ובולט (חשוב לגיל 65+)
- כפתור WhatsApp ישיר
- אימייל
- טופס פנייה פשוט
- שעות פעילות""",
        },
    ]

    def __init__(self, research_results: list, website_plan: str, output_dir: str):
        self.research_results = research_results
        self.website_plan = website_plan
        self.output_dir = output_dir
        self.website_dir = os.path.join(output_dir, "website")
        os.makedirs(self.website_dir, exist_ok=True)

    def _get_context(self) -> str:
        """מסכם את המחקר הרלוונטי לבניית האתר"""
        relevant = ["marketing", "content", "website_plan"]
        context_parts = []
        for r in self.research_results:
            if r["domain_id"] in relevant:
                context_parts.append(
                    f"### {r['domain_name_he']}\n{r['content'][:800]}"
                )
        return "\n\n".join(context_parts)

    def _generate_css(self) -> str:
        """מייצר CSS מרכזי"""
        print("\n🎨 מייצר style.css...")
        prompt = """צור קובץ CSS מלא לאתר LUMINA - פלטפורמה לגיל 65+ בישראל.

דרישות עיצוב:
- RTL מלא (direction: rtl, font-family עברית)
- פונט בסיס: 18px (גדול לנגישות)
- פלטת צבעים: עיקרי #E8735A (טרקוטה חמה), משני #2C7873 (ירוק-כחול), רקע #FFF9F5
- כפתורים: גובה מינימלי 50px, padding נדיב, border-radius 30px
- ניגודיות גבוהה בכל הטקסטים
- Responsive (mobile-first)
- Navigation: ברור, גדול, sticky
- Cards: צל עדין, border-radius 16px
- Hero: gradient חמה, טקסט לבן
- Sections: padding נדיב (60px-80px)
- Footer: כהה, מאורגן

כתוב CSS מלא ומפורט עם:
- Reset/Base
- Variables (CSS custom properties)
- Layout (nav, hero, sections, footer)
- Components (cards, buttons, forms, pricing table)
- Utilities
- Media queries (mobile 768px)

החזר רק קוד CSS בלי הסברים."""

        css_content = ""
        with client.messages.stream(
            model=DOMAIN_AGENT_MODEL,
            max_tokens=6000,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for event in stream:
                if (
                    event.type == "content_block_delta"
                    and hasattr(event.delta, "text")
                    and event.delta.type == "text_delta"
                ):
                    css_content += event.delta.text

        # נקה ```css markers אם יש
        css_content = css_content.replace("```css", "").replace("```", "").strip()

        css_path = os.path.join(self.website_dir, "style.css")
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_content)
        print(f"  💾 נשמר: style.css")
        return css_content

    def _generate_js(self) -> str:
        """מייצר JavaScript בסיסי"""
        print("\n⚡ מייצר script.js...")
        prompt = """צור קובץ JavaScript בסיסי לאתר LUMINA.

כלול:
1. Mobile menu toggle (hamburger)
2. Smooth scroll לעוגנים
3. כפתור WhatsApp floating (מספר דמה: 972501234567)
4. טופס הרשמה - validation בסיסי + הודעת תודה
5. Scroll-to-top button
6. הדגשת פריט ניווט פעיל לפי URL

כתוב JS נקי, vanilla (ללא libraries), עם תגובות בעברית.
החזר רק קוד JS בלי הסברים."""

        js_content = ""
        with client.messages.stream(
            model=DOMAIN_AGENT_MODEL,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for event in stream:
                if (
                    event.type == "content_block_delta"
                    and hasattr(event.delta, "text")
                    and event.delta.type == "text_delta"
                ):
                    js_content += event.delta.text

        js_content = js_content.replace("```javascript", "").replace("```js", "").replace("```", "").strip()

        js_path = os.path.join(self.website_dir, "script.js")
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"  💾 נשמר: script.js")
        return js_content

    def _generate_page(self, page: dict, context: str) -> None:
        """מייצר עמוד HTML אחד"""
        page_id = page["id"]
        page_name = page["name"]
        print(f"\n🌐 בונה {page_name} ({page_id}.html)...")

        nav_links = """
        <nav class="main-nav">
            <div class="nav-container">
                <a href="index.html" class="logo">🌟 לומינה</a>
                <button class="menu-toggle" id="menuToggle">☰</button>
                <ul class="nav-links" id="navLinks">
                    <li><a href="index.html">בית</a></li>
                    <li><a href="activities.html">פעילויות</a></li>
                    <li><a href="about.html">אודות</a></li>
                    <li><a href="join.html">הצטרפו</a></li>
                    <li><a href="contact.html">צור קשר</a></li>
                </ul>
            </div>
        </nav>"""

        prompt = f"""צור עמוד HTML מלא עבור "{page_name}" של אתר LUMINA.

הקשר מחקרי:
{context[:600]}

תוכן העמוד:
{page["prompt_addition"]}

דרישות טכניות:
- HTML5 מלא עם DOCTYPE, lang="he", dir="rtl", charset UTF-8
- כלול בדיוק את ה-nav הזה (אל תשנה!):
{nav_links}
- קשר ל: <link rel="stylesheet" href="style.css">
- קשר ל: <script src="script.js"></script> לפני </body>
- title: "[שם העמוד] | לומינה - רשת פעילות לגיל 65+"
- meta description מתאים
- כל הטקסטים בעברית
- כפתורי CTA גדולים ונגישים
- footer עם: © 2026 לומינה | טלפון: 03-1234567 | info@lumina.co.il

החזר רק קוד HTML מלא, בלי הסברים."""

        html_content = ""
        with client.messages.stream(
            model=DOMAIN_AGENT_MODEL,
            max_tokens=5000,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for event in stream:
                if (
                    event.type == "content_block_delta"
                    and hasattr(event.delta, "text")
                    and event.delta.type == "text_delta"
                ):
                    html_content += event.delta.text
                    print(".", end="", flush=True)

        html_content = html_content.replace("```html", "").replace("```", "").strip()

        html_path = os.path.join(self.website_dir, f"{page_id}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\n  💾 נשמר: {page_id}.html")

    def build(self):
        """בונה את האתר המלא"""
        print("\n" + "=" * 70)
        print("🌐 WebsiteBuilderAgent - בונה את אתר LUMINA")
        print("=" * 70)
        print(f"📄 {len(self.PAGES)} עמודים + CSS + JS")

        context = self._get_context()
        self._generate_css()
        self._generate_js()

        for page in self.PAGES:
            self._generate_page(page, context)

        print(f"\n✅ האתר נבנה בהצלחה!")
        print(f"📁 קבצי האתר: {self.website_dir}")
        print(f"\nעמודים שנוצרו:")
        for page in self.PAGES:
            print(f"  🌐 {page['id']}.html - {page['name']}")
        print(f"  🎨 style.css")
        print(f"  ⚡ script.js")
        print(f"\n💡 לפתיחה: פתח {self.website_dir}/index.html בדפדפן")
