Insta Nurse Alexa Skill
=======================

This is the Alexa Skill created for Diagonizing the symptoms of the user and provide with a short description about our diagnosis.

File Structure
==============
InstaNurse.py			-> Contains alexa interaction model
PriaidDiagnosisClient.py	-> Contains sample Application code to interact with the api
Symptoms.txt			-> Contains list of symptoms to work with
config.py			-> Contains the user credential 


Platform
========
Python 3.5
Flask
Flask-ask
unidecode
ngrok
AWS developer console

Instruction to Compile and Run
==============================

run below commands in the extracted folder
-> cd InstaNurse
-> python3.5 InstaNurse.py

In a new terminal run the below commands
-> ./ngrok http 5000

-> copy and paste the sample utterence, Intent Schema and Slot in the respecive places
-> copy and paste in the developer console at configuration tab

