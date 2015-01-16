'''
Created on Jan 15, 2015
'''

__AUTHOR__ = "Mohammed Hamdy"

import logging
from argparse import ArgumentParser
from time import sleep
from os import walk as traverse_dir
from os import path
from whatsauto.util import (make_registration_request, read_numbers_file, get_text_from_speech,
                            get_token, get_account_id)
from whatsauto.log import WhatsappLogger

def make_registration_requests(numbers_file, wav_dir="/var/spool/asterisk/monitor/", 
                               wav_wait_secs=240, request_sleep=1):
  number_generator = read_numbers_file(numbers_file)
  logger = WhatsappLogger("/root/textvoice")
  for (country_code, phone, id_) in number_generator:
    logger.log(logging.DEBUG, "Registering {}-{}".format(country_code, phone))
    result = make_registration_request(country_code, phone)
    if result["status"] == "sent":
      logger.log(logging.INFO, "Request was successful. Waiting {} seconds".format(wav_wait_secs))
      # wait until wav file is retrieved
      sleep(wav_wait_secs)
      logger.log(logging.DEBUG, "Searching for wav with id : {}".format(id_))
      for (root_dir, fileshere, dirshere) in traverse_dir(wav_dir):
        for file_ in fileshere:
          if id_ in file_:
            logging.info("Found file <{}>".format(file_))
            complete_wav_path = path.join(root_dir, file_)
            regcode = get_text_from_speech(complete_wav_path)
            token = get_token()
            account_id = get_account_id(country_code+phone)
            open("/root/textvoice/success.txt", 'wt').write(country_code+phone + 
                "," + token + "," + account_id + "\n")
            break
        else:
          logging.warn("Couldn't find file with suitable id")
    else: # unsuccessful number
      logging.warn("Request was not successful. status '{}'".format(result["status"]))
      open(path.join("/root/textvoice", result["status"] + ".txt"), "wt").write(country_code+phone)
            
    # sleep between requests
    sleep(request_sleep)
    
if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("-f", "--numbers_file", help="the file that contains numbers to query")
  parser.add_argument("--wav_dir", default="/var/spool/asterisk/monitor/")
  parser.add_argument("--wav_wait", type=int, default=240, help="time to wait for wav files to be downloaded (secs)")
  parser.add_argument("--req_sleep", type=int, default=1, help="time to sleep between whatsapp requests")
  args = parser.parse_args()
  make_registration_requests(args.numbers_file, args.wav_dir, args.wav_wait, args.req_sleep, args.debug)