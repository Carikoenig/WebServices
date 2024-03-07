# WebServices
third project of "AI and the Web".
How to start it:
    clone the repo 
    open cmd:
    make a virtual environment and install the requiremnts with 'pip install -r requirements.txt'
        'python hub.py'
    open 2 new cmd for each channel to start and register the channels:
        'python channel.py'
        'flask –app channel.py register'
        'python channel1.py'
        'flask –app channel1.py register'
        'python channel2.py'
        'flask –app channel.py register'
    open another cmd:
        'python client.py'

#### Code organization
- hub.py – The hub code. No need to modify this. Run with
    > python hub.py
Runs on localhost, port 5555

- channel.py – The starter code for a channel. Run with
   > python channel.py
After that, register your channel (in a separate terminal) with
   > flask –app channel.py register
   
- client.py – The client application. Run with
   > python client.py
Open displayed URL in browser


### Project 3: Web Services

Work on the following two tasks for the distributed message board environment presented in the seminar:

Code: https://studip.uni-osnabrueck.de/sendfile.php?type=0&file_id=a1bc74c9b9384a9cb05c5f1e32bffaed&file_name=distributed_messageboard.zip

HINT: It's very easy to fulfill the minimum requirements. Contributions that fulfill only the minimum requirements can still get 90% of the points. (10% are for creative solutions)

 

1. Build an interesting channel for the distributed message board:

    Implement some chatbot for your channel, i.e. messages will not only be provided by users but also generated automatically
    It's totally up to you to come up with some interesting ideas
    Possible Examples:
        Guessing games
        ELIZA style chatbot
        Calculation bot - try to interpret input as a calculation task
        Service bot - provide some kind of statistics about the input


2. Make a fancier client

    The standard client is very simplistic. Make it fancier, somehow.


3. Deploy your channel and your client on the known servers.
    Register your channel with the central hub.
    Play around with other groups' channels.
