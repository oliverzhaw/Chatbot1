import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
    As a digital therapy coach, check in daily with your patient to assess their well-being related to their chronic condition.
    Use open-ended questions and empathetic dialogue to create a supportive environment.
    Reflectively listen and encourage elaboration to assess the patient's detailed condition without directing the topic.
"""

my_instance_context = """
    Meet Daniel Müller, 52, who is tackling obesity with a therapy plan that includes morning-to-noon intermittent fasting, 
    thrice-weekly 30-minute swims, and a switch to whole grain bread.
"""

my_instance_starter = """
Jetzt, frage nach dem Namen und einem persönlichen Detail (z.B. Hobby, Beruf, Lebenserfahrung).
Verwende diese im geschlechtsneutralem Gespräch in Du-Form.
Sobald ein Name und persönliches Detail bekannt ist, zeige eine Liste von Optionen.
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="coach",
    user_id="daniel",
    type_name="Health Coach",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

bot.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


#-----------------------------------------------------------

# Define the parameters for the second bot
second_type_role = """
    As a therapy coach for patients with chronic diseases, engage in a conversation with the user about their medication regimen. Encourage the user to ask questions they have about their medication, and provide clear, empathetic answers. Ensure that the user understands the importance of adhering to their medication regimen by explaining the benefits and potential consequences of non-compliance. Offer support and guidance to help the user stay motivated and committed to their treatment plan
"""

second_instance_context = """
    Meet Sarah Johnson, 35, who is seeking guidance to manage her gluten intolerance and improve her overall well-being.
"""

second_instance_starter = """
Craft a welcoming message for the patient, acknowledging their journey with a chronic disease like adiposity. Encourage a friendly tone and express willingness to support them. Invite the user to share their feelings and any specific concerns they may have about managing their condition
"""

# Create a second instance of the Chatbot class
second_bot = Chatbot(
    database_file="database/second_chatbot.db",  # You might want to use a different database file
    type_id="trainer",
    user_id="oliver",
    type_name="Nutritionist",
    type_role=second_type_role,
    instance_context=second_instance_context,
    instance_starter=second_instance_starter
)

# Implement routes for interacting with the second bot
@app.route("/<type_id>/<user_id>/second/chat")
def second_chatbot(type_id: str, user_id: str):
    return render_template("second_chat.html")

# Similar routes for info_retrieve, conversation_retrieve, response_for, reset for the second bot
# Route for retrieving information about the second bot
@app.route("/<type_id>/<user_id>/second/info")
def second_info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/second_chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)

# Route for retrieving conversation history of the second bot
@app.route("/<type_id>/<user_id>/second/conversation")
def second_conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/second_chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)

# Route for receiving user input and getting response from the second bot
@app.route("/<type_id>/<user_id>/second/response_for", methods=["POST"])
def second_response_for(type_id: str, user_id: str):
    user_says = None
    user_says = request.json

    bot: Chatbot = Chatbot(
        database_file="database/second_chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)

# Route for resetting the conversation with the second bot
@app.route("/<type_id>/<user_id>/second/reset", methods=["DELETE"])
def second_reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/second_chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


