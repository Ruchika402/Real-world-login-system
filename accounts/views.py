from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm

def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            from django.core.mail import send_mail
            from django.conf import settings
            
            # Professional HTML Welcome Email
            subject = '🎉 Welcome to TaskMaster!'  # ← CHANGE "TaskMaster" to your app name
            
            # Plain text version (for email clients that don't support HTML)
            text_message = f"""
Hello {user.first_name}!,

Welcome to TaskMaster! Thank you for creating an account with us.

Your account has been successfully created. You can now:
• Log in to your dashboard
• Update your profile
• Start using our services

If you have any questions, feel free to contact our support team.

Best regards,
The TaskMaster Team
"""
            
            # HTML version (beautiful, professional email)
            html_message = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to TaskMaster</title>
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f4f7; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        
        <!-- Header with your brand color -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 28px;">🎉 Welcome to TaskMaster!</h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0;">Your journey starts here</p>
        </div>
        
        <!-- Main Content -->
        <div style="padding: 40px 30px;">
            <h2 style="color: #333333; margin-top: 0;">Hello {user.first_name} {user.last_name}!</h2>
            
            <p style="color: #555555; line-height: 1.6; font-size: 16px;">
                Thank you for creating an account with <strong>TaskMaster</strong>. We're thrilled to have you on board!
            </p>
            
            <div style="background-color: #f0fdf4; border-left: 4px solid #10b981; padding: 20px; margin: 25px 0; border-radius: 8px;">
                <p style="margin: 0 0 10px; font-weight: bold; color: #065f46;">✅ Your account is now ready!</p>
                <p style="margin: 0; color: #065f46;">Here's what you can do next:</p>
                <ul style="margin: 10px 0 0; color: #065f46;">
                    <li>Complete your profile</li>
                    <li>Explore your dashboard</li>
                    <li>Connect with other users</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://127.0.0.1:8000/accounts/dashboard/" 
                   style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; text-decoration: none; padding: 12px 30px; border-radius: 25px; 
                          font-weight: bold;">
                    Go to Dashboard →
                </a>
            </div>
            
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
            
            <p style="color: #6b7280; font-size: 14px; line-height: 1.5;">
                Need help? Contact our support team at 
                <a href="mailto:support@taskmaster.com" style="color: #667eea;">support@taskmaster.com</a>
            </p>
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f9fafb; padding: 25px; text-align: center; border-top: 1px solid #e5e7eb;">
            <p style="color: #9ca3af; font-size: 12px; margin: 0;">
                © 2026 TaskMaster. All rights reserved.<br>
                You received this email because you created an account with TaskMaster.
            </p>
        </div>
    </div>
</body>
</html>
'''
            
            # Send the email with both plain text and HTML versions
            send_mail(
                subject,
                text_message,  # Plain text fallback
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,  # Beautiful HTML version
                fail_silently=False,  # Set to True for production
            )
            
            messages.success(request, 'Registration successful! Welcome aboard!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})
            
        
def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    """User dashboard (protected view)"""
    return render(request, 'accounts/dashboard.html', {
        'user': request.user,
    })

def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')