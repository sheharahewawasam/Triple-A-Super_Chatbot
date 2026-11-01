"""
Give every existing advisor a sign-in account.

The advisors predate authentication, so they exist as bare names with no way to
log in. This creates one auth User per Advisor and links them.

New accounts have unusable passwords until an administrator provisions a unique
password with python manage.py changepassword <username>. Existing databases
where this migration already ran are unchanged: rotate any shared placeholder
password separately on every deployment. Never put replacement passwords in git.

New advisors added later get an account the same way - through the admin - not
through this migration.
"""
from django.contrib.auth.hashers import make_password
from django.db import migrations

def create_users(apps, schema_editor):
    Advisor = apps.get_model("rag_api", "Advisor")
    User = apps.get_model("auth", "User")

    # New installations must explicitly provision a unique password per adviser.
    # This does not rotate passwords on databases where this migration already ran.
    hashed = make_password(None)

    for advisor in Advisor.objects.filter(user__isnull=True):
        # Usernames are lowercased so signing in is not case-sensitive, while
        # Advisor.name stays as it is - it is what Pinecone's owner field and
        # the audit logs are keyed on.
        username = advisor.name.lower()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"password": hashed, "is_active": True},
        )
        if not created and not user.password:
            user.password = hashed
            user.save(update_fields=["password"])
        advisor.user = user
        advisor.save(update_fields=["user"])


def unlink_users(apps, schema_editor):
    Advisor = apps.get_model("rag_api", "Advisor")
    User = apps.get_model("auth", "User")

    names = list(Advisor.objects.exclude(user__isnull=True)
                 .values_list("user__username", flat=True))
    Advisor.objects.update(user=None)
    # Leave superusers alone; they were not created here.
    User.objects.filter(username__in=names, is_superuser=False).delete()


class Migration(migrations.Migration):
    dependencies = [("rag_api", "0005_add_user_to_advisor")]
    operations = [migrations.RunPython(create_users, unlink_users)]
