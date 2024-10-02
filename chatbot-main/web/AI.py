from openai import OpenAI
from functions import Funcs
import json
openaiClient = OpenAI(
  api_key='<put your apikey here>',  # this is also the default, it can be omitted
)

class AI:
        
    def getOpenAIBasicResponse(self, query):
        
        system_prompt = """
                            You are an expert chatbot designed to answer questions about robots. Your knowledge spans:
                            Robot Types: Industrial, service, humanoid, autonomous.
                            Robotics Engineering: Mechanical design, sensors, control systems.
                            AI in Robotics: Machine learning, computer vision, and autonomy.
                            Robot Programming: Common languages (ROS, Python, C++).
                            Applications: Robotics in industries like healthcare, manufacturing, space.
                            Ethics: Impact on jobs, privacy, and safety.
                            Human-Robot Interaction: Assistive and social robots.
                            Provide clear, educational answers for all users, from beginners to experts.
                            Only answer questions pertaining to Robots
                        """
        assistent_prompt = """
                            You are a helpful, knowledgeable assistant specializing in robotics.
                            Answer questions clearly and concisely. with images 
                            Tailor your responses to the user’s knowledge level, 
                            whether they are beginners or experts. 
                            Provide practical examples, offer explanations when needed, and stay focused on robotics-related topics.
                            If the user asks complex or open-ended questions, 
                            break them down into simpler concepts and guide the user toward understanding. 
                            Always be polite, engaging, and supportive in your responses.
                        """
        response = openaiClient.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content":query},
                {"role": "assistant", "content":assistent_prompt},
            ],
            temperature=0
        )
        generated_text = response.choices[0].message.content
        return generated_text

    def getOpenAIFunctionCalling(self, query):
        functions = [
            {
                "name": "get_weather",
                "description": "Get the current weather for a specified city.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The name of the city to get the weather for."
                        }
                    },
                    "required": ["city"],
                },
            }
        ]
        messages = [{"role": "user", "content": query}]

        response = openaiClient.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            #prompt=query,
            functions=functions,
            function_call='auto'
        )

        function_call = response.choices[0].message
        print(function_call)

        if function_call is not None and function_call.function_call is not None and function_call.function_call.name == "get_weather":
            function_args = function_call.function_call.arguments
            function_args = json.loads(function_args)
            city = function_args.get("city")
            weather_info = self.get_weather(city)
            return weather_info
        else:
            return self.getOpenAIBasicResponse(query=query)

    def get_weather(self, city):
        func = Funcs()
        return func.getweather(city)