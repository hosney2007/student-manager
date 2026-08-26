# تجهيز المشروع للنشر على Vercel مع Supabase

## شنو تزاد في المشروع

- **تسجيل دخول (Login)**: كل صفحات المشروع محمية دروك، لازم تعمل login باش تدخل. عندك يوزر admin يتزاد أوتوماتيك أول مرة يخدم فيها السيرفر (شوف تحت).
- **بحث (Search)**: صفحة الطلبة (`/student`) وصفحة المجموعات (`/group`) فيهم فورم بحث (بالاسم أو رقم الطالب أو رقم الولي بالنسبة للطلبة).

## 1) Supabase — جيب رابط قاعدة البيانات

1. ادخل لمشروعك في supabase.com
2. `Project Settings` → `Database` → `Connection string` → اختار `URI`
3. استعمل الـ **Transaction pooler** (بورت `6543`) خاصة إلي باش تخدم على Vercel (serverless)
4. الرابط باش يكون شبه:
   `postgresql://postgres:[YOUR-PASSWORD]@aws-0-xxxx.pooler.supabase.com:6543/postgres`

ملاحظة: المشروع يقبل زادة `postgres://` (كيما Supabase يعطيها بالزمان) ويحولها أوتوماتيك لـ `postgresql://`.

## 2) متغيرات البيئة (Environment Variables)

عندك ملف `.env.example` فيه القائمة، خاصك تزيدهم في Vercel:

| المتغير | الشرح |
|---|---|
| `DATABASE_URL` | رابط Supabase (URI) |
| `SECRET_KEY` | نص عشوائي طويل (لأمان الجلسات) |
| `ADMIN_USERNAME` | يوزر الأدمن الأول (افتراضي `admin`) |
| `ADMIN_PASSWORD` | باسورد الأدمن الأول (افتراضي `admin123` — **بدلها وجوب**) |

## 3) رفع المشروع على GitHub

```bash
git init
git add .
git commit -m "init"
git remote add origin <رابط الريبو متاعك>
git push -u origin main
```

(ملف `.gitignore` مجهز باش ميرفعش `instance/` و`__pycache__` و`.env`)

## 4) النشر على Vercel

1. روح لـ vercel.com → `Add New Project` → اختار الريبو
2. Vercel باش يكتشف `vercel.json` أوتوماتيك (Python runtime)
3. في `Settings → Environment Variables` زيد المتغيرات الأربعة فوق (`DATABASE_URL`, `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`)
4. Deploy

أول ما السيرفر يخدم، `db.create_all()` باش يخلق الجداول في Supabase، وباش يزيد يوزر admin أوتوماتيك (بالمتغيرات إلي حطيت أو بالافتراضي `admin` / `admin123`).

## 5) بعد النشر

- ادخل لـ `https://<your-app>.vercel.app/login`
- دخل بـ `ADMIN_USERNAME` / `ADMIN_PASSWORD` إلي حطيت
- **نصيحة**: بدل باسورد الأدمن الافتراضي في متغيرات Vercel قبل ما تعمل deploy فعلي (لا تخليه `admin123` في الإنتاج)

## هيكلة الـ deploy (شنية تزادت)

- `requirements.txt` — الحزم المطلوبة (Flask, SQLAlchemy, Flask-Login, psycopg2-binary...)
- `vercel.json` — يوجه كل الطلبات لـ `api/index.py`
- `api/index.py` — نقطة الدخول إلي Vercel يشغلها (import للـ Flask app)
- `config.py` — يقرا `DATABASE_URL` من env ويشتغل مع Postgres/Supabase
- `models/user.py` + `routes/auth.py` + `templates/login.html` — نظام تسجيل الدخول

## ملاحظة مهمة

قاعدة `sqlite` (ملف `instance/database.db`) تخدم محليا برك للتجربة. على Vercel نظام الملفات read-only، فـ **لازم** `DATABASE_URL` يشاور لـ Supabase وإلا التطبيق ميحتفظش بالبيانات.
