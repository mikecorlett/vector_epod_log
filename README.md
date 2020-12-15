# vector_epod_log
Testing the escape pod; capture results to CSV

The user is prompted to speak commands Vector from a list in a file.

The script then 'tails' a logfile and captures log output, searching for 'incoming_text' lines and decoding the JSON.

For each detected response, the user is prompted to pass/fail the outcome and decide to retyr or go to the next command
