from django import forms

from .models import Post, Comment, Category

# Form üç iş görür: 1) HTML input-ları çəkir  2) gələn məlumatı yoxlayır  3) (ModelForm) bazaya yazır.
# Nişanlar:  [DƏRS 12] müəllim yazır · [PRAKTİKA 12] tələbə yazır · [EV 12] ev tapşırığı


# [DƏRS 11] ModelForm — sahələri Comment modelindən özü götürür
class CommentForm(forms.ModelForm):
    # Dərs 12-dəki real hesab qalır; istəyə görə görünən ad ayrıca göstərilir.
    name = forms.CharField(max_length=50, required=False, label="Görünən ad (istəyə görə)")

    class Meta:
        model = Comment
        fields = ["name", "text"]
        labels = {"text": "Şərhin"}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name and self.user is not None and self.user.is_authenticated:
            name = self.user.username
        if name.lower() == "admin":
            raise forms.ValidationError("admin adı ilə şərh yazmaq olmaz.")
        return name

    # [DƏRS 11] öz yoxlama qaydamız: clean_<sahə adı>. Django bunu is_valid() zamanı özü çağırır
    def clean_text(self):
        text = self.cleaned_data["text"]                          # bu sahənin təmizlənmiş dəyəri
        if len(text) < 5:
            raise forms.ValidationError("Şərh ən azı 5 simvol olmalıdır.")
        return text                                               # HƏMİŞƏ dəyəri qaytar


# [DƏRS 11] post yaratmaq və redaktə etmək üçün — eyni form hər ikisinə yarayır
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # [DƏRS 12] "author" formdan ÇIXARILDI — müəllifi istifadəçi seçmir, view request.user yazır
        # [EV 12] tapşırıq 6 — is_published: qaralama kimi saxlamaq üçün
        fields = ["title", "category", "tags", "content", "image", "is_published"]
        labels = {
            "title": "Başlıq",
            "category": "Kateqoriya",
            "tags": "Teqlər",
            "content": "Mətn",
            "image": "Şəkil",
            "is_published": "Dərc olunsun",
        }

    # [EV 11] tapşırıq 3
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise forms.ValidationError("Başlıq ən azı 5 simvol olmalıdır.")
        if title.isupper():
            raise forms.ValidationError("Başlığı tam böyük hərflə yazma.")
        return title


# [EV 11] tapşırıq 6 — PostForm-un əkizi
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description"]


# [EV 11] tapşırıq 2 — adi Form: modelə bağlı deyil, sahələri özümüz yazırıq
class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label="Adın")
    email = forms.EmailField(label="Email")                       # email formatını özü yoxlayır
    message = forms.CharField(widget=forms.Textarea, label="Mesaj")

    def clean_message(self):
        message = self.cleaned_data["message"]
        if len(message) < 10:
            raise forms.ValidationError("Mesaj ən azı 10 simvol olmalıdır.")
        return message
