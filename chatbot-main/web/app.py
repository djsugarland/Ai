from flask import Flask, request, jsonify
import os.path
from AI import AI

app = Flask(__name__, static_folder='public/static')

@app.route("/")
def index():
    return app.send_static_file('bot.html')

#Basic Example
@app.route('/api/v1/docs', methods=['POST'])
def process_json():
   content_type = request.headers.get('Content-Type')
   print(content_type)
   if (content_type == 'application/json;'):
       json = request.get_json()
       ai = AI()
       #return ai.getOpenAIBasicResponse(json['query'])
       return ai.getOpenAIBasicResponse(json['query'])
   else:
       return 'Content-Type not supported!'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)