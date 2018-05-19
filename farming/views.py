# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .forms import FarmerForm, ScheduleForm, FarmForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from models import FarmerDetail, FarmDetail, ScheduleDetail
from django.http.response import HttpResponse
from datetime import date
from datetime import timedelta
import logging
from django.conf import settings
logger = logging.getLogger(__name__)

def index(request):
    logger.info("Home page accessed.")
    return render(request, "home.html")

@csrf_exempt
def createFarmerDetail(request):
    try:
        if request.method == "GET":
            logger.info("Farmer Creation Page")
            form = FarmerForm()
            return render(request, "createfarmer.html",{"form":form}) 
        elif request.method == "POST":
            form = FarmerForm()
            request_form = FarmerForm(request.POST)
            logger.info("Farmer Creation Request {}".format(request_form.cleaned_data))
            if request_form.is_valid():
                request_form.save()
                messages.success(request, "Inserted Successfully")
                return redirect("/createfarmer", {"message":"Created successfully", "form": form})
            else:
                messages.error(request, "Error, Enter valid details.")
                return redirect("/createfarmer", {"message":"Creation failed", "form": form})
        else:
            messages.error(request, "Only GET and POST method allowed.")
            return render(request,"createfarmer.html", {"form": form})
    except Exception as e:
        logger.error("Farmer Creation Failed due to {}".format(e))
        return render(request,"createfarmer.html", {"form": form})

@csrf_exempt
def createFarm(request):
    form = FarmForm()
    try:
        if request.method == "POST":
            request_form = FarmForm(request.POST)
            logger.info("Farmer Creation Request {}".format(request_form.cleaned_data))
            if request_form.is_valid():
                request_form.save()
                messages.success(request, "Inserted Successfully")
                return redirect("/createfarm", {"message":"Created successfully", "form": form})
            else:
                messages.error(request, "Error, Enter valid details.")
                return redirect("/createfarm", {"message":"Creation failed", "form": form})
        elif request.method == "GET":
            return render(request,"createfarm.html", {"form": form})
        else:
            messages.error(request, "Only GET and POST method allowed.")
            return render(request,"createfarm.html", {"form": form})
    except Exception as e:
        logger.error("Farm Creation Failed due to {}".format(e))
        return render(request,"createfarm.html", {"form": form})

@csrf_exempt
def createSchedule(request):
    form = ScheduleForm()
    try:
        if request.method == "GET":
            return render(request,"createschedule.html", {"form": form})
        elif request.method == "POST":
            request_form = ScheduleForm(request.POST)
            logger.info("Schedule Creation Request {}".format(request_form.cleaned_data))
            if request_form.is_valid():
                request_form.save()
                messages.success(request, "Inserted Successfully")
            else:
                messages.error(request, "Error, Enter valid details.")
            return render(request,"createschedule.html", {"form": form})
        else:
            messages.error(request, "Only GET and POST method allowed.")
            return render(request,"createschedule.html", {"form": form})
    except Exception as e:
        logger.error("Schedule Creation Failed due to {}".format(e))
        return render(request,"createschedule.html", {"form": form})

def listAllFarmer(request):
    try:
        if request.method == "GET":
            farmers = []
            farmer_details = FarmerDetail.objects.values()
            farm_detail = FarmDetail.objects.values()
            f = {i["id"]:i for i in farmer_details}
            for i in farm_detail:
                i["farmer_name"] = f[i["farmer_id"]]["name"]
                i["farmer_phone"] = f[i["farmer_id"]]["phone"]
                i["farmer_language"] = f[i["farmer_id"]]["language"]
                farmers.append(i) 
            return render(request, "listallfarmers.html", {"farmer": farmers})
        else:
            return render(request, "listallfarmers.html")
    except Exception as e:
        logger.error("Error in list farmers {}".format(e))
        messages.error(request, "Error, Not able to fetch data")
        return render(request, "listallfarmers.html")

def listAllFarm(request):
    try:
        if request.method == "GET":
            farm_detail = FarmDetail.objects.all()
            return render(request, "listallfarms.html", {"farm":farm_detail})
        else:
            return render(request, "listallfarms.html")
    except Exception as e:
        logger.error("Error in list farms {}".format(e))
        messages.error(request, "Error, Not able to fetch data.")
        return render(request, "listallfarms.html")
    
def allDue(request):
    try:
        if request.method == "GET":
            schedule_detail = ScheduleDetail.objects.all()
            today_due_data = []
            tomorrow_due_data = []
            tod_date = date.today()
            tom_date = tod_date+timedelta(days=1)
            for i in schedule_detail:
                sow_date =  i.sowingdate
                days_after_sowing = i.days
                schedule_date = sow_date + timedelta(days=days_after_sowing)
                if schedule_date == tod_date:
                    today_due_data.append(i)
                elif schedule_date == tom_date:
                    tomorrow_due_data.append(i)
            return render(request, "alldue.html", {"todaydue":today_due_data, "tomorrowdue": tomorrow_due_data})
        else:
            return render(request, "alldue.html")
    except Exception as e:
        logger.error("Error in list due schedule {}".format(e))
        messages.error(request, "Error, Not able to fetch data.")
        return render(request, "alldue.html")