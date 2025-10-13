#`Flask` is a web framework. It provides tools, libraries, and technologies that allow you to build a web application. `request` is used to get the data from the user. `jsonify` is used to return the response in JSON format.
#`Cross-Origin Resource Sharing` is a mechanism that uses additional HTTP headers to tell browsers to give a web application running at one origin, access to selected resources from a different origin.
#importing all the functions from the controller file.
#`__name__` is a special variable in Python that is used to determine whether a script is being run as the main program or it is being imported as a module.
#`Cross-Origin Resource Sharing` is a mechanism that uses additional HTTP headers to tell browsers to give a web application running at one origin, access to selected resources from a different origin.
from flask import Flask, request, jsonify 
from flask_cors import CORS 
from middleware import * 
from connectAPI import *
app = Flask(__name__) 
CORS(app)

@app.route('/chatbot/query', methods=['POST'])
def chatbot():
    try:
        data = request.get_json() 
        response = valiateQuery(data)
        return {
            "data":response,
            "statusCode":200
        },200
    except Exception as e:
        print(f"Error in chatbot Route: {str(e)}")
        return jsonify({
                "Error":str(e),
                "statusCode":500
            }),400

# This is the main function in which the application runs.
if __name__ == "__main__":
    app.run(debug=True , port="8080",host="0.0.0.0")