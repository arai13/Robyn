import aiml
import sqlite3
from bottle import get, post, run, request

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()
db = sqlite3.connect('db/diseases.db')

cursor = db.cursor()

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn("std-startup.xml")

# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
k.respond("load aiml b")

@get('/')
def ask():
    return '''
        <form action="/" method="post">
                <input name="user_input" type="float" />
                <input value="Enter" type="submit" />
        </form>
    '''

conversation = ""

@post('/')
def robyn_responds():
    user_input = request.forms.get('user_input')

    response = k.respond(user_input)
    if response[0] == '!':
        response = response[1:]
        cursor.execute(response)
        temp = cursor.fetchone()
        response = temp[0]
    
    global conversation
    current_user_conv = "<b>You: </b>" + user_input
    current_robyn_conv = "<b>Robyn: </b>" + response 
    conversation = conversation + current_user_conv + "<br>" + current_robyn_conv + "<br>"

    return '''
        <p>%s</p>

        <form action="/" method="post">
                <input name="user_input" type="float" />
                <input value="Enter" type="submit" />
        </form>
    ''' % (conversation)

run(host='localhost', port=8080, debug=True)