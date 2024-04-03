# Question-answer-agent

* This repo allows two agents to talk to each other in the terminal including mp3 readout.
* The Hayden agent is the student and Nate agent is the teacher.
* Hayden will ask a question to the teacher and the teacher provide an answer 

### Setup
  * Add ```OPENAI_API_KEY= to .env file```
  * install dependencies and run ```$ python3 app.py``` in the terminal

### Additional options
  * Adjust the provided ```nate.txt``` and ```hayden.txt``` files with your own prmpts, or just change the subject.
  * Adjust the turns to control the number of questions
  * Copy paste the question/answer printout to the hayden_additional.txt to avoid duplicate questions.
