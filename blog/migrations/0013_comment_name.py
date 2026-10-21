from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("blog", "0012_remove_comment_name_comment_author")]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="name",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
    ]
