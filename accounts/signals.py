from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now


@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    """Send email when user logs in successfully"""
    
    # Get client IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    # Get user agent (browser info)

    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    
    subject = f'🔐 New Login to Your Account - {now().strftime("%Y-%m-%d %H:%M")}'
    message = f"""
    Hello {user.get_full_name() or user.username},
    
    We detected a new login to your account.
    📅 Time: {now().strftime("%Y-%m-%d %H:%M:%S")}
    🌐 IP Address: {ip_address}
    💻 Browser: {user_agent[:200]}
    
    If this was you, you can safely ignore this email.
    
    If this wasn't you, please:
    1. Change your password immediately
    2. Contact our support team
    
    Stay safe,
    Your App Team
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

@receiver(user_logged_out)
def send_logout_notification(sender, request, user, **kwargs):
    """Send email when user logs out (optional but nice)"""
    if user:  # user might be None in some cases
        subject = '👋 You Have Been Logged Out'
        message = f"""
        Hello {user.get_full_name() or user.username},
        
        You were logged out of your account at {now().strftime("%Y-%m-%d %H:%M:%S")}.
        
        If this wasn't you, please reset your password immediately.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,  # Don't crash if email fails
        )

@receiver(user_login_failed)
def send_failed_login_alert(sender, credentials, request, **kwargs):
    """Alert about failed login attempts (security feature)"""
    username = credentials.get('username', 'Unknown')
    
    # Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Try to find user by username to get their email
    try:
        from django.contrib.auth.models import User
        user = User.objects.get(username=username)
        email = user.email
    except User.DoesNotExist:
        email = None
    
    if email:
        subject = '⚠️ Failed Login Attempt on Your Account'
        message = f"""
        Hello,
        
        Someone tried to log into your account ({username}) but failed.
        
        📅 Time: {now().strftime("%Y-%m-%d %H:%M:%S")}
        🌐 IP Address: {ip_address}
        
        If this was you trying to log in, you can ignore this message.
        
        If this wasn't you, please:
        1. Check your password strength
        2. Enable two-factor authentication
        3. Contact support immediately
        
        Best regards,
        Security Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True,
        )