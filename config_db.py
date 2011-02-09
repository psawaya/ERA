from era_db import Screen,Prompt,Option,eraDB

# You *must* call prepareReconfig() before defining the workflow
eraDB.prepareReconfig()

s1 = Screen.new()
p1 = Prompt.new()
p1.setText("Which keywords are relevant to this paper?")
p1.setType("checkbox")
p1o1 = Option.new() 
p1o1.setText("Computer Science") 
p1o1.setsFlag("cs")
p1o2 = Option.new() 
p1o2.setText("Mathematics") 
p1o2.setsFlag("math")
p1o3 = Option.new() 
p1o3.setText("Cognitive Science") 
p1o3.setsFlag("cogsci")
p1.addOptions([p1o1,p1o2,p1o3]) 

test1 = Prompt.new()
test1.setType('textarea')
test1.setText('This is a textarea prompt.')

test2 = Prompt.new()
test2.setType('input')
test2.setText('This is a text input prompt.')

s1.addPrompt(p1)
s1.addPrompt(test1)
s1.addPrompt(test2)
s2 = Screen.new()
p2 = Prompt.new()
p2.setText("Which theorems were proven?")
p2.setType("textarea")
p2.setOnlyFlags(["math"])
p3 = Prompt.new()
p3.setText("Which programming languages were used?")
p3.setType("textarea")
p3.setUnlessFlags(["math"])
s2.addPrompt(p2)
s2.addPrompt(p3)

    # This call needs to be here, to commit changes to the database
eraDB.save()