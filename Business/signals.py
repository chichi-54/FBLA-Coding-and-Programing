from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Business, Notification, Review
from Users.models import Profile
from django.contrib.auth.models import User

@receiver(post_save, sender=Business)
def notify_business_created(sender, instance, created, **kwargs):
    if created:
        admins = Profile.objects.filter(is_admin=True)

        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                message=f"New business '{instance.name}' was created",
                notification_type="business_created"
            )

    
@receiver(post_save, sender=Business)
def notify_business_deleted(sender, instance, **kwargs):
    admins = Profile.objects.filter(is_admin=True)

    for admin in admins:
        Notification.objects.create(
            recipient=admin.user.profile,
            message=f"Business '{instance.name}' was deleted",
            notification_type="business_deleted"
        )

@receiver(post_save, sender=Review)
def notify_review_added(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.business.owner.user.profile,
            message=f"New review on '{instance.business.name}'",
            notification_type="review_added"
        )


@receiver(post_save, sender=Business)
def notify_business_approved(sender, instance, **kwargs):
    if instance.approval_state == "Approved":
        Notification.objects.get_or_create(
            recipient=instance.owner.user.profile,
            notification_type="business_approved",
            defaults={
                "message": f"Your business '{instance.name}' has been approved"
            }
        )


@receiver(post_save, sender=Business)
def notify_business_declined(sender, instance, **kwargs):
    if instance.approval_state == "Declined":
        Notification.objects.get_or_create(
            recipient=instance.owner.user.profile,
            notification_type="business_declined",
            defaults={
                "message": f"Your business '{instance.name}' has been declined"
            }
        )
