from era_db import Screen,Prompt,Option,eraDB

# You *must* call prepareReconfig() before defining the workflow
eraDB.prepareReconfig()

s1 = Screen.new()
p1 = Prompt.new()
p1.setText("Please enter the name of the paper being reviewed.")
p1.setType("input")
s1.addPrompt(p1)

p2 = Prompt.new()
p2.setText("Please enter the author's name.")
p2.setType("input")
s1.addPrompt(p2)

p3 = Prompt.new()
p3.setText("Please enter your name.")
p3.setType("input")
s1.addPrompt(p3)

p4 = Prompt.new()
p4.setText("Claims")
p4.setType("textarea")
s1.addPrompt(p4)

p5 = Prompt.new()
p5.setText("Summary")
p5.setType("textarea")
s1.addPrompt(p5)

s2 = Screen.new()

# Relevance

p6 = Prompt.new()
p6.setType("checkbox")
p6.setText("How close is this paper to the call for paper's core coverage?")
p6o1 = Option.new()
p6o1.setText("This paper is solely about an element in the core coverage")
p6o2 = Option.new()
p6o2.setText("This paper is mainly about one of the elements in the core coverage")
p6o3 = Option.new()
p6o3.setText("This paper is only tangentally related to the call for papers")
p6o4 = Option.new()
p6o4.setText("This paper doesn't discuss any of the element in the call for paper's coverage")
p6.addOptions([p6o1,p6o2,p6o3,p6o4])
s2.addPrompt(p6)

# Originality

s3 = Screen.new()

p7 = Prompt.new()
p7.setType("checkbox")
p7.setText("Has this paper already been published?")
p7o1 = Option.new()
p7o1.setText("Yes Verbatim")
p7o2 = Option.new()
p7o2.setText("A previous version of this paper has been published before")
p7o3 = Option.new()
p7o3.setText("This is an update of a previously published paper")
p7o4 = Option.new()
p7o4.setText("Not to my knowledge")
p7.addOptions([p7o1,p7o2,p7o3,p7o4])

s3.addPrompt(p7)

# Presentation

s4 = Screen.new()

p8 = Prompt.new()
p8.setType("checkbox")
p8.setText("How well organised is this paper?")
p8o1 = Option.new()
p8o1.setText("Excellent")
p8o2 = Option.new()
p8o2.setText("Good")
p8o3 = Option.new()
p8o3.setText("Average")
p8o4 = Option.new()
p8o4.setText("Poor")
p8o5 = Option.new()
p8o5.setText("I'm not sure")
p8.addOptions([p8o1,p8o2,p8o3,p8o4,p8o5])

s4.addPrompt(p8)

p9 = Prompt.new()
p9.setType("checkbox")
p9.setText("How readable is this paper?")
p9o1 = Option.new()
p9o1.setText("Very Readable")
p9o2 = Option.new()
p9o2.setText("Quite Readble")
p9o3 = Option.new()
p9o3.setText("Not Very Readable")
p9o4 = Option.new()
p9o4.setText("Totally Un-Readable")
p9o5 = Option.new()
p9o5.setText("I'm not sure")

p9.addOptions([p9o1,p9o2,p9o3,p9o4,p9o5])

s4.addPrompt(p9)

p10 = Prompt.new()
p10.setType("checkbox")
p10.setText("How complete and thorough is the bibliography?")
p10o1 = Option.new()
p10o1.setText("Very Thorough")
p10o2 = Option.new()
p10o2.setText("Quite Thorough")
p10o3 = Option.new()
p10o3.setText("Average")
p10o4 = Option.new()
p10o4.setText("Not Very Thorough Un-Readable")
p10o5 = Option.new()
p10o5.setText("There were no references at all")

p10.addOptions([p10o1,p10o2,p10o3,p10o4,p10o5])

s4.addPrompt(p10)

# This call needs to be here, to commit changes to the database
eraDB.save()