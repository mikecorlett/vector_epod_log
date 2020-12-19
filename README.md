# vector_epod_log
Testing the escape pod; capture results to CSV

* The user is prompted to speak commands to Vector from a list in a file.
* The script then 'tails' a logfile and captures log output, searching for 'incoming_text' lines and decoding the JSON. The logfile must be created in another process; currently this is a manual procedure.
* For each detected response, the user is prompted to pass/fail the outcome and decide to retry or go to the next command.

To create log file: journalctl -u escape_pod.service -f > testlog.txt

**TODO**
* Spawn process to create logfile from the script
* Allow users to enter commands rather than use a list?
* Play voice files

