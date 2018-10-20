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


SKILL_NAME = "Duluth Facts"
FACT_MESSAGE = "Here's your Duluth Fact: "

facts = [
	'In the late 1800s and early 1900s, the city of Duluth was home to more millionaires per capita than any other city in the world',
	'1 out of ever 7 Duluth residents are employed in the medical field',
	'Over 1000 ocean-going and freshwater ships use the Port of Duluth annually',
	'The Duluth harbor is 2,342 miles from the Atlantic',
	'On average, 40 million metric tons of cargo pass through the Twin Ports aboard 1,100 vessels each year',
	'Minnesota Point is the longest fresh-water sandspit in the world',
	'Duluth extends 24 miles along Lake Superior shores',
	'The Lake Superior Zoo was established in 1923 under the city’s permission to construct a pen for a pet deer',
	'Canal Park was historically used as an industrial dumping ground and also contained the area’s red light district.',
	'From 1891 to 1939 Duluth had an extensive cable car system',
	'In 1905 the Aerial Transfer Bridge was constructed, with a large gondola capable of carrying up to 60 tons of traffic',
	'In 1929, the lift bridge in Duluth was modified into today’s Aerial Lift bridge',
	'Chester Congdon donated funds for the City of Duluth to purchase the land along the eastern shoreline in order to preserve the area in its natural state and remain undeveloped',
]

sb = SkillBuilder()

class DuluthFactHandler(AbstractRequestHandler):
    
	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input) or
				is_intent_name("NewDuluthFact")(handler_input))
        
	def handle(self, handler_input):
		logging.info("Starting Default")

		duluth_fact = random.choice(facts)
		speech = FACT_MESSAGE + duluth_fact

		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response

class HelpHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("AMAZON.HelpIntent")(handler_input))
		
	def handle(self, handler_input):
		speech = "You can ask me for a Duluth fact!"
		
		handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech)).ask(speech)
		return handler_input.response_builder.response

class CancelOrStopHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return(is_intent_name("AMAZON.CancelIntent")(handler_input) or
            is_intent_name("AMAZON.StopIntent")(handler_input) or
            is_request_type("SessionEndedRequest")(handler_input))
    
    def handle(self, handler_input):
        handler_input.response_builder.speak("Goodbye")
        return handler_input.response_builder.response		
		
sb.add_request_handler(DuluthFactHandler())
sb.add_request_handler(HelpHandler())
sb.add_request_handler(CancelOrStopHandler())

lambda_handler = sb.lambda_handler()