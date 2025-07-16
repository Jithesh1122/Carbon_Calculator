class CarbonFootprintChatbot:
    def __init__(self):
        self.responses = {
            "carbon footprint": "Carbon footprint measures your environmental impact. Try reducing waste and using public transport!",
            "reduce emissions": "You can reduce emissions by using renewable energy, reducing waste, and traveling efficiently."
        }

    def get_response(self, message):
        for key, response in self.responses.items():
            if key in message.lower():
                return response
        return "I'm here to help! Try asking about 'carbon footprint' or 'reduce emissions'."
