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

from random import randint


SKILL_NAME = "Dice Coin Coins"

sb = SkillBuilder()
# logger = logging.getLogger(_name_)
# logger.setLevel(logging.DEBUG)

class DefaultHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return(is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("AMAZON.HelpIntent")(handler_input))
        
    def handle(self, handler_input):
        logging.info("Starting Default")
        speech = "You can ask me to roll a dice or flip a coin"
        
        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech)).ask(speech)
        return handler_input.response_builder.response

class RollDiceHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return(is_request_type("RollADice")(handler_input) or
                is_intent_name("RollADice")(handler_input))
        
    def handle(self, handler_input):
        dice = randint(1,6)
        
        speech = "Dice number is " + str(dice)
        
        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response
        
class FlipCoinHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return(is_request_type("FlipACoin")(handler_input) or
                is_intent_name("FlipACoin")(handler_input))
        
    def handle(self, handler_input):
        coin = randint(0,1)
        if coin == 0:
            speech = "Coin Flip is Heads"
        else:
            speech = "Coin Flip is Tails"
        
        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response

sb.add_request_handler(DefaultHandler())
sb.add_request_handler(RollDiceHandler())
sb.add_request_handler(FlipCoinHandler())

lambda_handler = sb.lambda_handler()