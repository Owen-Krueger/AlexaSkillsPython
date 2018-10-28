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


SKILL_NAME = "Mummy Facts"
FACT_MESSAGE = "Here's your Mummy Fact: "

facts = [
	'A mummy is a person or animals body that has been preserved after death using a technique called mummification. Ancient Egyptians perfected the art of mummification over centuries. They developed a method for drying and wrapping a body in linen strips that made it last for thousands of years',
	'Egyptians started making mummies around 3400BC.',
	'In 2600BC ancient Egyptians finally figured out that if they removed the bodys internal organs before wrapping a person up, their body would last instead of rot.',
	'Egyptians dried the bodies out completely for 40 days before wrapping!',
	'The Egyptians were not the first to make mummies. People in South America did it first',
	'In ancient Egyptian mummification, onions were sometimes used to fill body cavities, often serving as false eyes',
	'Egyptians used vast amounts of linen to mummify a body. The linen on one mummy from the 11th dynasty measured 9,095 feet (845 square meters), which is enough linen to cover three tennis courts',
	'King Ramses II is the first mummy to receive a passport. His passport lists his occupation as "king.',
	'During mummification in ancient Egypt, internal organs were removed through a long incision on the left side of the body. The priest who made the incision was known as the slicer or ripper up',
	'According to Egyptian lore, the god Osiris was the very first mummy',
	'The most popular mummy in the world is most likely Vladimir Lenin. Millions of visitors to Moscow have visited his mummy',
	'The oldest well-preserved mummy in Europe is the "Iceman," who was preserved in a glacier in the Alps for over 5,300 years',
	'Tutankhamun is the only royal mummy discovered with all of its priceless treasures intact',
	'The difference between a mummy and a skeleton is that a mummy still has some of its soft tissue, such as hair, muscle, or skin',
	'Over one million mummies have been found in Egypt, mostly of cats',
	'Egyptians saw mummification as an important step in attaining a happy afterlife',
]

sb = SkillBuilder()

class MummyFactHandler(AbstractRequestHandler):
    
	def can_handle(self, handler_input):
		return(is_request_type("LaunchRequest")(handler_input) or
				is_intent_name("NewMummyFacts")(handler_input))
        
	def handle(self, handler_input):
		logging.info("Starting Default")

		mummy_fact = random.choice(facts)
		speech = FACT_MESSAGE + mummy_fact

		handler_input.response_builder.speak(speech).set_card(
			SimpleCard(SKILL_NAME, speech))
		return handler_input.response_builder.response

class HelpHandler(AbstractRequestHandler):
	
	def can_handle(self, handler_input):
		return(is_intent_name("AMAZON.HelpIntent")(handler_input))
		
	def handle(self, handler_input):
		speech = "You can ask me for a Mummy fact!"
		
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
		
sb.add_request_handler(MummyFactHandler())
sb.add_request_handler(HelpHandler())
sb.add_request_handler(CancelOrStopHandler())

lambda_handler = sb.lambda_handler()