from google.appengine.ext import db

class ERA_DB(object):
    def __init__(self):
        self.screens = []
    def prepareReconfig(self):
        # Set all previous screens to inactive
        screens = Screen.all()
        # screens.filter('active =', True)
        all_screens = screens.fetch(1000)
        
        for screen in all_screens:
            screen.active = False
            screen.put()
    def save(self):
        for objIdx in range(len(self.screens)):
            # Screen numbers start at 1, so idx+1
            self.screens[objIdx].nth = objIdx+1
            self.screens[objIdx].save()

eraDB = ERA_DB()

#TODO: find the proper way to override init
class Screen(db.Model):
    active = db.BooleanProperty(True)
    nth = db.IntegerProperty()

    @classmethod
    def new(cls):
        newInst = cls()
        
        eraDB.screens.append(newInst)

        newInst.active = True
        newInst.put()

        newInst.prompts = []
        
        return newInst
    def addPrompt(self,prompt):
        prompt.screen = self
        self.prompts.append(prompt)
    def save(self):
        self.put()
        for prompt in self.prompts:
            prompt.save()
    @classmethod
    def getNthActiveScreen(cls,nth):
        screens = cls.all()
        screens.filter('active =',True)
        screens.filter('nth =',nth)
        return screens.get()

class Prompt(db.Model):
    screen = db.ReferenceProperty(Screen)
    
    promptText = db.StringProperty("Prompt text goes here.")
    promptType = db.StringProperty("input")
    
    onlyFlags = db.ListProperty(str)
    unlessFlags = db.ListProperty(str)

    @classmethod
    def new(cls):
        newInst = cls()
        newInst.put()
        newInst.options = []
        return newInst
    def setText(self,text):
        self.promptText = text
    def setType(self,promptType):
        if promptType not in ['textarea','checkbox','select','input']:
            # Invalid type!
            return False
        self.promptType = promptType
    def setOnlyFlags(self,flags):
        self.onlyFlags = flags
    def setUnlessFlags(self,flags):
        self.unlessFlags = flags
    def addOptions(self,options):
        self.put()
        for opt in options:
            opt.prompt = self.key()
            self.options.append(opt)
    def save(self):
        self.put()
        for opt in self.options:
            opt.save()
    def shouldShowPrompt(self,flags):
        for flag in flags:
            if flag in self.unlessFlags:
                return False
            if len(self.onlyFlags) > 0 and flag not in self.onlyFlags:
                return False
        return True
    def getOptions(self):
        opt = Option.all()
        opt.filter('prompt =',self)
        return opt.fetch(1000)
    
class Option(db.Model):
    text = db.StringProperty("Option text goes here.")
    flagsSet = db.ListProperty(str)
    
    prompt = db.ReferenceProperty(Prompt)

    @classmethod
    def new(cls):
        newInst = cls()
        newInst.put()
        return newInst
    def setsFlag(self,flag):
        self.flagsSet.append(flag)
    def setText(self,text):
        self.text = text
    def save(self):
        self.put()