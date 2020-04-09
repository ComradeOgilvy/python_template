#!/usr/bin/env python3

import argparse
import os
import configparser
import logging
import time
import subprocess
import sys
from datetime import datetime, timedelta

"""
Helper Function to call an bash command
- calls a shell command and returns the output (utf8 encoded)
- stderr is piped to stdout
- stdin is forbidden
- debug:
  - print start of command
  - print end of command
  - print output of command
"""
def _launch_command(command:list):
    """
    Run the command given. The command has to be simple, not containing any 
    bash elements.

    Raise a ValueError if the command asked is not found.
    :param command: the different parts of the command have to be given as 
    different elements of a list:

    example: "ls -l file.txt" has to be given as: ["ls", "-l", "file.txt"]
    :return:    The output of the command decoded with UTF-8, 
                None if an issue occurred
    """
    try:
        logging.debug('Start subprocess '+'"'+ ' '.join(map(str,command))+'"')
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        logging.debug('Finished subprocess '+'"'+ 
            ' '.join(map(str,command))+'"')
        output = process.stdout.read().decode('UTF-8').rstrip()
        logging.debug('[output] %s', output)
        return output
    except FileNotFoundError as fe:
        logging.exception(
            "The command '{}' could not be found.".format(fe.filename)
        )
        return None
    except subprocess.CalledProcessError as e:
        logging.exception(
            "The subprocess failed with: output = %s, error code = %s" 
            %(e.output, e.returncode)
        )
        return None

"""
Main Logic
- describe main logic here
"""
def _main():

    return 0

"""
Main Initialization
"""
def main(arguments):
    try:
        """
        Initialize configuration
        """
        cfg = configparser.ConfigParser()
        try:
            with args.config as f:
                cfg.read_file(f)
        except IOError as e:
            exit_status = 1
            logging.exception(
                "Cannot open Configuration File: [%s]", str(e)
            )
            raise
        
        """ 
        Initialize the logger
        """
        # try to get log path from config file
        try:
            log_file = cfg.get("logging", "log_file")
        except (configparser.NoSectionError, configparser.NoOptionError):
            log_file = os.getcwd() + '/template.log'
        # Check if we have write access to the log file
        # Otherwise use current working directory
        if not (os.access(log_file, os.W_OK)):
            logging.error(
                "No write access to %s, put log file into current working directory",
                log_file
                )
            log_file = os.getcwd()+'/template.log'
        logging_handler = logging.FileHandler(
            log_file,
            mode="w",
        )
        logging_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
        logging_handler.setFormatter(logging_formatter)
        logging.getLogger().addHandler(logging_handler)
        logging.getLogger().setLevel(logging.INFO)

        """
        Parse the remaining configuration options into a configuration dictionary
        """
        # config = {}
        # try:
        #     config[value] = cfg.get("","")
        # except(configparser.NoSectionError, configparser.NoOptionError) as e:
        #     logging.exception("Could not parse configuration option [%s]", str(e))
        #     raise

        """
        Start counting the time and start application
        """
        t0 = time.monotonic()
        logging.critical(
                "=== START OF APPLICATION AT %s ===",
                datetime.utcnow().isoformat()
            )
        try:
            """
            start main logic
            """
            exit_status = _main()
        except Exception as e:
            exit_status = 3
            logging.exception("Execution failed: %s", str(e))
            raise

    finally:
        """
        Calculate Duration and exit the application
        """
        t1 = time.monotonic()
        duration = t1 - t0
        logging.critical(
            "=== END OF APPLICATION AT %s (%s) ===",
            datetime.utcnow().isoformat(),
            timedelta(seconds=duration),
        )
        sys.exit(exit_status)

"""
Load the CLI parameters
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lorem ipsum dolor sit amet"
    )
    parser.add_argument(
        "-c", "--config",
        default='./config.ini',
        type=argparse.FileType("r"),
        help="Configuration file"
    )
    args = parser.parse_args()
    main(args)
