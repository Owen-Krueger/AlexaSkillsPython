from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

SKILL_NAME = "Favorite Color"

sb = SkillBuilder()

class FavoriteColorHandler(AbstractRequestHandler):

	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input)
		
	def handle(self, handler_input):
		speech = "Hi"
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response

class HelpHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input)
		
	def handle(self, handler_input):
		speech = "Hi"
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response
		
class CancelOrStopHandler(AbstractRequestHandler):

	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input)
		
	def handle(self, handler_input):
		speech = "Hi"
		
		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response

sb.add_request_handler(FavoriteColorHandler())
sb.add_request_handler(HelpHandler())
sb.add_request_handler(CancelOrStopHandler())

lambda_handler = sb.lambda_handler()