# Parsivel 2 Disdrometer datalogger (parsivel2_datalogger)

Provides a reliable and simple datalogger for the parsivel 2 disdrometer.

### Dependencies
- pyserial


### Install
`git clone git@github.com:ackermannluis/parsivel2_datalogger.git`

To install in your home directory, use:

`python setup.py install --user`

### Linux
you will need to run (on terminal) the following command to allow python access 
to the serial port

`sudo usermod -a -G tty YOUR_USER_NAME`

### Use
- just run on the terminal by navegating to the source folder and running:

`python parsivel_datalogger_main.py`
