
from flask import Flask, render_template, request, send_file, flash
from analyzeSlang import *
from pytrends.exceptions import ResponseError

app = Flask(__name__)

analyzedData = None
template = None
socialMediaRender = None
error = None
currentSocialPlatform = None


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/facebook", methods = ["GET", "POST"])  # http://127.0.0.1:5000/
def facebook():
    return socialMedia("socialPlatform.html", "facebook")


@app.route("/discord", methods=["GET", "POST"])
def discord():
    return socialMedia("socialPlatform.html", "discord")

@app.route("/reddit")
def reddit():
    return render_template('socialPlatform.html', False)


@app.route("/instagram", methods = ["GET", "POST"])
def instagram():
    return socialMedia("socialPlatform.html", "instagram")


def renderSocialMediaTemplate(nameHTML, socialPlatform):
        global analyzedData
        global template
        global socialMediaRender
        global names
        global currentSocialPlatform
        global error
        
        currentSocialPlatform = socialPlatform
        try:
            analyzedData = AnalyzeSlang(currentSocialPlatform)
            names = analyzedData.getParticipantNames()
            socialMediaRender = render_template(nameHTML, template = analyzedData.getTemplateSetup(), socialPlatform = socialPlatform, showDownload = True, names=names)
            return socialMediaRender
        except KeyError:
            error = "Please upload a valid JSON file"
            print(error)
            return render_template(nameHTML, template = None, socialPlatform = socialPlatform, error=error)
        except:
            error = "Something went wrong. Please wait 1 minute before uploading another file."
            print(error)
            return render_template(nameHTML, template = None, socialPlatform = socialPlatform, error=error)
        


def socialMedia(nameHTML, socialPlatform):    
    if request.method == "POST" and (request.form.get('fname')):  #When form is submitted (When user press Download button)            
            senderName = request.form.get('fname')
            analyzedData.createCSV(senderName)
            return send_file('messages.csv', mimetype='text/csv', download_name="messages.csv", as_attachment=True)

    elif request.method == "POST":
        # try:
        if socialPlatform == "facebook":
            return renderSocialMediaTemplate(nameHTML, "facebook")
        
        if socialPlatform == "instagram":
            return renderSocialMediaTemplate(nameHTML, "instagram")

        if socialPlatform == "discord":
            return renderSocialMediaTemplate(nameHTML, "discord")

        # except:
        #     return render_template(nameHTML, template = None, socialPlatform = socialPlatform, error=True)

    elif socialMediaRender and currentSocialPlatform == socialPlatform:
        return socialMediaRender

    return render_template(nameHTML, template = None, socialPlatform = socialPlatform, error=error)


if __name__ == "__main__":
    app.run(debug=True)