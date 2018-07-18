from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect

#------------------------------------------------------------------------------
# Codes start here ... Chia Tham
from django.utils.crypto import get_random_string
from django.contrib import messages
from .models import *

import datetime
import time
import random
import bcrypt

def blank(request):
    print ("*"*20+" blank "+"*"*20)
    return render(request, "campus3/blank.html")

def index(request):
    print ("*"*20+" index "+"*"*20)
    ### Get User Types
    c01=userType.objects.using('campus3').all()
    ### Check if userTYpe is empty, then insert staff & student as values
    if len(c01) == 0:
        c02=userType(nameType="Staff")
        c02.save(using="campus3")
        c03=userType(nameType="Student")
        c03.save(using="campus3")
    ### Get User Types
    c04=userType.objects.using('campus3').all()
    ### Get College Email
    c05=Person.objects.using('campus3').all()
    ### Context Info
    context = {
        "allUserType" : c04,
        "allEmail" : c05,
    }
    return render(request, "campus3/index.html", context)

### Registration logic
def regUser(request):
    print ("*"*20+" regUser "+"*"*20)
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.person_validator(request.POST)
        ### Check User Type
        if request.POST.get("inputUserType") == "0":
            errors["9error010"] = "Unable to register where user group is empty. Try again!"
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/campus3")
        ### Check Validation Errors
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/campus3")
        else:
            ### Check Email Duplication
            c11=Person.objects.using('campus3').filter(personEmail=request.POST.get("inputPersonEmail"))
            if len(c11) > 0:
                errors["9error012"] = "Unable to register with this person email address. Try again!"
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect("/campus3")
            ### Generate College Email 
            temp_l = request.POST.get("inputLastName")
            temp_f = request.POST.get("inputFirstName")
            temp_cnt = 0
            while True:
                temp_cnt+=1
                ### Campus ID
                temp_n = str(random.randint(10,99))
                temp_email = temp_f[0].lower() + temp_l.lower() + temp_n + "@college.edu"
                # print temp_email
                ### Try To Generate Campus ID For X Times
                if temp_cnt > 10:
                    errors["9error013"] = "Unable to register with this person. ERROR 1."
                    for tag, error in errors.iteritems():
                        messages.error(request, error, extra_tags=tag)
                    return redirect("/campus3")
                    break
                ### Try to find if email exist
                c12=Person.objects.using('campus3').filter(collegeEmail=temp_email)
                if len(c12) == 0:
                    break
            ### End While Loop
            ### Generate Campus ID
            temp_year = str(datetime.date.today().year)
            temp_cnt = 0
            while True:
                temp_cnt+=1
                ### College Email Address
                temp_n = str(random.randint(1000,9999))
                temp_id = "#" + temp_year + temp_n
                # print (temp_id)
                ### Try To Generate College Email Address For X Times
                if temp_cnt > 10:
                    errors["9error014"] = "Unable to register with this person. ERROR 2"
                    for tag, error in errors.iteritems():
                        messages.error(request, error, extra_tags=tag)
                    return redirect("/campus3")
                    break
                ### Check If The Random College Email Address Found In DB
                c13=Person.objects.using('campus3').filter(campusID=temp_email)
                if len(c13) == 0:
                    break
            ### End While Loop
            ### Bcrypt Password
            hashPassword = bcrypt.hashpw(request.POST.get("inputPassword1").encode(), bcrypt.gensalt())
            ### Insert Person Into DB
            Person.objects.using('campus3').create(
                campusID=temp_id, 
                lastName=request.POST.get("inputLastName"),
                firstName=request.POST.get("inputFirstName"),
                dateBirth=request.POST.get("inputDateBirth"),
                address=request.POST.get("inputAddress"),
                phone=request.POST.get("inputPhone"),
                extNum=request.POST.get("inputExtNum"),
                personEmail=request.POST.get("inputPersonEmail"), 
                collegeEmail=temp_email,
                # password=request.POST.get("inputPassword1"),
                password=hashPassword,
            )
            ### Get the Record
            c14=Person.objects.using('campus3').get(collegeEmail=temp_email)
            c15=userType.objects.using('campus3').get(id=request.POST.get("inputUserType"))
            ### Insert UserGroup Into DB
            userGroup.objects.using('campus3').create(person_ID=c14,userType_ID=c15)
            ### Insert Building Into DB
            Building.objects.using('campus3').create(
                ID_building=c14,
                buildingName=request.POST.get("inputBuilding"), 
                officeRoom=request.POST.get("inputOffice"), 
            )
            ### Create a Session 
            request.session["key"]  = str(time.time()) + "-" + str(random.randint(1,99999))
            request.session["id"]  = c14.id
            request.session["adminRight"] = c14.adminRight
            ### Generate a New Message for New User
            errors["9error015"] = "Your new campus ID is "+temp_id+", and your new college email address is "+temp_email+". Please use your college email address for sign in. Thank you."
            ### Prepare Message For New User
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/campus3/dashboard/"+str(c14.id))
    return redirect("/campus3")

### Login Logic
def login(request):
    print ("*"*20+" login "+"*"*20)
    ### Get Input 
    temp_e = request.POST.get("inputCollegeEmail")
    temp_p = request.POST.get("inputPassword")
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/campus3")
        else:
            ### Check If College Email Exist
            c21 = Person.objects.using('campus3').filter(collegeEmail=temp_e)
            if len(c21) > 0:
                ### Get Password From DB
                c22 = Person.objects.using('campus3').get(collegeEmail=temp_e)
                ### Password Not Match
                # if c22.password != temp_p:
                #     errors["9error020"] = "Signed Failed! Invalid credentials! Error 1"
                ### Bcrypt Password Not Match
                hashPassword_db = c22.password
                # print (bcrypt.checkpw(temp_p.encode(), hashPassword_db.encode()))
                if bcrypt.checkpw(temp_p.encode(), hashPassword_db.encode()):
                    pass
                else:
                    errors["9error021"] = "Signed Failed! Invalid credentials!"
            else:
                ### College Email Not Found
                errors["9error022"] = "Signed Failed! Invalid credentials!"
            ### Prepare Error Messages
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect("/campus3")
            else:
                ### Create A Session 
                request.session["key"]  = str(time.time()) + "-" + str(random.randint(1,99999))
                request.session["id"]  = c22.id
                request.session["adminRight"] = c22.adminRight
                if str(request.session["adminRight"]) == "False":
                    return redirect("/campus3/dashboard/"+str(c22.id))
                else:
                    return redirect("/campus3/admin")
    return redirect("/campus3")

### System Page
def system(request):
    print ("*"*20+" system "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3")
    ### Get All User Info
    c31=userType.objects.using('campus3').all()
    c32=MealCardType.objects.using('campus3').all()
    ### Context Info
    context = {
        "allUserType" : c31,
        "allMealType" : c32,
    }
    return render(request, "campus3/system.html", context)

## adminDashboard Page
def admin(request):
    print ("*"*20+" admin dashboard "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Get All User Info
    c41=Person.objects.using('campus3').all()
    ### Get the User Info
    c42=Person.objects.using('campus3').get(id=request.session["id"])
    ### Context Info
    context = {
        "allPersons" : c41,
        "personInfo" : c42,
        "currentID": request.session["id"],
    }
    return render(request, "campus3/admin.html", context)

## User Dashboard Page
def dashboard(request,userID):
    print ("*"*20+" dashboard "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check If Current User
    if str(request.session["id"]) != str(userID):
        return redirect("/campus3")
    ### Get the User Info
    c51=Person.objects.using('campus3').filter(id=userID)
    ### Get User Types
    c52=userType.objects.using('campus3').all()
    ### Get Group Types
    c53=userGroup.objects.using('campus3').filter(person_ID=userID)
    ## Get Building Info
    c55=Building.objects.using('campus3').filter(ID_building=userID)
    ## Get Parking Info
    c56=Parking.objects.using('campus3').filter(ID_parking=userID)
    ## Get Meal Cards
    c57=MealCardType.objects.using('campus3').all()
    ## Get Meal Plans
    c58=MealGroup.objects.using('campus3').filter(ID_meal=userID)
    ### Total Meal Amout
    totalAmt = 0
    for zz in c58:
        c58a=MealCardType.objects.using('campus3').get(id=zz.ID_mealType.id)
        totalAmt = totalAmt + c58a.CardAmt
    ### Get Person Info
    c59=Person.objects.using('campus3').get(id=userID)
    ## Get date
    temp_extraDay = datetime.datetime.now() + timedelta(days=1)
    temp_dayFormat= temp_extraDay.strftime("%Y-%m-%d")
    ### Calculate Age
    temp_today = datetime.datetime.now().date()
    temp_born = c59.dateBirth
    age = temp_today.year - temp_born.year - ((temp_today.month, temp_today.day) < (temp_born.month, temp_born.day))
    ### Context Info
    context = {
        "currentID": request.session["id"],
        "allPersons" : c51,
        "allUserGroup": c53,
        "allBuilding": c55,
        "allParking": c56,
        "allMealCards": c57,
        "allMealPlans": c58,
        "personInfo" : c59,
        "age" : age,
        "amt" : totalAmt,
        "tomorrow" : datetime.datetime.now() + timedelta(days=-1),
        "expiryDate" : temp_dayFormat,
    }
    return render(request, "campus3/dashboard.html", context)

### User Info Page
def user(request,userID):
    print ("*"*20+" user info "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3")
    ### Get the User Info
    c61=Person.objects.using('campus3').filter(id=userID)
    ### Calculate Age
    c62=Person.objects.using('campus3').get(id=userID)
    temp_today = datetime.datetime.now().date()
    temp_born = c62.dateBirth
    age = temp_today.year - temp_born.year - ((temp_today.month, temp_today.day) < (temp_born.month, temp_born.day))
    ### Get User Types
    c63=userGroup.objects.using('campus3').filter(person_ID=userID)
    ## Get Building Info
    c64=Building.objects.using('campus3').filter(ID_building=userID)
    ## Get Parking Info
    c65=Parking.objects.using('campus3').filter(ID_parking=userID)
    ## Get Meal Cards
    c66=MealCardType.objects.using('campus3').all()
    ## Get Meal Plans
    c67=MealGroup.objects.using('campus3').filter(ID_meal=userID)
    ### Total Meal Amout
    totalAmt = 0
    for zz in c67:
        c67a=MealCardType.objects.using('campus3').get(id=zz.ID_mealType.id)
        totalAmt = totalAmt + c67a.CardAmt
    ### Context Info
    context = {
        "currentID": request.session["id"],
        "allPersons" : c61,
        "allUserGroup": c63,
        "allBuilding": c64,
        "allParking": c65,
        "allMealCards": c66,
        "allMealPlans": c67,
        "age" : age,
        "amt" : totalAmt,
        "tomorrow" : datetime.datetime.now() + timedelta(days=-1),
    }
    return render(request, "campus3/user.html", context)

### Add User Type Logic
def addUserType(request):
    print ("*"*20+" addUserType "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.userType_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/campus3/system")
        else:
            ### Insert Into DB
            userType.objects.using('campus3').create(
                nameType=request.POST.get("inputUserType"), 
            )
    return redirect("/campus3/system")

### Add User Group Logic
def addUserGroup(request,userID):
    print ("*"*20+" addUserGroup "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.userGroup_validator(request.POST)
        temp_group = request.POST.get("inputUserType")
        if str(temp_group) == "0":
            errors["9error030"] = "You did not selected a new user group."
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            ### Check AdminRight
            if str(request.session["adminRight"]) == "False":
                return redirect("/campus3/dashboard/"+userID)
            else:
                return redirect("/campus3/services/"+userID)
        else:
            ### Get the Record
            c71=Person.objects.using('campus3').get(id=userID)
            c72=userType.objects.using('campus3').get(id=request.POST.get("inputUserType"))
            ### Insert UserType Into DB
            userGroup.objects.using('campus3').create(person_ID=c71,userType_ID=c72)
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Manage Services Page
def services(request,userID):
    print ("*"*20+" services "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check If Current User
    # if str(request.session["id"]) != str(userID):
    #     return redirect("/campus3/dashboard/"+userID)
    ## Get date
    temp_extraDay = datetime.datetime.now() + timedelta(days=1)
    temp_dayFormat= temp_extraDay.strftime("%Y-%m-%d")
    ### Get the User Info
    c81=Person.objects.using('campus3').filter(id=userID)
    ### Get User Types
    c82=userType.objects.using('campus3').all()
    ### Get Group Types
    c83=userGroup.objects.using('campus3').filter(person_ID=userID)
    ### Filter Out UserType From GroupType
    c82a=set(c82)
    c83a=set(c83)
    for xx in c83a:
        # print xx.userType_ID.id
        c84=userType.objects.using('campus3').filter(id=xx.id)
        c82a=c82a.difference(c84)
    ## Get Building Info
    c85=Building.objects.using('campus3').filter(ID_building=userID)
    ## Get Parking Info
    c86=Parking.objects.using('campus3').filter(ID_parking=userID)
    ## Get Meal Cards
    c87=MealCardType.objects.using('campus3').all()
    ## Get Meal Plans
    c88=MealGroup.objects.using('campus3').filter(ID_meal=userID)
    ### Total Meal Amout
    totalAmt = 0
    for zz in c88:
        c88a=MealCardType.objects.using('campus3').get(id=zz.ID_mealType.id)
        totalAmt = totalAmt + c88a.CardAmt
    ### Calculate Age
    c89=Person.objects.using('campus3').get(id=userID)
    temp_today = datetime.datetime.now().date()
    temp_born = c89.dateBirth
    age = temp_today.year - temp_born.year - ((temp_today.month, temp_today.day) < (temp_born.month, temp_born.day))
    ### Context Info
    context = {
        "currentID": request.session["id"],
        "allPersons" : c81,
        "allUserType": c82a,
        "allUserGroup": c83,
        "allBuilding": c85,
        "allParking": c86,
        "allMealCards": c87,
        "allMealPlans": c88,
        "age" : age,
        "amt" : totalAmt,
        "tomorrow" : datetime.datetime.now() + timedelta(days=-1),
        "expiryDate" : temp_dayFormat,
    }
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return render(request, "campus3/services.html", context)

### Add Meal Type Logic
def addMealType(request):
    print ("*"*20+" addMealType "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.mealType_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/campus3/system")
        else:
            ### Insert Into DB
            MealCardType.objects.using('campus3').create(
                CardType=request.POST.get("inputMealType"), 
                CardAmt=request.POST.get("inputMealAmt"), 
            )
    return redirect("/campus3/system")

### Add Meal Logic
def addMeal(request,userID):
    print ("*"*20+" addMeal "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.mealGroup_validator(request.POST)
        temp_group = request.POST.get("inputMealCard")
        if str(temp_group) == "0":
            errors["9error040"] = "You did not selected a new meal plan."
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            ### Check AdminRight
            if str(request.session["adminRight"]) == "False":
                return redirect("/campus3/dashboard/"+userID)
            else:
                return redirect("/campus3/services/"+userID)
        else:
            ### Get the Record
            c91=Person.objects.using('campus3').get(id=userID)
            c92=MealCardType.objects.using('campus3').get(id=request.POST.get("inputMealCard"))
            ### Insert MealGroup Into DB
            MealGroup.objects.using('campus3').create(ID_meal=c91,ID_mealType=c92)
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Add Building Office Logic
def addBuilding(request,userID):
    print ("*"*20+" addBuilding "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.building_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            ### Check AdminRight
            if str(request.session["adminRight"]) == "False":
                return redirect("/campus3/dashboard/"+userID)
            else:
                return redirect("/campus3/services/"+userID)
        else:
            ### Get userID
            c101=Person.objects.using('campus3').get(id=userID)
            ### Insert Into DB
            Building.objects.using('campus3').create(
                ID_building=c101,
                buildingName=request.POST.get("inputBuilding"), 
                officeRoom=request.POST.get("inputOffice"), 
            )
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Add Parking Logic
def addParking(request,userID):
    print ("*"*20+" addParking "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.parking_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            ### Check AdminRight
            if str(request.session["adminRight"]) == "False":
                return redirect("/campus3/dashboard/"+userID)
            else:
                return redirect("/campus3/services/"+userID)
        else:
            ### Get userID
            c111=Person.objects.using('campus3').get(id=userID)
            ### Generate Random Permit No
            c112=get_random_string(length=15).upper()
            ### Insert Into DB
            Parking.objects.using('campus3').create(
                ID_parking=c111,
                plateNo=request.POST.get("inputPlateNo").upper(), 
                dateExpiry=request.POST.get("inputExpiryDate"),
                permitNo=c112, 
            )
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Delete Person Group Logic
def deleteGroup(request,userID,noID):
    print ("*"*20+" deleteGroup "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Get and Delete - Person Group 
    c121=userGroup.objects.using('campus3').get(id=noID)
    c121.delete()
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Delete Meal Group Logic
def deleteMeal(request,userID,noID):
    print ("*"*20+" deleteMeal "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Get and Delete - Meal Group 
    c131=MealGroup.objects.using('campus3').get(id=noID)
    c131.delete()
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Delete Building Logic
def deleteBuilding(request,userID,noID):
    print ("*"*20+" deleteBuilding "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Get and Delete - Building 
    c141=Building.objects.using('campus3').get(id=noID)
    c141.delete()
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Delete Parking Logic
def deleteParking(request,userID,noID):
    print ("*"*20+" deleteParking "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Get Parking 
    c151=Parking.objects.using('campus3').get(id=noID)
    c151.delete()
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Update Phone Info
def updatePhone(request,userID):
    print ("*"*20+" updatePhone "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.updatePhone_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            ### Check AdminRight
            if str(request.session["adminRight"]) == "False":
                return redirect("/campus3/dashboard/"+userID)
            else:
                return redirect("/campus3/services/"+userID)
        else:
            c161=Person.objects.using('campus3').get(id=userID)
            c161.phone = request.POST.get("inputUpdatePhone")
            c161.save(using="campus3")
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Update Ext No
def updateExtNum(request,userID):
    print ("*"*20+" updateExtNum "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.updateExtNum_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            ### Check AdminRight
            if str(request.session["adminRight"]) == "False":
                return redirect("/campus3/dashboard/"+userID)
            else:
                return redirect("/campus3/services/"+userID)
        else:
            c171=Person.objects.using('campus3').get(id=userID)
            c171.extNum = request.POST.get("inputUpdateExtNum")
            c171.save(using="campus3")
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Update Person Email
def updatePersonEmail(request,userID):
    print ("*"*20+" updatePersonEmail "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check if the form is POST
    if request.method == "POST":
        ### Input Validation
        errors = Person.objects.updatePersonEmail_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            ### Check AdminRight
            if str(request.session["adminRight"]) == "False":
                return redirect("/campus3/dashboard/"+userID)
            else:
                return redirect("/campus3/services/"+userID)
        else:
            c181=Person.objects.using('campus3').get(id=userID)
            c181.personEmail = request.POST.get("inputUpdatePersonEmail")
            c181.save(using="campus3")
    ### Check AdminRight
    if str(request.session["adminRight"]) == "False":
        return redirect("/campus3/dashboard/"+userID)
    else:
        return redirect("/campus3/services/"+userID)

### Logout
def logout(request):
    print ("*"*20+" logout "+"*"*20)
    ### Remove Session 
    request.session.flush()
    return redirect("/campus3")

### Hack Page
def hack(request,userID):
    print ("*"*20+" hack "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check If Current User
    if str(request.session["id"]) != str(userID):
        ### Check AdminRight
        if str(request.session["adminRight"]) == "False":
            return redirect("/campus3/dashboard/"+userID)
        else:
            return redirect("/campus3/admin")
    ### Get the User Info
    c191=Person.objects.using('campus3').get(id=userID)
    ### Context Info
    context = {
        "personInfo" : c191,
        "adminRight" : str(request.session["adminRight"]),
    }
    return render(request, "campus3/hack.html", context)

### Hacking Logic
def hacking(request,userID):
    print ("*"*20+" hacking "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check If Current User
    if str(request.session["id"]) != str(userID):
        ### Check AdminRight
        if str(request.session["adminRight"]) == "False":
            return redirect("/campus3/dashboard/"+userID)
        else:
            return redirect("/campus3/admin")
    errors = {}
    c201=Person.objects.using('campus3').get(id=userID)
    if str(request.session["adminRight"]) == "False":
        c201.adminRight = True
        errors["9error050"] = "Your account ("+c201.collegeEmail+") has been successful upgraded! Thank you."
    else:
        c201.adminRight = False
        errors["9error051"] = "Your account ("+c201.collegeEmail+") has been successful downgraded! Thank you."
    c201.save(using="campus3")
    ### Prepare Message For New User
    for tag, error in errors.iteritems():
        messages.error(request, error, extra_tags=tag)
    ### Remove Session 
    request.session.flush()
    return redirect("/campus3")

### Hack Page
def destory(request,userID):
    print ("*"*20+" destory "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Initial values
    errors = {}
    summary = " "
    ### Delete User group
    c211=userGroup.objects.using('campus3').filter(person_ID=userID)
    if len(c211) > 0:
        summary = summary + str(len(c211)) +" record(s) of Group. "
    ### Delete Meal group
    c212=MealGroup.objects.using('campus3').filter(ID_meal=userID)
    if len(c212) > 0:
        summary = summary + str(len(c212)) +" record(s) of Meal. "
    ### Delete Building group
    c213=Building.objects.using('campus3').filter(ID_building=userID)
    if len(c213) > 0:
        summary = summary + str(len(c213)) +" record(s) of Building. "
    ### Delete Parking group
    c214=Parking.objects.using('campus3').filter(ID_parking=userID)
    if len(c214) > 0:
        summary = summary + str(len(c214)) +" record(s) of Parking Permit. "
    ### Delete User
    c215=Person.objects.using('campus3').filter(id=userID)
    if len(c215) > 0:
        c215a=Person.objects.using('campus3').get(id=userID)
        summary = "The "+c215a.collegeEmail+" has been deleted. This included "+summary
        errors["9error061"] = summary
    ### Delete all 
    c211.delete()
    c212.delete()
    c213.delete()
    c214.delete()
    c215.delete()
    ### Prepare Message For New User
    for tag, error in errors.iteritems():
        messages.error(request, error, extra_tags=tag)
    ### Check AdminRight
    if str(request.session["id"]) == str(userID):
        request.session.flush()
        return redirect("/campus3")
    else:
        return redirect("/campus3/admin")

### deleteGroupType Logic
def deleteGroupType(request,noID):
    print ("*"*20+" delete GroupType "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check Number of userGroup
    errors = {}
    c221=userGroup.objects.using('campus3').filter(userType_ID=noID)
    c222=userType.objects.using('campus3').get(id=noID)
    if len(c221) > 0:
        errors["9error061"] = "Error! The campus group of "+c222.nameType+" has been assigned to "+str(len(c221))+" record(s). Please unassign from the record(s) first before delete it. Thanks!"
    else:
        errors["9error062"] = "The campus group of "+c222.nameType+" has been deleted."
        c222.delete()
    ### Prepare Message For New User
    for tag, error in errors.iteritems():
        messages.error(request, error, extra_tags=tag)
    return redirect("/campus3/system")

### deleteMealType Logic
def deleteMealType(request,noID):
    print ("*"*20+" delete MealType "+"*"*20)
    ### Check Session 
    if "key" not in request.session:
        return redirect("/campus3")
    ### Check AdminRight
    if "adminRight" not in request.session:
        return redirect("/campus3")
    ### Check Number of mealGroup
    errors = {}
    c231=MealGroup.objects.using('campus3').filter(ID_mealType=noID)
    c232=MealCardType.objects.using('campus3').get(id=noID)
    if len(c231) > 0:
        errors["9error061"] = "Error! The meal card plan group of "+c232.CardType+" has been assigned to "+str(len(c231))+" record(s). Please unassign from the record(s) first before delete it. Thanks!"
    else:
        errors["9error061"] = "The meal group of "+c232.CardType+" has been deleted."
        c232.delete(using="campus3")
    ### Prepare Message For New User
    for tag, error in errors.iteritems():
        messages.error(request, error, extra_tags=tag)
    return redirect("/campus3/system")