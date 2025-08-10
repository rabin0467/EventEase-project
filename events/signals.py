from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
from django.core.exceptions import ObjectDoesNotExist

@receiver(m2m_changed, sender=Event.rsvp_participants.through)
def rsvp_activation_mail(sender, instance, action, **kwargs):
    if action:
        rsvp_emails = [user.email for user in instance.rsvp_participants.all()]

        send_mail(
            'RSVP confirmation',
            f"Thank you for joining to {instance.name}",
            "smyrbn.10oct.2001@gmail.com",
            rsvp_emails,
            fail_silently=False
        )