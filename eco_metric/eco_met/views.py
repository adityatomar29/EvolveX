from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CarbonFootprint, MLModelRun
# from .forms import MLPipelineForm
from django.http import JsonResponse
from django.db.models import Avg, Sum
from django.utils import timezone
from datetime import timedelta
# from codecarbon import EmissionsTracker
import random, time
import json
from django.views.decorators.csrf import csrf_exempt
from .utils.recommendation_engine import generate_recommendations
from .utils.ml_recommendation_engine import generate_ml_recommendations



# Create your views here.
def index(request):
    return render(request, 'landing2.html')

def auth(request):
    """
    Handles both login and signup from a single template (login.html)
    """
    if request.method == 'POST':
        action = request.POST.get('action')  # identifies which button was clicked

        username = request.POST.get('username')
        password = request.POST.get('password')

        # ---------- SIGNUP ----------
        if action == 'signup':
            email = request.POST.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another.")
                return redirect('auth')

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('auth')

        # ---------- LOGIN ----------
        elif action == 'login':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                if not User.objects.filter(username=username).exists():
                    messages.error(request, "User not registered. Please sign up first.")
                else:
                    messages.error(request, "Invalid credentials. Try again.")
                return redirect('auth')

    return render(request, 'login.html')


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('')


def carbon_calculator(request):
    total = None
    recommendations = []
    reduction = 0

    if request.method == 'POST':
        data = request.POST

        def get_val(name):
            try:
                return float(data.get(name, 0))
            except ValueError:
                return 0

        car_distance = get_val('car_distance')
        flight_hours = get_val('flight_hours')
        public_trips = get_val('public_trips')
        electricity = get_val('electricity')
        gas = get_val('gas')
        meat_meals = get_val('meat_meals')
        local_food = get_val('local_food')
        waste_kg = get_val('waste_kg')
        recycling = get_val('recycling')
        water_liters = get_val('water_liters')
        showers = get_val('showers')
        online_orders = get_val('online_orders')
        clothing = get_val('clothing')

        car_emission = car_distance * 0.2
        flight_emission = flight_hours * 90
        public_emission = public_trips * 1.5
        energy_emission = electricity * 0.5 + gas * 2.3
        food_emission = meat_meals * 7 - local_food * 0.05
        waste_emission = waste_kg * 1.2 - recycling * 0.1
        water_emission = water_liters * 0.002 + showers * 0.5
        shopping_emission = online_orders * 4 + clothing * 5

        total = round(sum([
            car_emission, flight_emission, public_emission,
            energy_emission, food_emission, waste_emission,
            water_emission, shopping_emission
        ]), 2)

        CarbonFootprint.objects.create(
            car_distance=car_distance,
            flight_hours=flight_hours,
            public_trips=public_trips,
            electricity=electricity,
            gas=gas,
            meat_meals=meat_meals,
            local_food=local_food,
            waste_kg=waste_kg,
            recycling=recycling,
            water_liters=water_liters,
            showers=showers,
            online_orders=online_orders,
            clothing=clothing,
            total_footprint=total
        )

        user_data = {
            "car_distance": car_distance,
            "flight_hours": flight_hours,
            "electricity": electricity,
            "gas": gas,
            "meat_meals": meat_meals,
            "waste_kg": waste_kg,
            "recycling": recycling,
            "water_liters": water_liters,
            "online_orders": online_orders,
            "clothing": clothing
        }

        recommendations, reduction = generate_recommendations(user_data)

        eco_score = int(total/100) + 40
        # eco_score = max(0, 100 - int(total))

        transport = car_emission + public_emission + flight_emission
        energy = energy_emission
        food = food_emission
        other = waste_emission + water_emission + shopping_emission

        return render(request,"results.html",{
        "total_footprint": total,
        "eco_score": eco_score,
        "recommendations": recommendations,
        "reduction": reduction,
        "transport": round(transport,2),
        "energy": round(energy,2),
        "food": round(food,2),
        "other": round(other,2)
        })

    return render(request, 'calculate.html')

    # return render(request, 'calculate.html', {'total_footprint': total})



def carbon_dashboard(request):
    return render(request, 'dashboard.html')

def carbon_data_api(request):
    """API endpoint for live dashboard data"""
    data = CarbonFootprint.get_dashboard_data()
    return JsonResponse(data)


def ml_tracker_view(request):
    return render(request, "MLCalculator.html")

@csrf_exempt
def add_ml_model(request):
    if request.method == "POST":

        data = request.POST

        model = MLModelRun.objects.create(
            model_name=data.get("model_name"),
            training_time=float(data.get("training_time")),
            hardware=data.get("hardware"),
            energy_consumed=float(data.get("energy"))
        )

        user_data = {
            "model_name": model.model_name,
            "training_time": model.training_time,
            "hardware": model.hardware,
            "energy": model.energy_consumed,
        }

        recommendations, reduction = generate_ml_recommendations(user_data)

        eco_score = max(0, 100 - int(model.emission))

        return render(request, "ml_results.html", {
            "total_emission": model.emission,
            "eco_score": eco_score,
            "reduction": reduction,
            "recommendations": recommendations,
            "model_name": model.model_name,
            "hardware": model.hardware,
            "training_time": model.training_time,
            "energy": model.energy_consumed,
        })

    return render(request, "MLCalculator.html")  # fallback