#!/usr/bin/env python

from era_db import Prompt,Screen,Option

from google.appengine.api import users
from google.appengine.ext import db

from google.appengine.ext.webapp import util

import tornado.web
import tornado.wsgi
import unicodedata
import wsgiref.handlers

class BadReviewIDException(Exception):
    def __init__(self,reviewID):
        self.reviewID = reviewID
    def __str__(self):
        return "Bad review ID: %s" % self.reviewID

# Throw this error when the user submits a form missing
# data for one of the prompts expected.
class BadPOSTIDException(Exception):
    def __init__(self,postID):
        self.postID = postID
    def __str__(self):
        return "Bad POST ID: %s" % self.postID

class Review(db.Model):
    created = db.DateTimeProperty()
    
    # That way, if a user undoes their answer for a given prompt 
    # that sets a flag, we can keep track of any other prompts
    # that may have also set that flag, and not wrongly unset it.

    flagsSet = db.ListProperty(str)
    
    @classmethod
    def getFlagsByID(reviewID):
        reviewObj = Review.get_by_id(reviewID)
        if reviewObj is None:
            raise BadReviewIDException(reviewID)
        return reviewObj.flagsSet
    def getSetFlagNames(self):
        return map(lambda x: x[1],self.flagsSet)
    def getPromptsToShow(self,screen):
        p = Prompt.all()
        p.filter("screen =",screen)
        p = p.fetch(1000)
        
        prompts = [prompt for prompt in p if prompt.shouldShowPrompt(self.getSetFlagNames())]
        
        return prompts
    # Notice that this method does not call self.put()
    def unsetFlagsByPrompt(self,prompt):
        for x in self.flagsSet:
            promptID = prompt.key().id()
            if x[0] == promptID:
                self.flagsSet.remove(promptID)                
    def unsetFlagForPromptOption(self,option,flag):
        flagTuple = [option,prompt.key().id(),option.key().id(),flag]
        if flagTuple in self.flagsSet:
            self.flagsSet.remove(flagTuple)
    def setFlagForPromptOption(self,option,flag):
        flagTuple = [option.prompt.key().id(),option.key().id(),flag]
        if flagTuple not in self.flagsSet:
            self.flagsSet.append(flagTuple)

# Flags set is a list of lists, of the form
# (<promptID>,<optionID>,flagName)
class SetFlag(db.Model):
    review = db.ReferenceProperty(Review)
    prompt = db.ReferenceProperty(Prompt)
    flagname = db.StringProperty()

class PromptResponse(db.Model):
    created = db.DateTimeProperty()
    review = db.ReferenceProperty(Review)
    prompt = db.ReferenceProperty(Prompt)
    
    # 'option' field is optional, right now, it's only used for checkboxes.
    option = db.ReferenceProperty(Option)
    optionValue = db.BooleanProperty(False)
    
    text = db.StringProperty()
    
    def assignValue(self,value,prompt,option=None):
        if prompt is None:
            # Must be an option
            self.option = option
            self.optionValue = value
        else:
            self.prompt = prompt
            if prompt.promptType == 'textarea' or prompt.promptType == 'input':
                self.text = value
        self.put()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render("templates/index.html")
        
class NewReviewHandler(tornado.web.RequestHandler):
    def get(self):
        newReview = Review()
        newReview.put()

        return self.render("templates/new.html",url="http://" + self.request.host,review=newReview)

class ScreenHandler(tornado.web.RequestHandler):
    def get(self,reviewID,nthScreen):
        #TODO: redirect to next screen if there are no prompts to show for this one
        return self.renderOrRedirectNextScreen(reviewID,nthScreen)
    
    # Handles form response
    def post(self,reviewID,nthScreen):        
        review = Review.get_by_id(int(reviewID))
        
        # First, unset all option flags for the prompt, and then
        # reset them as needed as we look at the options.

        # Only call review.put() at the end, so we only write
        # the flags to the DB once.
        
        # Look for the prompts in the POST args, their arg name is just the prompt.key().id()
        for promptID in self.request.arguments.get('prompts[]'):
            prompt = Prompt.get_by_id(int(promptID))
            review.unsetFlagsByPrompt(prompt)
            
            # If a promptID isn't present in POST args, its options must be.
            
            if promptID in self.request.arguments:
                # Look for an entity in the DB with the keyName promptID_reviewID.
                # Or, create one if it doesn't already exist

                response = PromptResponse.get_or_insert("%s_%s" % (promptID,reviewID))
                response.assignValue(self.request.arguments[promptID][0],prompt)

        for optionID in self.request.arguments:
            # Special postvar that holds prompt IDs, already used it
            if optionID == 'prompts[]': continue

            if optionID[:6] == 'option':
                optionValue = self.request.arguments[optionID][0] == 'on'
                
                option = Option.get_by_id(int(optionID[6:]))
                response.assignValue(optionValue,None,option)
                
                for flag in option.flagsSet:
                    review.setFlagForPromptOption(option,flag)

        review.put()

        return self.renderOrRedirectNextScreen(reviewID,nthScreen)
    @classmethod
    def getPromptsForNthScreen(cls,reviewID,nthScreen):
        return Review.get_by_id(long(reviewID)).getPromptsToShow(Screen.getNthActiveScreen(long(nthScreen)))
    def renderOrRedirectNextScreen(self,reviewID,nthScreen):
        promptsObj = ScreenHandler.getPromptsForNthScreen(reviewID,nthScreen)

        return self.render("templates/screen.html",prompts=promptsObj,reviewID=long(reviewID),nthScreen=long(nthScreen))

class ReviewRedirectHandler(tornado.web.RequestHandler):
    def get(self,reviewID):
        self.redirect("/review/%s/screen/1" % reviewID)

settings = {

}
application = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/new/?", NewReviewHandler),
    
    (r"/review/([0-9]+)/screen/([0-9]+)/?", ScreenHandler),
    (r"/review/([0-9]+)/?", ReviewRedirectHandler),
    
], **settings)

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()