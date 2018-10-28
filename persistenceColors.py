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

dynamodb = resource('dynamodb')
table = dynamodb.Table('FavoriteColor')

class DefaultHandler(AbstractRequestHandler):

	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input))
		
	def handle(self, handler_input):
		speech = "Hi"
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response
		
class SetFavoriteColorHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("SetFavoriteColor")(handler_input))
		
	def handle(self, handler_input):
<<<<<<< HEAD
	
		if FavoriteColor_slot in slots:
			favoriteColor = slots[FavoriteColor].value
		
		speech = "Got it. Your favorite color is " + favoriteColor
=======
		slots = handler_input.request_envelope.request.intent.slots
	
		colorTable = table.get_item('Color')
		if 'FavoriteColor' in slots:
			favoriteColor = slots['FavoriteColor'].value
			
			if favoriteColor is not None:
		
				table.put_item(
					Item = {'Color' : favoriteColor})
					
				speech = "Got it. Your favorite color is " + favoriteColor
				
			else:
				speech = "Sorry, we had an issue"
>>>>>>> 25d6f4cbe704f3b1c390a101c939a2ec4d2a92e2
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response
		
class GetFavoriteColorHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("GetFavoriteColor")(handler_input))
		
	def handle(self, handler_input):
		slots = handler_input.request_envelope.request.intent.slots

		#filtering_exp = Key('Color')
		
		speech = ""
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response

class HelpHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input))
		
	def handle(self, handler_input):
		speech = "Hi"
		
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