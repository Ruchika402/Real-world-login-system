# accounts/signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User

@receiver(user_logged_in)
def send_login_notification(sender, request, user, **kwargs):
    """Send professional login notification email"""
    
    # Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR', 'Unknown')
    
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    
    # Professional HTML email
    subject = f'🔐 New Sign-in to Your Account'
    
    html_message = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Notification</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            
            <!-- Header -->
            <div style="background-color: #4F46E5; padding: 30px 20px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🔐 Security Alert</h1>
            </div>
            
            <!-- Content -->
            <div style="padding: 30px 25px;">
                <h2 style="color: #1f2937; margin-top: 0;">Hello {user.get_full_name() or user.username},</h2>
                
                <p style="color: #4b5563; line-height: 1.6;">We noticed a new sign-in to your account. Here are the details:</p>
                
                <div style="background-color: #f9fafb; padding: 15px; border-radius: 6px; margin: 20px 0;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; color: #6b7280; width: 120px;">📅 Date & Time:</td>
                            <td style="padding: 8px 0; color: #1f2937;">{now().strftime("%B %d, %Y at %I:%M %p")}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #6b7280;">🌐 IP Address:</td>
                            <td style="padding: 8px 0; color: #1f2937;">{ip_address}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #6b7280;">💻 Device:</td>
                            <td style="padding: 8px 0; color: #1f2937;">{user_agent[:100]}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; color: #6b7280;">📍 Location:</td>
                            <td style="padding: 8px 0; color: #1f2937;">Approximate based on IP</td>
                        </tr>
                    </table>
                </div>
                
                <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; color: #92400e; font-size: 14px;">
                        <strong>⚠️ Not you?</strong> If you didn't sign in to your account, please reset your password immediately.
                    </p>
                </div>
                
                <div style="margin-top: 25px;">
                    <a href="#" style="display: inline-block; background-color: #4F46E5; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-right: 10px;">Reset Password</a>
                    <a href="#" style="display: inline-block; color: #4F46E5; text-decoration: none;">Learn More →</a>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                <p style="color: #6b7280; font-size: 12px; margin: 0;">
                    This is an automated security notification from Your App Name.<br>
                    If you have any questions, please contact our support team.
                </p>
                <p style="color: #9ca3af; font-size: 11px; margin-top: 10px;">
                    © 2026 Your App Name. All rights reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    # Plain text version as fallback
    text_message = f"""
Hello {user.get_full_name() or user.username},

We noticed a new sign-in to your account.

Sign-in Details:
--------------
Time: {now().strftime("%B %d, %Y at %I:%M %p")}
IP Address: {ip_address}
Device: {user_agent[:100]}
Location: Approximate based on IP

If this was you, you can safely ignore this email.

If this wasn't you, please reset your password immediately.

Best regards,
Security Team
Your App Name
"""
    
    send_mail(
        subject,
        text_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,  # This sends the HTML version
        fail_silently=False,
    )


@receiver(user_logged_out)
def send_logout_notification(sender, request, user, **kwargs):
    """Send professional logout notification"""
    if user:
        subject = '👋 You Have Been Signed Out'
        
        html_message = f'''
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #10B981; padding: 30px 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0;">👋 Goodbye!</h1>
                </div>
                <div style="padding: 30px;">
                    <h2>Hello {user.get_full_name() or user.username},</h2>
                    <p>You have been successfully signed out of your account.</p>
                    <p style="color: #6b7280;">Sign-out time: {now().strftime("%B %d, %Y at %I:%M %p")}</p>
                    <p>If you didn't sign out, please <a href="#" style="color: #4F46E5;">reset your password</a> immediately.</p>
                </div>
                <div style="background-color: #f9fafb; padding: 20px; text-align: center;">
                    <p style="color: #6b7280; font-size: 12px;">© 2026 Your App Name</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        text_message = f"Hello {user.username},\n\nYou have been signed out at {now().strftime('%B %d, %Y at %I:%M %p')}.\n\nIf this wasn't you, please reset your password."
        
        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message, fail_silently=True)


@receiver(user_login_failed)
def send_failed_login_alert(sender, credentials, request, **kwargs):
    """Send security alert for failed login attempts"""
    username = credentials.get('username', 'Unknown')
    
    # Get IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR', 'Unknown')
    
    try:
        user = User.objects.get(username=username)
        email = user.email
    except User.DoesNotExist:
        email = None
    
    if email:
        subject = '⚠️ Security Alert: Failed Sign-in Attempt'
        
        html_message = f'''
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"></head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #EF4444; padding: 30px 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0;">⚠️ Security Alert</h1>
                </div>
                <div style="padding: 30px;">
                    <h2>Hello {user.get_full_name() or user.username},</h2>
                    <p>We detected a <strong>failed sign-in attempt</strong> to your account.</p>
                    
                    <div style="background-color: #fef2f2; padding: 15px; border-radius: 6px; margin: 20px 0;">
                        <table>
                            <tr><td>📅 Time:</td><td>{now().strftime("%B %d, %Y at %I:%M %p")}</td></tr>
                            <tr><td>🌐 IP Address:</td><td>{ip_address}</td></tr>
                            <tr><td>🔑 Attempted Username:</td><td>{username}</td></tr>
                        </table>
                    </div>
                    
                    <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px;">
                        <strong>🔒 Recommended Actions:</strong>
                        <ul style="margin-top: 10px;">
                            <li>Reset your password to something strong</li>
                            <li>Enable two-factor authentication if available</li>
                            <li>Contact support if you see suspicious activity</li>
                        </ul>
                    </div>
                </div>
                <div style="background-color: #f9fafb; padding: 20px; text-align: center;">
                    <p style="color: #6b7280; font-size: 12px;">© 2026 Your App Name - Security Department</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        text_message = f"Security Alert: Failed sign-in attempt to your account at {now().strftime('%B %d, %Y at %I:%M %p')} from IP {ip_address}."
        
        send_mail(subject, text_message, settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message, fail_silently=True)