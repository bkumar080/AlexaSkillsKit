from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import PriaidDiagnosisClient
import random
import config
import sys
import datetime

Gender_val = ''
SymptomsVal = []
YearBorn = 0
report = ''


app = Flask(__name__)
ask = Ask(app,"/insta_nurse")

def get_diagnosis(usrSymps, usrGender, usrYear):
	now = datetime.datetime.now()
	currentYear = now.year
	print(usrSymps)
	with open('symptoms.txt') as json_file:
		sympData = json.load(json_file)
	usrSymps = [i.lower() for i in usrSymps]
	selectedSymptomsIds = [s['ID'] for s in sympData if s['Name'].lower() in usrSymps]

	if usrGender == 'Male':
		diagnosis = diagnosisClient.loadDiagnosis(selectedSymptomsIds, PriaidDiagnosisClient.Gender.Male, usrYear)
	else:
		diagnosis = diagnosisClient.loadDiagnosis(selectedSymptomsIds, PriaidDiagnosisClient.Gender.Female, usrYear)

	# print(diagnosis)
	str1, str2, str3 = '', '', ''

	for d in diagnosis:
		str1 += d['Issue']['Name'] + ' , or , '
		if d['Issue']['Ranking'] == 1:
			mainIssueId = d['Issue']['ID']

	issueInfo = diagnosisClient.loadIssueInfo(mainIssueId)

	str2 = 'Here is a Short Description about ' + issueInfo['Name'] + '. ' + issueInfo['DescriptionShort']
	str3 = 'Medical Condition.' + issueInfo['MedicalCondition'] + '. Possible Symptoms.' + issueInfo[
		'PossibleSymptoms'] + '. Treatment Description.' + issueInfo['TreatmentDescription']
	
	return [str1.rstrip(' , or , '), str2, str3]

@app.route('/')
def homepage():
	return "Welcome to Insta Nurse. I am a digital medical assistant to provide you with the symptoms"

@ask.launch
def start_skill():
	welcome_message = 'Welcome to Insta Nurse. I am a digital medical assistant, to provide you with the diagnosis of your symptoms. Please tell me your gender?.. For example Male, or, Female.'
	return question(welcome_message)

@ask.intent("GenderIntent")
def gender_intent(Gender):
	global Gender_val
	Gender_val = Gender
	year_born_msg = 'Please tell me your Birth Year? For instance, 1994'
	return question(year_born_msg)

@ask.intent("YearIntent")
def YearBorn_intent(Year_Born):
	global YearBorn
	YearBorn = Year_Born
	symptoms_msg = 'Please tell me one of your Symptom. For instance, Headache.. or... I am having headache'
	return question(symptoms_msg)

@ask.intent("SymptomsIntent")
def symptoms_intent(Symptoms):
	global SymptomsVal
	SymptomsVal.append(Symptoms)
	question_msg = 'Do you face any other symptoms? Other than '+Symptoms
	print (question_msg , SymptomsVal)
	return question(question_msg)

@ask.intent("YesIntent")
def yes_intent():
	symptoms_msg = 'Ok, Now tell me the next Symptom.'
	return question(symptoms_msg)

@ask.intent("NoIntent")
def no_intent():
	DiagResult = get_diagnosis(SymptomsVal,Gender_val,YearBorn)
	global report
	report =  DiagResult[2]
	global SymptomsVal
	SymptomsVal = []
	diag_msg = 'Oh! it seems like you are facing '+ DiagResult[0] + '. ' + DiagResult[1] + '. If you want more information about it. Say, Elaborate it.. else.. Say, Terminate, to conclude diagnosis'
	return question(diag_msg)

@ask.intent("DetailIntent")
def det_intent():
	report_msg = report+'. Get well soon'
	return statement(report_msg)

@ask.intent("TerminateIntent")
def ter_intent():
	ter_msg = 'My diagnosis is for a knowledge purpose, Kindly visit the nearby doctor to have a detailed report. Hope you get well soon'
	return statement(ter_msg)

@ask.intent("FinishIntent")
def conc_intent():
	finish_text = 'Sure, Thank you for patiently listening to our work... I hope you enjoyed. And special thanks to the Google and JP Morga representatives, for spending your valueable time with us. Have a wonderful evening. Good bye.'
	return statement(finish_text)

if __name__ == '__main__':
	username = config.username
	password = config.password
	authUrl = config.priaid_authservice_url
	healthUrl = config.priaid_healthservice_url
	language = config.language

	diagnosisClient = PriaidDiagnosisClient.DiagnosisClient(username, password, authUrl, language, healthUrl)

	app.run(debug=True)




