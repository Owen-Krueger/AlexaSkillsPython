import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import ui
from ask_sdk_model import Response

import boto3
from boto3 import resource

import requests

SKILL_NAME = "Recipe"

sb = SkillBuilder()
logger = logging.getLogger()

apiStart = "https://api.edamam.com/search?"
apiEnd = "&app_id=c1afdbf8&app_key=7f60627b97806fb6216e832af1204ff6"


class DefaultHandler(AbstractRequestHandler):

	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input))
		
	def handle(self, handler_input):
		speech = "You can ask me to tell you a food recipe!"
		
		print("Starting check screen")
		print("Has screen: " + str(RecipeHelper.checkScreen(handler_input)))
		print("Finished check screen")
		handler_input.response_builder.speak(speech).set_card(
			ui.SimpleCard(SKILL_NAME, speech)).set_should_end_session(False)
		return handler_input.response_builder.response
		
class RecipeHelper():
	def getJsonFromAPI(apiStart, paramsList):
		r = requests.get(apiStart, params=paramsList)
		return(r.json())
	
	def getRecipe(data, index):
		return(data['hits'][index]['recipe'])
	
	def checkScreen(handler_input):
		print("In check Screen")
		if handler_input.request_envelope.context.system.device.supported_interfaces.display is None:
			return False
		else:
			return True
			
	def getIngredients(data, index):
		return(RecipeHelper.getRecipe(data, index)['ingredientLines'])
				
class TellRecipe(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("TellRecipe")(handler_input))
		
	def handle(self, handler_input):
		slots = handler_input.request_envelope.request.intent.slots
	
		if 'Food' in slots:
			recipe = slots['Food'].value
			
			if recipe is not None:
		
				handler_input.attributes_manager.session_attributes['recipe'] = recipe;
				
				paramsList = {'q': recipe, 'app_id' : 'c1afdbf8', 'app_key' : '7f60627b97806fb6216e832af1204ff6'}
				
				data = RecipeHelper.getJsonFromAPI(apiStart, paramsList)

				handler_input.attributes_manager.session_attributes['recipeNumber'] = 0

				recipeFromHelper = RecipeHelper.getRecipe(data,0)

				label = recipeFromHelper['label']
				source = recipeFromHelper['source']
				
				speech = "Here's a recipe for " + label + " from " + source
				speechText = ("Recipe: " + label + "\nFrom: " + source + 
				"\n\nIngredients: " + str(RecipeHelper.getIngredients(data, 0))[1:-1] + 
				"\n\n URL: " + recipeFromHelper['url'])
				
				handler_input.response_builder.speak(speech).set_card(
					ui.StandardCard(
					title=label,
					text = speechText,
					image = ui.Image(
						small_image_url= recipeFromHelper['image'],
						large_image_url= recipeFromHelper['image']
					)
				)
				).set_should_end_session(False)
				
			else:
				speech = "Sorry, we had an issue"
				handler_input.response_builder.speak(speech).set_card(
					SimpleCard(SKILL_NAME, speech)).set_should_end_session(False)
				#.ask(reprompt)
		return handler_input.response_builder.response
		
class NextRecipe(AbstractRequestHandler):
	def can_handle(self, handler_input):
		return(is_intent_name("NextRecipe")(handler_input))
		
	def handle(self, handler_input):
		if 'recipe' in handler_input.attributes_manager.session_attributes:
			recipe = handler_input.attributes_manager.session_attributes['recipe']
		else:
			recipe = None
		
		if recipe is not None:
			paramsList = {'q': recipe, 'app_id' : 'c1afdbf8', 'app_key' : '7f60627b97806fb6216e832af1204ff6'}
			
			data = RecipeHelper.getJsonFromAPI(apiStart, paramsList)
			
			recipeNumber = handler_input.attributes_manager.session_attributes['recipeNumber'] + 1

			handler_input.attributes_manager.session_attributes['recipeNumber'] = recipeNumber
			
			recipeFromHelper = RecipeHelper.getRecipe(data,recipeNumber)
			
			label = recipeFromHelper['label']
			source = recipeFromHelper['source']
			
			speech = "Here's a recipe for " + label + " from " + source
			speechText = ("Recipe: " + label + "\nFrom: " + source + 
				"\n\nIngredients: " + str(RecipeHelper.getIngredients(data, 0))[1:-1] + 
				"\n\n URL: " + recipeFromHelper['url'])
				
			handler_input.response_builder.speak(speech).set_card(
			ui.StandardCard(
				title=SKILL_NAME,
				text = speechText,
				image = ui.Image(
					small_image_url= recipeFromHelper['image'],
					large_image_url= recipeFromHelper['image']
				)
			)
		).set_should_end_session(False)
			
		else:
			speech = "Sorry, you haven't requested a recipe yet. Please request a recipe to continue"
			
			handler_input.response_builder.speak(speech).set_card(
				ui.SimpleCard(SKILL_NAME, speech)
			).set_should_end_session(False)
		return handler_input.response_builder.response
		
class HelpHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("AMAZON.HelpRequest")(handler_input))
		
	def handle(self, handler_input):
		speech = "You can ask me to tell you a food recipe"
		
		handler_input.response_builder.speak(speech).set_card(
			ui.SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response
		
class CancelOrStopHandler(AbstractRequestHandler):

	def can_handle(self, handler_input):
		return(is_intent_name("AMAZON.StopIntent")(handler_input))
		
	def handle(self, handler_input):
		speech = "Goodbye"
		
		handler_input.response_builder.speak(speech).set_card(
			ui.SimpleCard(SKILL_NAME, speech)).set_should_end_session(True)
		return handler_input.response_builder.response

sb.add_request_handler(DefaultHandler())
sb.add_request_handler(TellRecipe())
sb.add_request_handler(NextRecipe())
sb.add_request_handler(HelpHandler())
sb.add_request_handler(CancelOrStopHandler())

lambda_handler = sb.lambda_handler()