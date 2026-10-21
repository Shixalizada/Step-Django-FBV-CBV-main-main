# Ayrı lokal commitlər

Patch-lər bu ZIP-in ilkin variantından hazırlanıb. `.git` qovluğu daxil edilməyib:
GitHub-dakı mövcud repoya avtomatik push olunmayıb.

| # | Commit mesajı | Məqsəd |
|---|---|---|
| 1 | `post silmə` | CBV `post_id` düzəlişi, təsdiq/silmə testi |
| 2 | `ContactForm` | Mesajın yoxlanması, bazada saxlanma, F5/admin testi |
| 3 | `başlıq yoxlaması` | Qısa/BÖYÜK HƏRF başlıq testləri |
| 4 | `düymələr və aktiv link` | Form başlıqları və düymə/navbar testi |
| 5 | `üç rəngdə mesaj` | Açıq `info` CSS və üç səviyyə testi |
| 6 | `kateqoriya formu` | Yeni kateqoriya keçidi və test |
| 7 | `qadağan olunmuş ad və migration` | `clean_name`, görünən ad və 0013 migration |
| 8 | `şəkil yükləmə bonusu və testlər` | Şəkilli yaratma/redaktə testi |

Orijinal layihədə ilk 6 tapşırığın əsas funksiyalarının çoxu artıq var idi;
patch-lər tələb olunan çatışmazlıqları və testləri əhatə edir.
