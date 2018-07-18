from __future__ import unicode_literals

from django.db import models

# Create your models here.

import re
CAMPUSID_REGEX = re.compile(r'\*[0-9]{8}')
PHONE_REGEX = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
EXTNUM_REGEX = re.compile(r'\d{4}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATE_REGEX = re.compile(r'19|20[0-9]{2}-[0-9]{2}-[0-9]{2}')

from datetime import datetime, timedelta

class PersonManager(models.Manager):
    def person_validator(self, postData):
        errors = {}
        today = str(datetime.now())[:10] 
        year12 = str(datetime.now()+ timedelta(days=-4380))[:10] # 4380 = 12 years
        print today, year12

        if len(postData['inputFirstName']) < 3:
            errors["1error010"] = "Registration failed! The first name required minimum of 3 characters."

        if len(postData['inputLastName']) < 3:
            errors["1error020"] = "Registration failed! The last name required minimum of 3 characters."

        if len(postData["inputDateBirth"]) < 10 or not DATE_REGEX.match(postData["inputDateBirth"]):
            errors["1error030"] = "Registration failed! Invalid date format in date of birth."
        elif str(postData["inputDateBirth"]) > year12:
            errors["1error031"] = "Registration failed! The person should be at least 12 years old!"

        if len(postData['inputAddress']) < 5:
            errors["1error040"] = "Registration failed! The address required minimum of 5 characters."
        
        if len(postData["inputPhone"]) < 9 or not PHONE_REGEX.match(postData["inputPhone"]):
            errors["1error050"] = "Registration failed! Invalid phone number format. Ex. 999-999-9999."

        if len(postData["inputExtNum"]) < 4 or not EXTNUM_REGEX.match(postData["inputExtNum"]):
            errors["1error060"] = "Registration failed! Invalid extension number format. Ex. 9999."

        if len(postData['inputBuilding']) < 3:
            errors["1error070"] = "Registration failed! The building name required minimum of 3 characters."
        
        if len(postData['inputOffice']) < 3:
            errors["1error071"] = "Registration failed! The office room required minimum of 3 characters."

        if len(postData['inputPersonEmail']) < 7 or not EMAIL_REGEX.match(postData['inputPersonEmail']):
            errors["1error080"] = "Registration failed! Invalid personal email address!"

        if len(postData['inputPassword1']) < 8:
            errors["1error090"] = "Registration failed! The password required minimum of 8 characters"
        elif len(postData['inputPassword2']) < 8:
            errors["1error091"] = "Registration failed! The confirm password required minimum of 8 characters"

        if postData['inputPassword1'] != postData['inputPassword2']:
            errors["1error100"] = "Registration failed! Password and confirm password should be matched!"

        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['inputCollegeEmail']) < 7 or len(postData['inputPassword']) < 8:
            errors["2error1"] = "Signed Failed! Invalid credentials!"
        return errors

    def userType_validator(self, postData):
        errors = {}
        if len(postData['inputUserType']) < 3:
            errors["3error1"] = "The description of campus group required minimum of 3 characters."
        return errors

    def userGroup_validator(self, postData):
        errors = {}
        return errors

    def mealType_validator(self, postData):
        errors = {}
        if len(postData['inputMealType']) < 3:
            errors["4error1"] = "The description of meal card type required minimum of 3 characters."
        if len(postData['inputMealAmt']) < 1:
            errors["4error2"] = "The amount of meal card is missing."
        return errors

    def mealGroup_validator(self, postData):
        errors = {}
        return errors

    def building_validator(self, postData):
        errors = {}
        if len(postData['inputBuilding']) < 3:
            errors["5error1"] = "The building name required minimum of 3 characters."
        if len(postData['inputOffice']) < 3:
            errors["5error2"] = "The office room required minimum of 3 characters."
        return errors

    def parking_validator(self, postData):
        errors = {}
        if len(postData['inputPlateNo']) < 6 or len(postData['inputPlateNo']) > 6 :
            errors["6error1"] = "The vehicle plate number required 6 characters only."
        return errors

    def updatePhone_validator(self, postData):
        errors = {}
        if len(postData["inputUpdatePhone"]) < 9 or not PHONE_REGEX.match(postData["inputUpdatePhone"]):
            errors["7error1"] = "Updates failed! Invalid phone number format. Ex. 999-999-9999."
        return errors

    def updateExtNum_validator(self, postData):
        errors = {}
        if len(postData["inputUpdateExtNum"]) < 4 or not EXTNUM_REGEX.match(postData["inputUpdateExtNum"]):
            errors["7error2"] = "Updates failed! Invalid extension number format. Ex. 9999."
        return errors

    def updatePersonEmail_validator(self, postData):
        errors = {}
        if len(postData['inputUpdatePersonEmail']) < 7 or not EMAIL_REGEX.match(postData['inputUpdatePersonEmail']):
            errors["7error3"] = "Updates failed! Invalid personal email address!"
        return errors

class Person(models.Model):
    campusID = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255)
    dateBirth = models.DateTimeField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    extNum = models.CharField(max_length=10)
    personEmail = models.CharField(max_length=255)
    collegeEmail = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)

    objects = PersonManager()

class userType(models.Model):
    nameType = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)

class userGroup(models.Model):
    person_ID = models.ForeignKey(Person, related_name="personGroupID")
    userType_ID = models.ForeignKey(userType, related_name="userTypeID")
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)

class Building(models.Model):
    ID_building = models.ForeignKey(Person, related_name="personBuildingID")
    buildingName = models.CharField(max_length=255)
    officeRoom = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)

class Parking(models.Model):
    ID_parking = models.ForeignKey(Person, related_name="personParkingID")
    plateNo = models.CharField(max_length=255)
    permitNo = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)

class MealCardType(models.Model):
    CardType = models.CharField(max_length=255)
    CardAmt = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)

class MealGroup(models.Model):
    ID_meal = models.ForeignKey(Person, related_name="personMealID")
    ID_mealType = models.ForeignKey(MealCardType, related_name="mealTypeID")
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)