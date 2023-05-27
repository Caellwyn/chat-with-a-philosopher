import openai

   
class AIAgent():
    def __init__(self, model="gpt-3.5-turbo"):
        self.model=model
        self.system_message = """Choose the 
        philosopher most appropriate to respond to each
        query and introduce yourself as that philosopher.  
        Then respond to the prompt as if you were that philosopher."""
        self.history = [{'role':'system', 'content':self.system_message}]
        
    def add_message(self, text, role):
        message = {'role':role, 'content':text}
        self.history.append(message)
        
    def query(self, prompt, temperature=.1):
        # Add user prompt to history
        self.add_message(prompt, 'user')

        # Query the model through the API 
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history,
            temperature=temperature, # this is the degree of randomness of the model's output
        )
        reply = response.choices[0].message["content"]

        # Add reply to message history
        self.add_message(reply, 'assistant')
        
        # Save usage report
        usage = response['usage']
        

        # Calculate cost of query
        if self.model.startswith("gpt-3.5"):
            cost = (.002 * usage['total_tokens']) / 1000
        elif self.model == "gpt-4":
            cost = (usage['prompt_tokens'] * .03 + usage['completion_tokens'] * .06) / 1000
        else:
            cost = 'unknown'
            
       
        return {'content':reply, 'usage':usage, 'cost':cost}
    
    def clear_history(self):
        self.history = [{'role':'system', 'content':self.system_message}]
        
    def get_history(self):
        return self.history