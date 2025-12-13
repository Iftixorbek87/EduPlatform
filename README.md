# EduPlatform — Zamonaviy Onlayn Kurs Platformasi  


## Loyiha xususiyatlari

| Xususiyat                        | Holati   | Tavsif |
|----------------------------------|--------|--------|
| Ro‘yxatdan o‘tish / Kirish       | Done   | Email bilan, rasm yuklash imkoniyati |
| O‘qituvchi va Talaba rollari    | Done   | `is_teacher` maydoni orqali |
| Kurs yaratish va boshqarish      | Done   | Admin panel + saytdan (kelajakda) |
| Kursga yozilish (Enroll)         | Done   | Bir marta bosishda |
| Video darslar (YouTube embed)    | Done   | Responsive iframe |
| Dars progressini saqlash         | Done   | Qaysi darsgacha o‘qigan – eslab qoladi |
| Kurs tugaganda PDF sertifikat    | Done   | ReportLab bilan avtomatik generatsiya |
| Responsive dizayn                | Done   | Mobile + Desktop uchun moslashtirilgan |
| Admin panel (Django Admin)       | Done   | To‘liq boshqaruv |

---

## Texnologiyalar

- **Backend**: Django 5.2  
- **Database**: SQLite (development), PostgreSQL (production uchun tayyor)  
- **Frontend**: Bootstrap 5, Custom CSS  
- **PDF generatsiya**: ReportLab  
- **Authentication**: Django Custom User (email bilan)  
- **Deployment**: Render, PythonAnywhere, Heroku (tayyor)  

---



## Qanday ishlatish kerak?

```bash
# 1. Repositoryni klonlash
git clone https://github.com/Iftixorbek07/EduUz.git
cd EduUz

# 2. Virtual muhit yaratish
python -m venv .venv
.venv\Scripts\activate

# 3. Kerakli paketlarni o‘rnatish
pip install -r requirements.txt

# 4. Migratsiyalarni qo‘llash
python manage.py makemigrations
python manage.py migrate

# 5. Superuser yaratish
python manage.py createsuperuser

# 6. Serverni ishga tushirish
python manage.py runserver
Brauzerda och: http://127.0.0.1:8000
Admin panel: http://127.0.0.1:8000/admin/

Admin paneldan foydalanish

O‘zingni is_teacher = True qil
Kategoriya → Kurs → Darslar → Testlar qo‘sh
Talaba sifatida ro‘yxatdan o‘t → kursga yozil → o‘qi → sertifikat ol!



Muallif
Iftixorbek Odilov
Backend Developer | Django Enthusiast

GitHub: @Iftixorbek87
Telegram: @Iftixorbek_Odilov
Email: odiloviftixorbek@gmail.com
Tel : +998943980949


Agar loyiha yoqsa – ⭐ Star bosing! Bu menga katta motivatsiya beradi!
