# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
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

from rasa_sdk import Action

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

# from rasa_sdk.events import ActiveLoop, SlotSet

# class ActionChangeFlightDate(Action):
#     def name(self):
#         return "action_change_flight_date"

#     def run(self, dispatcher, tracker, domain):
#         previous_form = tracker.get_slot("previous_form")
#         new_date = tracker.get_slot("date")

#         return_events = [
#             SlotSet("flight_date", new_date),
#             ActiveLoop(None), 
#             SlotSet("requested_slot", None)
#         ]

#         if previous_form == "flight_status_form":
#           dispatcher.utter_message(text=f"Updating flight date for flight status check to {new_date}...")
#           return_events.append(ActiveLoop("flight_status_form"))  # Reactivate flight_status_form

#         elif previous_form == "flights_search_form":
#             dispatcher.utter_message(text=f"Updating flight date for scheduled flights search to {new_date}...")
#             return_events.append(ActiveLoop("flights_search_form"))  # Reactivate flights_search_form

#         return return_events
