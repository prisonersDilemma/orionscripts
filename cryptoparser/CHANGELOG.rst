Tue Oct 24 07:28:14 EDT 2017

#### New in version 0.0.6
* Added pattern option. A string or regex pattern can now be passed as an
  argument. Default is to search for the hash contained in the class method:
  CoinHive.Anonymous(). The string/regex is compiled (as opposed to using
  the re.search function) before any HTTP requests are made, for better
  performance.

* Changed default location of resource and output files. These are now stored
  in the current working directory of the script, rather than on the user's
  desktop.

* Added logging and loglevel option. Control the magnitude of the messages
  printed to stdout by using the loglevel option. This takes...

