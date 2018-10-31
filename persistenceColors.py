import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import boto3
from boto3 import resource

SKILL_NAME = "Favorite Color"

sb = SkillBuilder()
logger = logging.getLogger()

class DefaultHandler(AbstractRequestHandler):

	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input))
		
	def handle(self, handler_input):
		speech = "You can ask me to remember a color or to tell you what your favorite color is"
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response
		
class SetFavoriteColorHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("SetFavoriteColor")(handler_input))
		
	def handle(self, handler_input):
		slots = handler_input.request_envelope.request.intent.slots
	
		if 'FavoriteColor' in slots:
			favoriteColor = slots['FavoriteColor'].value
			
			if favoriteColor is not None:
		
				handler_input.attributes_manager.session_attributes['favoriteColor'] = favoriteColor;
					
				speech = "Got it. Your favorite color is " + handler_input.attributes_manager.session_attributes['favoriteColor']
				reprompt = "You can ask me what your favorite color is"
				
			else:
				speech = "Sorry, we had an issue"
				reprompt = "Try to ask me to remember another favorite color"
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech)).ask(reprompt)
		return handler_input.response_builder.response
		
class GetFavoriteColorHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("GetFavoriteColor")(handler_input))
		
	def handle(self, handler_input):
		if 'favoriteColor' in handler_input.attributes_manager.session_attributes:
			myFavoriteColor = handler_input.attributes_manager.session_attributes['favoriteColor']
			speech = "Your favorite color is " + myFavoriteColor
			
		else:
			speech = "I don't think I know your favorite color"

		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response

class HelpHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input))
		
	def handle(self, handler_input):
		speech = "You can ask me to remember a color or to tell you what your favorite color is"
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response
		
class CancelOrStopHandler(AbstractRequestHandler):

	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input))
		
	def handle(self, handler_input):
		speech = "Goodbye"
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response

sb.add_request_handler(DefaultHandler())
sb.add_request_handler(SetFavoriteColorHandler())
sb.add_request_handler(GetFavoriteColorHandler())
sb.add_request_handler(HelpHandler())
sb.add_request_handler(CancelOrStopHandler())

lambda_handler = sb.lambda_handler()