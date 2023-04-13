# ActivityViewer

View your Wii U activity stats on PC!

## Usage

**NOTICE: If you're using the Aroma FTPiiU plugin, make sure that "Allow access to system files" is set to `True`.**

Make sure you have Python 3.10 or later installed, then run `pip3 install -r requirements.txt` to install all required packages.

1. Turn on your Wii U (has to be modded) and launch your desired FTP client (FTPiiU_everywhere or Aroma plugin).
2. Run `py log.py` and enter your Wii U IP and account ID.
3. Once the script has finished transferring, run `py app.py` and visit [localhost](http://localhost)
