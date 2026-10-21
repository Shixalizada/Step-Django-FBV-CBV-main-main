"""Dərs 11 üçün testlər. İcra: python manage.py test blog.test_lesson11"""
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages
from tempfile import TemporaryDirectory

from .forms import CommentForm, ContactForm, PostForm
from .models import Category, Comment, ContactMessage, Post


class Lesson11HomeworkTests(TestCase):
    fixtures = ["demo_full"]

    def login(self, name="murad"):
        self.assertTrue(self.client.login(username=name, password="step12345"))

    def test_delete_needs_confirmation_and_post(self):
        self.login()
        address = reverse("blog:post_delete", args=[2])
        response = self.client.get(address)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bəli, sil")
        self.assertContains(response, "Xeyr, qayıt")
        self.assertTrue(Post.objects.filter(pk=2).exists())
        response = self.client.post(address, follow=True)
        self.assertRedirects(response, reverse("blog:post_list"))
        self.assertFalse(Post.objects.filter(pk=2).exists())
        self.assertContains(response, "Post silindi")

    def test_contact_validation_saving_and_prg(self):
        url = reverse("blog:contact")
        bad = self.client.post(url, {"name": "Ali", "email": "yanlis", "message": "qısa"})
        self.assertEqual(bad.status_code, 200)
        self.assertTrue(bad.context["form"].errors)
        self.assertEqual(ContactMessage.objects.count(), 0)
        good = self.client.post(url, {"name": "Ali", "email": "ali@example.org", "message": "Bu kifayət qədər uzun mesajdır."})
        self.assertRedirects(good, url)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.client.get(url)  # F5 təkrarlanan POST yaratmır
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.first().email, "ali@example.org")
        User.objects.create_superuser("testadmin", "admin@example.org", "Sifrə-123456")
        self.assertTrue(self.client.login(username="testadmin", password="Sifrə-123456"))
        self.assertEqual(self.client.get(reverse("admin:blog_contactmessage_changelist")).status_code, 200)

    def test_title_validation(self):
        data = {"category": 1, "content": "Kifayət qədər mətn var."}
        for title in ("abc", "SALAM"):
            form = PostForm(data={**data, "title": title})
            self.assertFalse(form.is_valid())
            self.assertIn("title", form.errors)
        self.assertTrue(PostForm(data={**data, "title": "Salam dünya"}).is_valid())

    def test_buttons_navbar_and_form_titles(self):
        self.login()
        response = self.client.get(reverse("blog:post_detail", args=[2]))
        self.assertContains(response, "Redaktə et")
        self.assertContains(response, 'href="/post/2/delete/"')
        new = self.client.get(reverse("blog:post_create"))
        self.assertContains(new, "Yeni post")
        self.assertContains(new, 'class="active">+ Yeni post')
        self.assertContains(self.client.get(reverse("blog:post_edit", args=[2])), "Postu redaktə et")
        self.client.logout()
        self.assertNotContains(self.client.get(reverse("blog:post_detail", args=[2])), "Redaktə et")

    def test_create_edit_delete_message_levels(self):
        self.login()
        payload = {"title": "Yeni mövzu başlığı", "category": 1, "content": "Mətn", "is_published": "on"}
        response = self.client.post(reverse("blog:post_create"), payload, follow=True)
        self.assertIn("Post yaradıldı.", [str(m) for m in response.context["messages"]])
        self.assertIn(messages.SUCCESS, [m.level for m in response.context["messages"]])
        post = Post.objects.get(title=payload["title"])
        payload["title"] = "Dəyişilmiş mövzu başlığı"
        response = self.client.post(reverse("blog:post_edit", args=[post.pk]), payload, follow=True)
        self.assertIn(messages.INFO, [m.level for m in response.context["messages"]])
        response = self.client.post(reverse("blog:post_delete", args=[post.pk]), follow=True)
        self.assertIn(messages.WARNING, [m.level for m in response.context["messages"]])

    def test_category_form_and_url_order(self):
        address = reverse("blog:category_create")
        self.assertEqual(address, "/category/new/")
        self.assertEqual(self.client.get(address).status_code, 200)
        response = self.client.post(address, {"name": "Elm", "slug": "elm", "description": "Elmi xəbərlər"})
        self.assertRedirects(response, reverse("blog:category_list"))
        self.assertTrue(Category.objects.filter(slug="elm").exists())
        self.assertContains(self.client.get(reverse("blog:category_list")), "Elm")

    def test_forbidden_comment_name_case_insensitive(self):
        self.login("aysel")
        url = reverse("blog:post_detail", args=[3])
        count = Comment.objects.count()
        for name in ("admin", "Admin", "ADMIN", "  aDmIn  "):
            response = self.client.post(url, {"name": name, "text": "Maraqlı mövzudur"})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "admin adı ilə şərh yazmaq olmaz")
            self.assertEqual(Comment.objects.count(), count)
        response = self.client.post(url, {"name": "Aysu", "text": "Maraqlı mövzudur"})
        self.assertRedirects(response, url)
        comment = Comment.objects.get(name="Aysu")
        self.assertEqual(comment.author.username, "aysel")
        self.assertContains(self.client.get(url), "Aysu")

    def test_reply_form_rejects_admin_name(self):
        self.login("aysel")
        url = reverse("blog:comment_reply", args=[1])
        response = self.client.post(url, {"name": "ADMIN", "text": "Cavab mətni"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin adı ilə şərh yazmaq olmaz")

    def test_image_upload_create_and_edit(self):
        # CBV CreateView / UpdateView request.FILES-i avtomatik formaya ötürür.
        self.login()
        gif = (b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00"
               b"!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            create_data = {"title": "Şəkilli yeni mövzu", "category": 1, "content": "Mətn",
                           "image": SimpleUploadedFile("ilk.gif", gif, content_type="image/gif")}
            self.assertRedirects(self.client.post(reverse("blog:post_create"), create_data),
                                 reverse("blog:post_detail", args=[Post.objects.latest("id").id]))
            post = Post.objects.get(title="Şəkilli yeni mövzu")
            self.assertTrue(post.image.name.startswith("posts/"))
            update_data = {"title": "Şəkilli yenilənmiş mövzu", "category": 1, "content": "Mətn",
                           "image": SimpleUploadedFile("ikinci.gif", gif, content_type="image/gif")}
            self.assertRedirects(self.client.post(reverse("blog:post_edit", args=[post.pk]), update_data),
                                 reverse("blog:post_detail", args=[post.pk]))
            post.refresh_from_db()
            self.assertIn("ikinci", post.image.name)

