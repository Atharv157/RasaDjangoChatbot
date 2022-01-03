# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .mysqlconn import check_mail
import random
from .otp import send_otp

#
#TEMPLATE FOR CLASS
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
 

 
class ActionAuthInform(Action):

    def name(self) -> Text:
        return "action_authinform"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        verified_email = tracker.get_slot("verified_email")
        if verified_email is not None:
            dispatcher.utter_message("You are already verified.")
        else:
            email = tracker.get_slot('email')
            otp = tracker.get_slot('authotp')
            #case to be activated when email is set and otp is not set
            if email is not None and otp is None:
                #email exists in db
                if check_mail(email):
                    tempotp = random.randint(1000, 9999)
                    if not send_otp(tempotp,email):
                        dispatcher.utter_message("Error occcured while sending OTP")
                    dispatcher.utter_message(response="utter_ask_authotp")
                    return [SlotSet("sendotp",str(tempotp))]
                else:
                    dispatcher.utter_message("Please enter correct email")
                    return[SlotSet("email", None)]
            #if this is the case then check if otp is matching or not
            elif email is not None and otp is not None:
                sendotp = tracker.get_slot("sendotp")
                if otp == sendotp:
                    #verified
                    dispatcher.utter_message("Thanks for the info. I have successfully authenticated you. You may ask any query now.")
                    return [SlotSet("verified_email",email),SlotSet("authotp",None),SlotSet("sendotp",None)]
                else:
                    #ask for correct info
                    # "Verification failed. Please start over by providing email again. Sorry for the inconvenience"
                    dispatcher.utter_message(sendotp)
                    return [SlotSet("email",None),SlotSet("authotp",None),SlotSet("sendotp",None)]
        
        return []


