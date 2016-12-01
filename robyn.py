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
<!DOCTYPE html>
<html>
<head>
    <title>Robyn - Your Friend for Health!</title>
    <link href="https://fonts.googleapis.com/css?family=Pacifico" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Ubuntu" rel="stylesheet">   

    <style type="text/css">
        body, html{{
            margin:0;
        padding:0;
        }}
    </style>
</head>
<body bgcolor="#CCD1D9">
    <div style="width: 100%; height: 6em; background: #212121;">
        <p style="font-family: 'Pacifico', cursive; color: white; font-size: 3em; margin: 0; padding-left: 1em;">Robyn: Your Friend for Medical Health!</p>
    </div>

    <div style="margin-left: auto; margin-right: auto; width: 90%; height: 27em; background: #669999; margin-bottom: 2em; border-radius: 6px;">
        <h3 style="margin-left: 1em; padding-top: 0.5em; font-family: 'Ubuntu', sans-serif;">Conversation</h3>
        <div style="width: 98%; margin-left: auto; margin-right: auto; height: 23em; background: white; overflow: auto;">
            <p>

            </p>
        </div>
    </div>

    <form style="text-align: center" action="/" method="post">
                <input id="text-box" style="width:80%; height: 5em; border-radius: 6px" name="user_input" type="float" />
                <input style="height: 3em; width: 4em; margin-left: 2em; border-radius: 6px; font-size: 1em; background: #48CFAD; font-family: 'Ubuntu', sans-serif;
" value="Enter" type="submit" />
    </form>

    <script type="text/javascript">
    window.onload = function(){{
    var text_input = document.getElementById ('text-box');
    text_input.focus ();
    text_input.select ();
    }}
    </script>
</body>
</html>    

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
<!DOCTYPE html>
<html>
<head>
    <title>Robyn - Your Friend for Health!</title>
    <link href="https://fonts.googleapis.com/css?family=Pacifico" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Ubuntu" rel="stylesheet">   

    <style type="text/css">
        body, html{{
            margin:0;
        padding:0;
        }}
    </style>
</head>
<body bgcolor="#CCD1D9">
    <div style="width: 100%; height: 6em; background: #212121;">
        <p style="font-family: 'Pacifico', cursive; color: white; font-size: 3em; margin: 0; padding-left: 1em;">Robyn: Your Friend for Medical Health!</p>
    </div>

    <div style="margin-left: auto; margin-right: auto; width: 90%; height: 27em; background: #669999; margin-bottom: 2em; border-radius: 6px;">
        <h3 style="margin-left: 1em; padding-top: 0.5em; font-family: 'Ubuntu', sans-serif;">Conversation</h3>
        <div style="width: 98%; margin-left: auto; margin-right: auto; height: 23em; background: white; overflow: auto;">
            <p>
            {0}
            </p>
        </div>
    </div>

    <form style="text-align: center" action="/" method="post">
                <input id="text-box" style="width:80%; height: 5em; border-radius: 6px" name="user_input" type="float" />
                <input style="height: 3em; width: 4em; margin-left: 2em; border-radius: 6px; font-size: 1em; background: #48CFAD; font-family: 'Ubuntu', sans-serif;
" value="Enter" type="submit" />
    </form>

    <script type="text/javascript">
    window.onload = function(){{
    var text_input = document.getElementById ('text-box');
    text_input.focus ();
    text_input.select ();
    }}
    </script>
</body>
</html>    
    '''.format(conversation)

run(host='localhost', port=8080, debug=True)