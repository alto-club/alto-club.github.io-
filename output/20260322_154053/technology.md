# 💻 פלטפורמה טכנולוגית

*נוצר: 22/03/2026 16:01*

---

# דוח מחקר טכנולוגי מקיף - פרויקט LUMINA

## פלטפורמה חברתית-תרבותית לגיל 65+ בישראל

---

# חלק א': Stack טכנולוגי מומלץ

## 1.1 ארכיטקטורה כללית מומלצת

לפני הפירוט הטכני, חשוב להגדיר את גישת הפיתוח:

**המלצה: Hybrid Architecture - Progressive Web App (PWA) + Native App**

הסיבות:
- PWA מאפשר גישה מדפדפן ללא הורדה (חסם גדול לגיל 65+)
- Native App מספק חוויה מיטבית למשתמשים מתקדמים יותר
- קוד בסיס אחד = עלות תחזוקה נמוכה יותר

---

## 1.2 Frontend

### מסגרת עבודה ראשית: **Next.js 14+**

```
יתרונות ל-LUMINA:
✓ Server-Side Rendering (SSR) - טעינה מהירה גם בחיבור איטי
✓ תמיכה מובנית ב-RTL (ימין לשמאל לעברית/ערבית)
✓ אופטימיזציה אוטומטית של תמונות
✓ SEO מצוין - חשוב לגיוס משתמשים חדשים
✓ קהילת מפתחים גדולה בישראל
```

### ספריית UI: **Tailwind CSS + Radix UI**

```
Radix UI - למה?
✓ Accessibility-first מובנה (ARIA labels, keyboard navigation)
✓ רכיבים בסיסיים נגישים לפי WCAG 2.1
✓ אפשר להתאים עיצוב לחלוטין
✓ תמיכה מלאה ב-RTL
```

### ספריות נוספות חיוניות:

| ספרייה | שימוש | סיבה |
|--------|-------|-------|
| i18next | תרגום עברית/ערבית | תמיכה מלאה ב-RTL switching |
| React Query (TanStack) | ניהול state ו-data fetching | cache חכם = פחות טעינות |
| Framer Motion | אנימציות עדינות | UX נעים, ללא הצפה |
| React Hook Form | טפסי רישום | ולידציה נגישה עם הודעות שגיאה ברורות |
| Embla Carousel | גלריה ציור | נגיש, קל לתפעול |

---

## 1.3 Backend

### המלצה ראשית: **Node.js + NestJS**

```
למה NestJS ולא Express פשוט?
✓ ארכיטקטורה מודולרית - אפשר להוסיף מודולים (ציור, יוגה, סיפורים) בנפרד
✓ TypeScript מובנה - פחות באגים, קוד בטוח יותר
✓ תיעוד API אוטומטי (Swagger) - קל לצוות לשמור על עקביות
✓ מפתחים NestJS נפוצים בשוק הישראלי
✓ Dependency Injection - בדיקות (tests) קלות יותר
```

### שירותים ספציפיים לפי מודול:

```
מודול וידאו (מדיטציה/יוגה):
├── Media Server: Cloudflare Stream / Mux.com
└── Live Streaming: Agora.io (RTK) - תמיכה בעברית, שרתים באירופה

מודול "הסיפור שלי":
├── עיבוד תמונות: Sharp (Node.js) + Cloudinary
└── עיבוד טקסט: TipTap Editor (עשיר, נגיש, RTL מלא)

מודול התראות:
├── Push Notifications: Firebase Cloud Messaging (FCM)
├── SMS: Infobip / MessageBird - בישראל
└── Email: SendGrid

מודול תשלומים (מנוי):
└── Tranzila / Cardcom - מעבדי תשלום ישראלים, עמידה בתקנות PCI-DSS
```

---

## 1.4 Database

### ארכיטקטורת נתונים מומלצת - שכבתית:

```
┌─────────────────────────────────────────┐
│  PostgreSQL (Supabase)                  │
│  נתונים מובנים:                         │
│  - משתמשים ופרופילים                   │
│  - רישומים לשיעורים                    │
│  - קהילות וחברויות                     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Redis (Upstash - Serverless)           │
│  מטמון וביצועים:                        │
│  - Session Management                  │
│  - לוח שיעורים (cache)                │
│  - Online users count                  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  MongoDB Atlas                          │
│  תוכן דינמי:                            │
│  - סיפורי חיים (מבנה גמיש)             │
│  - תגובות ותגיות                       │
│  - יומן פעילות                          │
└─────────────────────────────────────────┘
```

### למה Supabase ולא Firebase?

| קריטריון | Supabase | Firebase |
|---------|---------|---------|
| מיקום שרתים | EU (Frankfurt) ✓ | US בלבד |
| GDPR / חוק הגנת פרטיות ישראלי | מלא ✓ | מורכב |
| SQL מלא | כן ✓ | לא |
| Real-time | כן ✓ | כן |
| עלות ב-scale | נמוכה יותר ✓ | גבוהה יותר |
| Open Source | כן ✓ | לא |

---

## 1.5 Cloud & Infrastructure

### המלצה: **AWS (אירלנד/פרנקפורט) + Cloudflare**

```
AWS Services הנדרשים:
├── EC2 / ECS (Docker containers) - שרתי אפליקציה
├── RDS (PostgreSQL managed) - בסיס נתונים
├── S3 - אחסון תמונות וסיפורים
├── CloudFront CDN - הגשת תוכן מהיר
├── SES - שליחת emails
├── WAF - הגנה מפני מתקפות
└── Backup automatico - גיבוי יומי אוטומטי

Cloudflare:
├── DNS ו-SSL certificate
├── DDoS protection
├── Cloudflare Stream - וידאו (מחיר: $5/1000 דקות)
└── Edge caching - ביצועים טובים בכל ישראל
```

---

# חלק ב': UX/UI לגיל 65+ - Best Practices

## 2.1 עקרונות עיצוב ליבה

### טיפוגרפיה:

```css
/* המלצות גודל פונט ל-LUMINA */

--font-base: 18px;        /* בסיס (רגיל = 16px, אנחנו מגדילים) */
--font-body: 18-20px;     /* טקסט גוף */
--font-subtitle: 22-24px; /* כותרות משנה */
--font-title: 28-32px;    /* כותרות ראשיות */
--font-hero: 36-42px;     /* כותרות ראשה */

/* פונט מומלץ לעברית */
font-family: 'Assistant', 'Heebo', sans-serif;
/* שניהם: קריאות גבוהה, תמיכה מלאה ב-RTL, חינמיים ב-Google Fonts */

/* מרווח שורות */
line-height: 1.6-1.8;    /* נוחות קריאה מוגברת */
letter-spacing: 0.01em;  /* מרווח קל בין אותיות */
```

### ניגודיות צבעים:

```
דרישת WCAG AA (מינימום לפלטפורמה):
✓ יחס ניגודיות טקסט רגיל: 4.5:1 לפחות
✓ יחס ניגודיות טקסט גדול: 3:1 לפחות

המלצה ל-LUMINA - WCAG AAA (מעל הנדרש):
✓ יחס ניגודיות: 7:1

פלטת צבעים מוצעת:
├── רקע ראשי: #FAFAF8 (לבן-שמנת, לא לבן טהור - פחות עומס על עיניים)
├── טקסט ראשי: #1A1A2E (כמעט שחור - ניגודיות 15:1)
├── צבע מותג LUMINA: #6B48FF (סגול-כחול - אנרגטי, רוחני)
├── Accent: #FF6B6B (אדום-כתום רך - קריאה לפעולה)
├── Success: #2ECC71 (ירוק)
└── Warning: #F39C12 (כתום)
```

### אזורי לחיצה (Touch Targets):

```
תקן WCAG 2.1 - מינימום: 44x44px
המלצה ל-65+: 56x56px לפחות
מרווח בין כפתורים: מינימום 12px

כפתורי CTA ראשיים (הירשם, הצטרף לשיעור):
→ גובה: 56-64px
→ רוחב: מינימום 200px
→ padding: 16px 32px
→ border-radius: 12px (מעוגל - תחושה ידידותית)
```

---

## 2.2 עקרונות ניווט

### מבנה ניווט מומלץ:

```
ניווט עיקרי - מקסימום 5 פריטים:
┌─────────────────────────────────────────┐
│  🏠 בית  |  📅 שיעורים  |  🎨 גלריה  │
│  📖 סיפורים  |  👤 הפרופיל שלי        │
└─────────────────────────────────────────┘

כללים:
✓ אייקון + טקסט תמיד (לא רק אייקון)
✓ פריט פעיל - מובחן בבירור (צבע + underline)
✓ Breadcrumbs בכל עמוד פנימי
✓ כפתור "חזור" בולט בכל מסך
✓ ללא dropdown מורכב - תפריטים שטוחים בלבד
```

### עקרונות UX נוספים חיוניים:

```
אישורי פעולה:
✓ "הרישום לשיעור יוגה ביום ד' הצליח! 📧 נשלח אישור לאימייל"
✓ Undo option - 5 שניות לביטול פעולה (מניעת טעויות)

טפסים:
✓ שדה אחד לכל שורה (לא טפסים דחוסים)
✓ Label תמיד מעל השדה, לא בתוכו (placeholder נעלם בהקלדה)
✓ הודעות שגיאה בצד השדה, בצבע אדום + אייקון
✓ לא רק צבע לציון שגיאה (עבור עיוורי צבעים)

העמסת מידע:
✗ לא יותר מ-3 פעולות אפשריות בכל מסך
✗ ללא Infinite Scroll - עדיף Pagination עם כפתורים ברורים
✗ ללא Auto-play בווידאו
✓ "מצב פשוט" - אפשרות להסתיר תכונות מתקדמות
```

---

## 2.3 נגישות טכנית

```
HTML Semantics:
✓ שימוש ב-<main>, <nav>, <article>, <section>, <header>
✓ Heading hierarchy: H1 → H2 → H3 (לא דילוג)
✓ Alt text לכל תמונה (כולל AI-generated descriptions)
✓ aria-label לכל כפתור פונקציונלי
✓ focus-visible ברור לניווט מקלדת
✓ Skip-to-content link

תמיכה בטכנולוגיות עזר:
✓ Screen readers: NVDA, VoiceOver, TalkBack
✓ גדילת פונט ב-browser עד 200% ללא שבירת layout
✓ Windows High Contrast Mode
✓ תמיכה ב-keyboard navigation מלא
```

---

# חלק ג': תכונות חיוניות - פירוט טכני

## 3.1 לוח שיעורים ורישום

### ארכיטקטורת מסד נתונים:

```sql
-- טבלאות ליבה
CREATE TABLE classes (
  id UUID PRIMARY KEY,
  title VARCHAR(200) NOT NULL,          -- "יוגה בוקר עם מרים"
  type ENUM('yoga','meditation','art',
            'story','game'),
  instructor_id UUID REFERENCES users,
  scheduled_at TIMESTAMP WITH TIME ZONE,
  duration_minutes INTEGER,
  max_participants INTEGER DEFAULT 20,
  current_participants INTEGER DEFAULT 0,
  platform ENUM('zoom','in_person',
                'lumina_live'),
  meeting_link VARCHAR(500),
  description TEXT,
  difficulty_level ENUM('beginner',
                       'intermediate'),
  is_recurring BOOLEAN DEFAULT FALSE,
  recurrence_rule VARCHAR(100),         -- RRULE format
  thumbnail_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE registrations (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  class_id UUID REFERENCES classes,
  registered_at TIMESTAMP DEFAULT NOW(),
  reminder_sent BOOLEAN DEFAULT FALSE,
  attendance_confirmed BOOLEAN DEFAULT FALSE,
  UNIQUE(user_id, class_id)
);
```

### זרם רישום מומלץ (User Flow):

```
שלב 1: המשתמש רואה שיעור בלוח
   ↓
שלב 2: לחיצה על "הצטרף לשיעור" (כפתור גדול וברור)
   ↓
שלב 3: popup קצר: "שיעור יוגה עם מרים - יום ד' 10:00. להצטרף?"
   [כן, אני רוצה להצטרף] [לא כרגע]
   ↓
שלב 4: אישור מידי + Email + SMS (אם הפעיל)
   ↓
שלב 5: תזכורת 24 שעות לפני + 1 שעה לפני
   ↓
שלב 6: ביום השיעור - כפתור "כניסה לשיעור" בולט בדף הבית
```

---

## 3.2 מודול וידאו - מדיטציה ויוגה

### שכבות הפתרון:

```
שכבה 1 - ספריית VOD (תוכן מוקלט):
├── ספק: Cloudflare Stream
├── מחיר: $5 לכל 1,000 דקות שנצפו
├── תכונות: Adaptive bitrate, Hebrew subtitles
└── שחקן מותאם: Video.js עם ממשק מוגדל

שכבה 2 - שיעורים חיים (Live):
├── ספק: Agora.io Web SDK
├── מחיר: $0.0099 לדקת משתמש
├── תכונות: רזולוציה 720p, מקסימום 1000 משתתפים
├── Screen sharing - מדריך יכול להציג תרגיל
└── Chat בצד - שאלות בכתב בזמן שיעור

שחקן וידאו מותאם לגיל 65+:
```

```jsx
// רכיב VideoPlayer מותאם ל-LUMINA
const LuminaVideoPlayer = ({ src, title }) => {
  return (
    <div className="video-container">
      {/* כפתורי שליטה גדולים */}
      <button className="play-btn" style={{fontSize: '24px', 
                         padding: '16px 32px'}}>
        ▶ הפעל
      </button>
      
      {/* בקר עוצמה גדול */}
      <input type="range" 
             className="volume-slider"
             style={{height: '24px'}} />
      
      {/* כתוביות תמיד פעילות כברירת מחדל */}
      <track kind="subtitles" 
             src={subtitlesUrl} 
             srcLang="he" 
             default />
      
      {/* כפתור מסך מלא בולט */}
      <button style={{fontSize: '20px'}}>
        🔲 מסך מלא
      </button>
    </div>
  );
};
```

---

## 3.3 גלריה ציור

### ארכיטקטורת הגלריה:

```
זרם העלאת ציור:
├── העלאה: מצלמה (mobile) / בחירת קובץ (desktop)
├── עיבוד אוטומטי: Sharp.js
│   ├── הקטנה ל-1920x1080 מקסימום
│   ├── יצירת thumbnail 400x300
│   ├── שמירה ב-WebP + JPEG backup
│   └── Metadata: EXIF stripping (פרטיות)
├── אחסון: AWS S3 (תיקיית user/{userId}/artwork/)
└── CDN: Cloudflare (הגשה מהירה)

מסד נתונים:
```

```sql
CREATE TABLE artworks (
  id UUID PRIMARY KEY,
  creator_id UUID REFERENCES users,
  title VARCHAR(200),
  description TEXT,
  technique VARCHAR(100),      -- "אקוורל", "עיפרון", "דיגיטלי"
  created_date DATE,
  image_url VARCHAR(500),      -- S3 URL
  thumbnail_url VARCHAR(500),
  is_public BOOLEAN DEFAULT TRUE,
  workshop_id UUID,            -- אם נוצר בסדנה
  likes_count INTEGER DEFAULT 0,
  comments_count INTEGER DEFAULT 0,
  tags TEXT[],                 -- מערך תגיות
  created_at TIMESTAMP DEFAULT NOW()
);
```

```
פיצ'ר מיוחד - "הציור של השבוע":
└── אוטומטי: ציור עם הכי הרבה Likes השבוע
    מופיע בדף הבית עם שם האמן + תיאור קצר
    
אינטראקציה חברתית:
├── 👏 מחיאות כפיים (במקום "לייק" - יותר חם ומעודד)
├── 💬 תגובות טקסט (עם מודרציה)
└── 🔗 שיתוף - WhatsApp, Email, Download
```

---

## 3.4 מודול "הסיפור שלי" - ליבת LUMINA

### מבנה הסיפור:

```javascript
// מודל נתונים בגמישות MongoDB
{
  _id: ObjectId,
  authorId: UUID,
  title: String,            // "ילדותי בחיפה"
  coverImage: String,       // URL
  
  chapters: [{
    order: Number,
    title: String,          // "הבית ברחוב הרצל"
    content: {
      type: "rich_text",    // עורך TipTap
      html: String,
      plainText: String
    },
    media: [{
      type: "image" | "audio" | "video",
      url: String,
      caption: String,      // כיתוב לנגישות
      year: Number,         // שנת הצילום
      location: String
    }],
    createdAt: Date,
    updatedAt: Date
  }],
  
  visibility: "private" | "friends" | "community",
  tags: ["ילדות", "שנות ה-60", "ירושלים"],
  
  stats: {
    views: Number,
    hearts: Number,
    commentsCount: Number
  },
  
  isComplete: Boolean,
  publishedAt: Date
}
```

### עורך הסיפור - TipTap Configuration:

```javascript
// הגדרת עורך עשיר לגיל 65+
const StoryEditor = useEditor({
  extensions: [
    StarterKit,
    // כותרות גדולות
    Heading.configure({ levels: [1, 2, 3] }),
    // העלאת תמונות ישירות בתוך הטקסט
    Image.configure({ allowBase64: false }),
    // הקלטת קול ישירות
    AudioRecorder,        // extension מותאם
    // שמירה אוטומטית
    AutoSave.configure({ 
      debounce: 2000,     // שמירה כל 2 שניות
      onSave: saveToServer 
    }),
    // RTL support
    TextDirection.configure({ types: ['heading', 'paragraph'] }),
  ],
  
  editorProps: {
    attributes: {
      style: 'font-size: 18px; line-height: 1.8;',
      lang: 'he',
      dir: 'rtl',
    }
  }
});
```

### פיצ'רים מיוחדים למודול:

```
1. "עוזר כתיבה" - שאלות מנחות:
   - "מה היה הריח האהוב עליך בבית הילדות?"
   - "מי היה המורה שהשפיע עליך ביותר?"
   - "מה עשיתם בשבתות?"
   → שאלות מוצגות כהצעות, לא כחובה

2. Timeline View:
   → סיפורים מסודרים על ציר זמן אינטראקטיבי
   → ניתן לסנן לפי עשורים

3. "מנחה AI" (אופציונלי - Phase 2):
   → GPT-4 API בעברית
   → מציע המשך משפטים
   → תיקון כתיב עדין
   → מחיר: ~$0.01 לאינטראקציה

4. ייצוא לספר:
   → PDF מעוצב בסגנון ספר אמיתי
   → אפשרות להדפסה דרך שירות חיצוני (Blurb.com)
```

---

## 3.5 פרופיל אישי וקהילה

```sql
-- פרופיל מורחב
CREATE TABLE user_profiles (
  user_id UUID PRIMARY KEY,
  display_name VARCHAR(100),
  avatar_url VARCHAR(500),
  bio TEXT,                          -- סיפור קצר
  city VARCHAR(100),
  birth_year INTEGER,                -- לא תאריך מלא
  interests TEXT[],                  -- ['ציור', 'יוגה', 'גינון']
  languages TEXT[] DEFAULT '{he}',   -- ['he', 'ar']
  
  -- נגישות אישית
  font_size_preference 
    ENUM('medium','large','xlarge') DEFAULT 'large',
  high_contrast BOOLEAN DEFAULT FALSE,
  
  -- הגדרות תקשורת
  whatsapp_number VARCHAR(20),       -- אינטגרציה מתוכננת
  wants_sms_reminders BOOLEAN DEFAULT TRUE,
  wants_email_digest BOOLEAN DEFAULT TRUE,
  
  -- סטטיסטיקות
  classes_attended INTEGER DEFAULT 0,
  stories_published INTEGER DEFAULT 0,
  artworks_shared INTEGER DEFAULT 0,
  
  joined_at TIMESTAMP DEFAULT NOW()
);

-- מערכת קהילות
CREATE TABLE communities (
  id UUID PRIMARY KEY,
  name VARCHAR(200),                 -- "קבוצת יוגה ת"א", "אמנים חיפה"
  type ENUM('city','interest',
            'class_group'),
  description TEXT,
  members_count INTEGER DEFAULT 0,
  is_private BOOLEAN DEFAULT FALSE
);
```

---

# חלק ד': פתרונות Ready-Made vs פיתוח מאפס

## 4.1 השוואה מקיפה

### אפשרות א': Mighty Networks

```
יתרונות:
✓ מוכן מהיום הראשון
✓ כולל קהילה, קורסים, אירועים
✓ אפליקציה Native כלולה
✓ תמיכה טכנית

חסרונות קריטיים ל-LUMINA:
✗ אין תמיכה ב-RTL (עברית מוגבלת מאוד)
✗ לא ניתן להתאים UX לגיל 65+
✗ מודול "הסיפור שלי" לא קיים
✗ תמחור: $119-$360/חודש
✗ Lock-in: קשה להוציא נתונים
✗ ה-UX הבסיסי מורכב מדי לקהל היעד

ציון כולל ל-LUMINA: 3/10 ❌
```

### אפשרות ב': Circle.so

```
יתרונות:
✓ עיצוב נקי ומודרני
✓ API זמין
✓ אינטגרציה עם Zoom

חסרונות:
✗ RTL - חלקי בלבד
✗ אין מודולים ייחודיים (ציור, סיפורים)
✗ UX - לא מותאם לגיל 65+
✗ $89-$399/חודש
✗ כל התוכן על שרתי Circle - בעיית פרטיות
✗ תלות מלאה בספק

ציון כולל ל-LUMINA: 4/10 ❌
```

### אפשרות ג': WordPress + BuddyPress + תוספים

```
יתרונות:
✓ גמיש יחסית
✓ עברית מובנית
✓ קהילת WordPress ישראלית גדולה
✓ עלות נמוכה בהתחלה

חסרונות:
✗ אבטחה - WordPress = מטרה מועדפת להאקרים
✗ ביצועים - איטי עם תוספים רבים
✗ UX - מוגבל בהתאמה עמוקה
✗ מודולי וידאו ו-Timeline - פתרונות חלשים
✗ תחזוקה - דורש עדכונים תכופים ומומחה

ציון כולל ל-LUMINA: 5/10 ⚠️
```

### אפשרות ד': Hybrid - Low-Code + Custom Modules ✅

```
גישה מומלצת לשלב א':
├── Supabase - Backend as a Service (Database + Auth + Storage)
│   חוסך: 3-4 חודשי פיתוח backend
├── Next.js Frontend - פיתוח מותאם לח