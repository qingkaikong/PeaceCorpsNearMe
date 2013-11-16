from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def phone_msg():
    """Respond and get the SMS from the phone"""	
    if request.method == "POST":
		from_number = request.values.get('From', None)
		resp = twilio.twiml.Response()
		resp.message(message)
		print 'We have one phone sending SMS to us'
		return str(resp)
    return

if __name__ == "__main__":
    app.run(debug=True)
