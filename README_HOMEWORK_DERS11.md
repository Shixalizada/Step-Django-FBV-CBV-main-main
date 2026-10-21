# Dərs 11 - Blogda tam CRUD

Bu paket göndərilən `Step-Django-FBV-CBV-main` arxivinin üzərində hazırlanıb. Arxiv **Dərs 12**
funksiyalarını artıq ehtiva etdiyindən onların (giriş, müəllif icazələri, CBV və s.) üzərinə uyğun
əlavələr edilib; layihə köhnə dərsə geri qaytarılmayıb.

## Görülən işlər

1. **Post silmə** - GET təsdiq, POST silmə, uğurlu silmədən sonra ana səhifəyə yönləndirmə.
   CBV-lərin `post_id` URL parametrini qəbul etməsi də düzəldilib.
2. **Əlaqə formu** - mövcud `ContactForm`, `ContactMessage` və `0010_contactmessage` saxlanıb;
   email və minimum 10 simvol yoxlamaları, bazada saxlanma, admin siyahısı testlərlə əhatə edilib.
3. **Başlıq yoxlaması** - mövcud `clean_title()` qısa və BÖYÜK HƏRF başlıqlarını rədd edir;
   uyğun avtomatik testlər əlavə edilib.
4. **Düymələr** - post sahibi üçün redaktə/silmə düymələri və navbar-da aktiv `+ Yeni post`
   qorunub. CBV `page_title` məlumatı əlavə olunub.
5. **Mesajlar** - `success`, `info`, `warning` və onların CSS rəngləri təsdiqlənib; `info`
   üçün açıq CSS qaydası və testlər əlavə edilib.
6. **Kateqoriya** - mövcud `CategoryForm`, `/category/new/` qorunub; kateqoriyalar
   səhifəsinə yeni kateqoriya linki və test əlavə olunub.
7. **Qadağan olunmuş ad** - Dərs 12-də şərhlərin `name` sahəsi silinərək hesab müəllifi
   (`author`) ilə əvəzləndiyinə görə şərhlərin görünən adı ayrıca, **ixtiyari** sahə kimi
   geri əlavə edilib (`0013_comment_name`). `clean_name()` `admin`, `Admin`, `ADMIN`
   və boşluqlu variantları rədd edir. Boş görünən ad üçün hesabın istifadəçi adı işlənir;
   `author` əlaqəsi və giriş/icazə yoxlamaları olduğu kimi qalır.
8. **Bonus** - `image` sahəsi, `multipart/form-data` və CBV-lərin avtomatik
   `request.FILES` emalı mövcuddur; şəkil yaratma/redaktə testi əlavə olunub.

## Quraşdırma və yoxlama

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata demo_full
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test blog.test_lesson11 blog.tests
python manage.py runserver
```

`loaddata demo_full` yalnız yeni/boş baza üçündür. Əvvəldən dolu bazaya yenidən yükləməyin.
`showmigrations blog` çıxışında `0009`, `0010` və yeni `0013` migration-ları `[X]` olmalıdır.

**Əl ilə yoxlama:** Murad (`murad` / `step12345`) ilə daxil olub `/post/2/`,
`/post/2/edit/`, `/post/2/delete/` ünvanlarına baxın. Əlaqə formunu `/contact/`,
kateqoriya yaratmanı `/category/new/` ünvanında yoxlayın. Post/səhifə identifikatorları
`demo_full` fixture-nə əsaslanır. `/post/new/`-də `SALAM` və `abc` başlıqlarını rədd edin.
Şərh formasında `Admin` adı yoxlanmalıdır. POST uğurlu olanda redirect baş verdiyi üçün
brauzerdə F5 formu təkrar göndərməməlidir.

## Git və təhvil

Göndərilən arxivdə ilkin repo-nun `.git` qovluğu **yoxdur**. `submission/patches/` qovluğunda
ilk göndərilən ZIP-dən başlayan **8 ayrı lokal commit** üçün patch var; bunlar orijinal
GitHub reposuna avtomatik push edilməyib. Repo həmin ilkin arxivlə eynidirsə, patch-ləri
ardıcıllıqla `git apply` edib hər birini ayrıca commit edə bilərsiniz. Əgər repodakı fayllar
fərqlidirsə, hazır həllin dəyişikliklərini öz repoya uyğunlaşdırın.

GitHub-da `blog/migrations/0009_comment_parent.py`, `0010_contactmessage.py` və
`0013_comment_name.py` olmalıdır. `.venv/`, `db.sqlite3`, `media/`, `__pycache__/`
GitHub-da olmamalıdır (`.gitignore` bunları gizlədir). Müəllimə yalnız **mövcud repo linki**
göndərilməlidir.

## Yoxlamaların əhatəsi

Bu mühitdə Django və asılılıqlarını paket serverindən əldə etmək mümkün olmayıb:
**`manage.py test`, `migrate`, `check` burada icra edilməyib.** Python sintaksisi,
URL/form/model/migration şərtləri və patch-lərin quruluşu statik şəkildə yoxlanılıb.
Testləri yuxarıdakı əmrlərlə yerli kompüterdə icra edin.
