# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from rasa_sdk import Action
from typing import Any, Text, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from .advancedDataParser import AdvancedDateParser
from .airportMapper import AirportMapper

class ActionUtterPlacesResponse(Action):
  def name(self):
    return "action_utter_places_response"

  def run(self, dispatcher, tracker, domain):
    intent = tracker.get_intent_of_latest_message()

    # Mapping intents to corresponding utter responses
    response_mapping = {
        "check_popular_places": "utter_popular_places",
        "check_restaurant": "utter_restaurant",
        "check_dessert": "utter_dessert",
        "check_cafe": "utter_cafe",
        "check_bar": "utter_bar",
        "check_night_market": "utter_night_market",
        "check_entertainment": "utter_entertainment",
        "check_shopping": "utter_shopping",
    }

    # Get the appropriate response action
    response_action = response_mapping.get(intent)

    if response_action:
        dispatcher.utter_message(response=response_action)
    else:
        dispatcher.utter_message(text="Sorry, I couldn't find that information.")

    return []

class ValidateFlightStatusForm(FormValidationAction):
  def name(self) -> Text:
    return "validate_flight_status_form"

  async def validate_date(
    self,
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
  ) -> Dict[Text, Any]:
    if not slot_value:
      dispatcher.utter_message(text="Please provide a valid date.")
      return {'date': None}
        
    result = AdvancedDateParser.parse_date(slot_value)
    if not result:
      dispatcher.utter_message(
        text="Please provide a date in one of these formats:\n"
              "- Standard (15-03-2023 or 2023-03-15)\n"
              "- Month name (15 March 2023)\n"
              "- Natural (tomorrow, next Monday)\n"
              "- Holiday (Christmas, New Year's Eve)"
      )
      return {'date': None}
        
    _, formatted_date = result
    return {'date': formatted_date}
    
  async def validate_flight_number(
    self,
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
  ) -> Dict[Text, Any]:
    if not slot_value:
      dispatcher.utter_message(text="Please provide a valid flight number.")
      return {'flight_number': None}
    
    return {'flight_number': slot_value.upper()}
  
class ValidateFlightsSearchForm(FormValidationAction):
  def __init__(self):
    super().__init__()
    self.airport_mapper = AirportMapper("C:/Users/ASUS/Documents/vscode/Machine Learning/Rasa Projects/JetSetGo-Bot/actions/airports_lookup.txt")

  def name(self) -> Text:
    return "validate_flights_search_form"

  async def validate_departure(
    self,
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
  ) -> Dict[Text, Any]:
    if not slot_value:
      dispatcher.utter_message(text="Please provide a valid departure IATA.")
      return {'departure': None}
    
    iata_code = self.airport_mapper.find_iata(slot_value)

    if not iata_code:
      dispatcher.utter_message(
        text=f"Sorry, I couldn't find an airport matching '{slot_value}'. "
        "Please provide a valid IATA code or airport name."
      )
      return {'departure': None}

    return {'departure': iata_code}

  async def validate_arrival(
    self,
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
  ) -> Dict[Text, Any]:
    if not slot_value:
      dispatcher.utter_message(text="Please provide a valid arrival IATA.")
      return {'arrival': None}

    iata_code = self.airport_mapper.find_iata(slot_value)

    if not iata_code:
      dispatcher.utter_message(
        text=f"Sorry, I couldn't find an airport matching '{slot_value}'. "
        "Please provide a valid IATA code or airport name."
      )
      return {'arrival': None}
    
    return {'arrival': iata_code}
  
  async def validate_date(
    self,
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
  ) -> Dict[Text, Any]:
    if not slot_value:
      dispatcher.utter_message(text="Please provide a valid date.")
      return {'date': None}
    
    result = AdvancedDateParser.parse_date(slot_value)
    if not result:
      dispatcher.utter_message(
        text="Please provide a date in one of these formats:\n"
              "- Standard (15-03-2023 or 2023-03-15)\n"
              "- Month name (15 March 2023)\n"
              "- Natural (tomorrow, next Monday)\n"
              "- Holiday (Christmas, New Year's Eve)"
      )
      return {'date': None}
      
    _, formatted_date = result
    return {'date': formatted_date}
  
class ValidateHotelsForm(FormValidationAction):
  def name(self) -> Text:
    return "validate_hotels_form"

  async def validate_location(
    self,
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
  ) -> Dict[Text, Any]:
    if not slot_value:
      dispatcher.utter_message(text="Please provide a location.")
      return {'location': None}
    
    return {'location': slot_value}
  
  async def validate_check_in(
    self,
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
  ) -> Dict[Text, Any]:
    if not slot_value:
      dispatcher.utter_message(text="Please provide a valid check-in date.")
      return {'check_in': None}
    
    result = AdvancedDateParser.parse_date(slot_value)
    if not result:
      dispatcher.utter_message(
        text="Please provide a date in one of these formats:\n"
              "- Standard (15-03-2023 or 2023-03-15)\n"
              "- Month name (15 March 2023)\n"
              "- Natural (tomorrow, next Monday)\n"
              "- Holiday (Christmas, New Year's Eve)"
      )
      return {'check_in': None}
      
    _, formatted_date = result
    return {'check_in': formatted_date}
  
  async def validate_check_out(
    self,
    slot_value: Any,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
  ) -> Dict[Text, Any]:
    if not slot_value:
      dispatcher.utter_message(text="Please provide a valid check-out date.")
      return {'check_out': None}
    
    result = AdvancedDateParser.parse_date(slot_value)
    if not result:
      dispatcher.utter_message(
        text="Please provide a date in one of these formats:\n"
              "- Standard (15-03-2023 or 2023-03-15)\n"
              "- Month name (15 March 2023)\n"
              "- Natural (tomorrow, next Monday)\n"
              "- Holiday (Christmas, New Year's Eve)"
      )
      return {'check_out': None}
      
    _, formatted_date = result
    return {'check_out': formatted_date}