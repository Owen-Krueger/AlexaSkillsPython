import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


SKILL_NAME = "Titanic Facts"
FACT_MESSAGE = "Here's your Titanic Fact: "

facts = [
	'The Titanic was 269.1 meters or 882 feet and 9 inches long',
	'The Titanic used 825 tons of coal a day',
	'There were approximately 10,000 lamp bulbs used on the ship',
	'The Titanic cost 7 mililon 5 hundred thousand dollars to make',
	'Two workers were killed during the construction of the Titanic',
	'Twenty horses were needed to transport the main anchor',
	'There were 13 honeymooning couples on the maiden voyage of the Titanic',
	'31.6 percent of passengers and crew survived',
	'There were 2,223 people aboard the Titanic',
	'The Titanic could hold a maximum of 3,547 people',
	'The Titanic was equipped to hold 64 lifeboats',
	'The Titanic was actually carrying 20 lifeboats',
	'14,000 gallons of drinking water were used every 24 hours',
]

sb = SkillBuilder()

class TitanicFactHandler(AbstractRequestHandler):
    
	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input) or
				is_intent_name("NewTitanicFact")(handler_input))
        
	def handle(self, handler_input):
		logging.info("Starting Default")

		titanic_fact = random.choice(facts)
		speech = FACT_MESSAGE + titanic_fact

		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response

class HelpHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("AMAZON.HelpIntent")(handler_input))
		
	def handle(self, handler_input):
		speech = "You can ask me for a Titanic fact!"
		
		handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech)).ask(speech)
		return handler_input.response_builder.response

sb.add_request_handler(TitanicFactHandler())
sb.add_request_handler(HelpHandler())

lambda_handler = sb.lambda_handler()