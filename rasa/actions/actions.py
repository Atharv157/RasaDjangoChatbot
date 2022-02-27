# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

#rasa run -m models --enable-api --cors "*" --debug
#rasa run actions --cors "*" --debug
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#from importlib_metadata import email
from rasa_sdk.events import SlotSet, UserUttered
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .query import *
import random
from .otp import send_otp,send_transaction_alert
from rasa_sdk.forms import FormValidationAction
from forex_python.converter import CurrencyRates

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
        amount = tracker.get_slot('amount')
        receiver = tracker.get_slot('receiver')
        email = tracker.get_slot('email')
        # send_transfer_otp = tracker.get_slot('send_transfer_slot')
        # transfer_otp = tracker.get_slot('transfer_otp')
        if verified_email is not None:
            dispatcher.utter_message("You are already verified.")
        # elif amount is not None and receiver is not None and email is None:
        #     dispatcher.utter_message("For security reasons, I have to authenticate you, Can I please get your email address. Thank you")
        elif amount is not None and receiver is not None and email is not None:
            tempotp = random.randint(10000, 99999)
            if send_otp(tempotp,email):    
                dispatcher.utter_message("Enter the transaction otp")
                return [SlotSet("send_transfer_otp",tempotp)]
            else:
                dispatcher.utter_message("Internal error, please try again later")
                return[SlotSet('amount',None), SlotSet('receiver',None),SlotSet('transfer_otp',None),SlotSet('send_transfer_otp',None)]

        else:
            email = tracker.get_slot('email')
            otp = tracker.get_slot('authotp')
            #case to be activated when email is set and otp is not set
            if email is not None and otp is None:
                #email exists in db
                if check_mail(email):
                    tempotp = random.randint(100000, 999999)
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
                    dispatcher.utter_message("Verification failed. Please start over by providing email again. Sorry for the inconvenience")
                    return [SlotSet("email",None),SlotSet("authotp",None),SlotSet("sendotp",None)]
        
        return []

class ActionAccountBalance(Action):

    def name(self) -> Text:
        return "action_account_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        verified_email = tracker.get_slot("verified_email")
        if verified_email is None:
            dispatcher.utter_message("For security reasons, I have to authenticate you, Can I please get your email address. Thank you")
        else:
            answer = "Your account balance is "+ str(get_balance(verified_email))
            dispatcher.utter_message(answer)
            
        return []



class PinChange(Action):

    def name(self) -> Text:
        return "action_pin_change"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        verified_email = tracker.get_slot("verified_email")
        if verified_email is not None:
            pin = tracker.get_slot('pin')
            if pin is not None:
                # pin is provided
                if len(pin) != 4 or pin.isdigit() == False: 
                    dispatcher.utter_message("Invalid pin (pin should be of 4-digits only)")
                    return [SlotSet('pin',None)]  
                if change_pin(verified_email,pin):
                    dispatcher.utter_message("Pin updated")
                    return [SlotSet("pin",None)]
                else:
                    dispatcher.utter_message("Problem occured while updating pin. Please try again later. Sorry for the inconvinience")
            else:
                # pin not provided
                dispatcher.utter_message('Enter a 4-digit new pin')
        else:
            dispatcher.utter_message("For security reasons, I have to authenticate you, Can I please get your email address. Thank you")
        

        return []
class UnsetPin(Action):

    def name(self) -> Text:
        return "action_unset_pin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_ask_question")

        return [SlotSet('pin',None)]

class PhonenoChange(Action):

    def name(self) -> Text:
        return "action_change_phoneno"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        verifed_email = tracker.get_slot("verified_email")
        if verifed_email is not None:
            phoneno = tracker.get_slot('phoneno')
            if phoneno is not None:
                if len(phoneno) != 10 or phoneno.isdigit() == False: 
                    dispatcher.utter_message("Invalid phone number (Phone number should be of 10-digits only)")
                    return [SlotSet('phoneno',None)] 
                    # phoneno is provided
                if change_phoneno(verifed_email,phoneno):
                    dispatcher.utter_message("Phone number updated")
                    return [SlotSet("phoneno",None)]
                else:
                    dispatcher.utter_message("Problem occured while updating phone number. Please try again later. Sorry for the inconvinience")
            else:
                # phoneno not provided
                dispatcher.utter_message('Enter the new phone number')
        else:
            dispatcher.utter_message("For security reasons, I have to authenticate you, Can I please get your email address. Thank you")
        

        return []



class BlockCard(Action):

    def name(self) -> Text:
        return "action_block_card"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        verified_email = tracker.get_slot("verified_email")
        if verified_email is None:
            dispatcher.utter_message("For security reasons, I have to authenticate you, Can I please get your email address. Thank you")
        else:
            card_no = block_card(verified_email)
            if card_no is None: 
                dispatcher.utter_message("Problem occured while blocking your card. Please try again later or contact branch.")
            else:
                encrypt_card_no = "X"*12 + card_no[-1:-5:-1]
                answer = "Your card {} has been blocked.".format(encrypt_card_no)
                dispatcher.utter_message(answer)

        return []

class FreezeAccount(Action):

    def name(self) -> Text:
        return "action_freeze_account"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        verified_email = tracker.get_slot("verified_email")
        
        if verified_email is None:
            dispatcher.utter_message("For security reasons, I have to authenticate you, Can I please get your email address. Thank you")
        else:
            acc_no = freeze_account(verified_email)
            if acc_no is None: 
                dispatcher.utter_message("Problem occured while freezing your account. Please try again later or contact branch.")
            else:
                answer = "Your account {} has been freezed. To reactivate contact branch".format(acc_no)
                dispatcher.utter_message(answer)

        return []    

class ActionTransferMoney(Action):
    def name(self) -> Text:
        return "action_transfer_money"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        amount = tracker.get_slot("amount")
        receiver = tracker.get_slot("receiver")
        transfer_otp = tracker.get_slot("transfer_otp")
        verified_email = tracker.get_slot("verified_email")
        send_transfer_otp = tracker.get_slot("send_transfer_otp")
        email = tracker.get_slot("email")
        if verified_email is None and email is None:
            dispatcher.utter_message("For security reasons, I have to authenticate you, Can I please get your email address. Thank you")
        elif amount is not None and receiver is not None and transfer_otp is None:
            #firstly validating receiver
            if(not check_account_number_exists(verified_email,receiver)):
                dispatcher.utter_message("Failed to process the transaction. Invalid beneficiary account number. Please reintialize the process.")
                return[SlotSet('amount',None), SlotSet('receiver',None),SlotSet('transfer_otp',None),SlotSet('send_transfer_otp',None)]
            # validating the amount
            if(not check_balance_before_transfer(verified_email, amount)):
                dispatcher.utter_message("Transfer amount exceeds the available account balance. Please reintialize the process.")
                return[SlotSet('amount',None), SlotSet('receiver',None),SlotSet('transfer_otp',None),SlotSet('send_transfer_otp',None)]
            elif amount is not None and receiver is not None and transfer_otp is None:
                tempotp = random.randint(10000, 99999)
                if send_otp(tempotp,verified_email):    
                    dispatcher.utter_message("Enter the transaction otp")
                    return [SlotSet("send_transfer_otp",tempotp)]
                else:
                    dispatcher.utter_message("Internal error, please try again later")
                    return [SlotSet('amount',None), SlotSet('receiver',None),SlotSet('transfer_otp',None),SlotSet('send_transfer_otp',None)]
        elif amount is not None and receiver is not None and transfer_otp is not None and send_transfer_otp is not None:
            if str(send_transfer_otp)==str(transfer_otp):
                transaction_id = transfer(amount,receiver,verified_email=email)
                if transaction_id:
                    message = "Transaction Completed. Transaction reference ID is {}. Please take a note of it. Thank You".format(transaction_id)
                    dispatcher.utter_message(message)
                    send_transaction_alert(transaction_id,amount) 
                    if verified_email is None:
                        return [SlotSet('amount',None), SlotSet('receiver',None),SlotSet('transfer_otp',None),SlotSet('send_transfer_otp',None),SlotSet('verified_email',email)]
                    else:
                        return [SlotSet('amount',None), SlotSet('receiver',None),SlotSet('transfer_otp',None),SlotSet('send_transfer_otp',None)]
                else:
                    dispatcher.utter_message("Transaction cancelled. Please try again later.")
                    return [SlotSet('amount',None), SlotSet('receiver',None),SlotSet('transfer_otp',None),SlotSet('send_transfer_otp',None)]
            else:
                dispatcher.utter_message("Wrong OTP. Please try again")      
                return [SlotSet('amount',None), SlotSet('receiver',None),SlotSet('transfer_otp',None),SlotSet('send_transfer_otp',None)]  
        return []





class ValidateTransferForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_transfer_form"
    def validate_receiver(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        receiver = slot_value
            # basic validation of digits and length
        if(not receiver.isdigit() or len(receiver) != 12):
            return {"receiver": None}
    
        return {"receiver": slot_value}

    def validate_amount(self, 
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        amountstr = slot_value
        amount = int(amountstr)
        #isAmount valid
        if (not amount or not amountstr.isdigit() or amount<=0): 
            return {"amount": None}
        return {"amount": slot_value}


class ExchangeRate(Action):

    def name(self) -> Text:
        return "action_exchange_rate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        input_currency = tracker.get_slot("input_currency")
        output_currency = tracker.get_slot("output_currency")
        if input_currency is not None and output_currency is not None:
            c = CurrencyRates()
            answer = round(c.get_rate(input_currency,output_currency),4)
            dispatcher.utter_message("1 {} = {} {}".format(input_currency,answer,output_currency))
        else:
            dispatcher.utter_message("Error occured while checking exchange rates. Please try again later.")

        return []


class MiniStatement(Action):

    def name(self) -> Text:
        return "action_mini_statement"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        verified_email = tracker.get_slot("verified_email")
        if verified_email is None:
            dispatcher.utter_message("For security reasons, I have to authenticate you, Can I please get your email address. Thank you")
        else:
            statement = get_mini_statement(verified_email)
            if statement is None:
                dispatcher.utter_message(text="Failed to load mini-account statement.")
            else:
                row_template = '''
                    <tr class="trBorder">
                            <!-- content inside <td> -->
                            <td>{}</td>
                            <td>{}</td>
                            <td>{}</td>
                    </tr>
                '''
                rows  = ""
                for item in statement:
                    newrow = row_template.format(str(item[0])[0:10],item[1],item[2])
                    rows = rows + newrow
                htmlstring = '''
                <html>
                <body>
                    <table>
                        <tr class="trBorder">
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Status</th>
                        </tr>
                        {}
                    </table>
                </body>
                </html>'''
                print(rows)
                htmlstring = htmlstring.format(rows)
                htmlstring = htmlstring.replace("\n", "")
                htmlstring = htmlstring.replace(" ","")
                
                dispatcher.utter_message("Your mini account statement"+htmlstring)
        return []

class BranchLocator(Action):

    def name(self) -> Text:
        return "action_branch_locator"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("location")
        if city is None:
            dispatcher.utter_message("Please enter your city name")
        else:
            locations = get_branch_location(city.capitalize())
            if locations is None:
                dispatcher.utter_message("We don't have any branches in this city. Here's a list of our branch locations.")
                all_locations = get_all_location()
                locationset = set()
                for item in all_locations:
                    locationset.add(item[0])
                listentry = ""
                for item in locationset:
                    listentry = listentry + "<li>{}</li>".format(item)
                htmlstring = '''<ul>{}</ul>'''.format(listentry)
                dispatcher.utter_message(htmlstring)
                return [SlotSet('location',None)]
            else:
                dispatcher.utter_message("Address of branches in {}".format(city.capitalize()))
                for item in locations:
                    dispatcher.utter_message(item[-1])
                return [SlotSet("location",None)]
        return []