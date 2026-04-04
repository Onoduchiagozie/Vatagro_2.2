"""
Migration 0005: safely convert orders_orderproducts.sold_by
from a CharField (storing first_name strings) to a ForeignKey.

Three steps:
  1. Rename old column to sold_by_old so data is preserved
  2. Add new nullable FK column sold_by_new
  3. Data migration: match old string -> user PK, null if no match
  4. Drop old column, rename new column to sold_by
"""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def populate_sold_by_fk(apps, schema_editor):
    OrderProducts = apps.get_model('orders', 'OrderProducts')
    User = apps.get_model('account', 'User')

    for order in OrderProducts.objects.all():
        old_value = order.sold_by_old

        if not old_value or old_value == 'False':
            # 'False' was saved when farmername had no first_name — null it
            order.sold_by_new = None
        else:
            try:
                user = User.objects.get(first_name__iexact=old_value)
                order.sold_by_new = user
            except User.DoesNotExist:
                order.sold_by_new = None
            except User.MultipleObjectsReturned:
                # Two users share the same first name — take the first match
                order.sold_by_new = User.objects.filter(
                    first_name__iexact=old_value).first()

        order.save()


def reverse_populate(apps, schema_editor):
    OrderProducts = apps.get_model('orders', 'OrderProducts')
    for order in OrderProducts.objects.all():
        order.sold_by_old = order.sold_by_new.first_name if order.sold_by_new else ''
        order.save()


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_reviewrating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [

        # Step 1: rename old CharField so we can still read it
        migrations.RenameField(
            model_name='orderproducts',
            old_name='sold_by',
            new_name='sold_by_old',
        ),

        # Step 2: add the new FK column (nullable so existing rows are unblocked)
        migrations.AddField(
            model_name='orderproducts',
            name='sold_by_new',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='sales',
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # Step 3: match old name strings to real user PKs
        migrations.RunPython(populate_sold_by_fk, reverse_populate),

        # Step 4: drop the old string column
        migrations.RemoveField(
            model_name='orderproducts',
            name='sold_by_old',
        ),

        # Step 5: rename new FK column to the final name
        migrations.RenameField(
            model_name='orderproducts',
            old_name='sold_by_new',
            new_name='sold_by',
        ),
    ]