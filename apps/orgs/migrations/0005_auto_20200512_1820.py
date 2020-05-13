# Generated by Django 2.2.10 on 2020-05-12 10:20

from django.db import migrations


def migrate_old_organization_members(apps, schema_editor):
    org_model = apps.get_model("orgs", "Organization")
    org_member_model = apps.get_model('orgs', 'OrganizationMembers')
    db_alias = schema_editor.connection.alias
    orgs = org_model.objects.using(db_alias).all()

    ROLE_ADMIN = 'Admin'
    ROLE_USER = 'User'
    ROLE_AUDITOR = 'Auditor'
    roles = [ROLE_USER, ROLE_AUDITOR, ROLE_ADMIN]

    for org in orgs:
        users = org.users.all().only('id')
        auditors = org.auditors.all().only('id')
        admins = org.admins.all().only('id')
        total_members = zip([users, auditors, admins], roles)

        org_members = []
        for members, role in total_members:
            for user in members:
                org_user = org_member_model(user=user, org=org, role=role)
                org_members.append(org_user)
        org_member_model.objects.bulk_create(org_members)


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0004_organizationmembers'),
    ]

    operations = [
        migrations.RunPython(migrate_old_organization_members)
    ]
