from cProfile import label
from os import name
import re
from django.shortcuts import render,redirect

from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count

def home(request):
    total_users = User.objects.filter(is_staff=False).count()
    total_predictions = Prediction.objects.count()
    return render(request,"home.html",locals())

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if not name or not email or not phone or not password:
            messages.error(request,"All fields are required")
            return redirect("signup")
        if len(password) < 6:
            messages.error(request,"Password must be at least 6 characters long")
            return redirect("signup")
        if User.objects.filter(username=email).first():
            messages.error(request,"Email already registered")
            return redirect("signup")
        user = User.objects.create_user(username=email,password=password,first_name=name)
        user.save()
        user_profile = UserProfile.objects.create(user=user,phone=phone)
        login(request,user)
        messages.success(request,"Account created Successfully. Welcome!")
        return redirect("predict")
    return render(request,"signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if not user:
            messages.error(request,"Invalid Login Credentials")
            return redirect("login")
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("predict")
    return render(request,"login.html")

def logout_view(request):
    logout(request)
    messages.success(request,"Logged out successfully") 
    return redirect("login")

from .ml.loader import predict_crop,load_bundle 
from django.contrib.auth.decorators import login_required,user_passes_test

@login_required(login_url='login')
def predict_view(request):
    feature_order = load_bundle()["feature_cols"]
    result = None
    last_data = None

    if request.method == "POST":
        data = {}
        try:
            for feature in feature_order:
                value = float(request.POST.get(feature))
                data[feature] = value
            
        except Exception as e:
            messages.error(request,"Invalid Input Data. Please enter valid values.")
            return redirect("predict")
        label = predict_crop(data)

        Prediction.objects.create(user=request.user, **data, predicted_label=label)
        result = label
        last_data = data
        messages.success(request,f"Recommended Crop: {label}")


    return render(request,"predict.html",locals())
@login_required(login_url='login')
def history_view(request):
    prediction = Prediction.objects.filter(user=request.user).order_by('-created_at')
    return render(request,"history.html",locals())

from django.shortcuts import get_object_or_404
@login_required(login_url='login')
def user_delete_prediction_view(request, id):
    pred = get_object_or_404(Prediction, id=id, user=request.user)
    if request.method == "POST":
        pred.delete()
        messages.success(request, "Prediction deleted successfully.")
        return redirect("history")
    # if not POST, redirect back (prevents accidental deletes via GET)
    return redirect("history")
   
from django.db.models import Count
from datetime import datetime

@login_required(login_url='login')
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "update_profile":
            name = request.POST.get("name")
            phone = request.POST.get("phone")

            if not name or not phone:
                messages.error(request, "All fields are required")
                return redirect("profile")
            
            request.user.first_name = name
            request.user.save()
            profile.phone = phone
            profile.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
        
        elif action == "change_password":
            current_pwd = request.POST.get("current_password")
            new_pwd = request.POST.get("new_password")
            confirm_pwd = request.POST.get("confirm_password")
            
            if not request.user.check_password(current_pwd):
                messages.error(request, "Current password is incorrect.")
            elif new_pwd != confirm_pwd:
                messages.error(request, "New passwords do not match.")
            elif len(new_pwd) < 6:
                messages.error(request, "Password must be at least 6 characters.")
            else:
                request.user.set_password(new_pwd)
                request.user.save()
                messages.success(request, "Password changed successfully! Please login again.")
                return redirect("login")

    # Fetch stats
    all_predictions = Prediction.objects.filter(user=request.user)
    predictions_count = all_predictions.count()
    
    this_month = datetime.now().replace(day=1)
    predictions_this_month = all_predictions.filter(created_at__gte=this_month).count()
    
    top_crop_obj = all_predictions.values('predicted_label').annotate(count=Count('predicted_label')).order_by('-count').first()
    top_crop = top_crop_obj['predicted_label'] if top_crop_obj else None

    context = {
        "profile": profile,
        "predictions_count": predictions_count,
        "predictions_this_month": predictions_this_month,
        "top_crop": top_crop,
    }
    return render(request, "profile.html", context)


def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if not user:
            messages.error(request,"Invalid Login Credentials")
            return redirect("admin_login")
        if not user.is_staff:
            messages.error(request,"You are not authorized to access admin panel")
            return redirect("admin_login")
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("admin_dashboard")
    return render(request, "admin_login.html")



from django.utils import timezone
import json
from datetime import timedelta
@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_dashboard_view(request):
    total_users = User.objects.filter(is_staff=False).count()
    total_predictions = Prediction.objects.count()

    crop_qs = (Prediction.objects.values('predicted_label')
                .annotate(c=Count('id'))
                .order_by('-c')[:10]
               )
    crop_labels = [i['predicted_label'].title() for i in crop_qs]
    crop_counts = [r['c'] for r in crop_qs]

    today = timezone.localdate()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    day_labels = [d.strftime("%d %b") for d in days]
    day_counts = [Prediction.objects.filter(created_at__date=d).count() for d in days]

    context = {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "crop_labels_json": json.dumps(crop_labels),
        "crop_counts_json": json.dumps(crop_counts),
        "day_labels_json": json.dumps(day_labels),
        "day_counts_json": json.dumps(day_counts),
    }

    return render(request, "admin_dashboard.html",context=context)

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_users_view(request):
    users = User.objects.filter(is_staff=False)
    return render(request, "admin_view_users.html",{"users": users})

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_user_delete_view(request, id):
    user = get_object_or_404(User, id=id, is_staff=False)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("admin_users_view")
    return redirect("admin_users_view")



@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_logout_view(request):
    logout(request)
    messages.success(request,"Logged out successfully") 
    return redirect("admin_login")

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def admin_view_prediction(request):
    # use GET so filtering is bookmarkable and avoids CSRF for filter form
    crops = Prediction.objects.values_list('predicted_label', flat=True).distinct().order_by('predicted_label')
    selected_crop = request.GET.get("crop", "")
    start_date = request.GET.get("start", "")
    end_date = request.GET.get("end", "")

    qs = Prediction.objects.select_related('user').all()

    if selected_crop:
        qs = qs.filter(predicted_label=selected_crop)
    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__date__lte=end_date)

    qs = qs.order_by('-created_at')

    context = {
        "qs": qs,
        "crops": crops,
        "selected_crop": selected_crop,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, "admin_view_prediction.html", context)