'''
Created on Jan 15, 2015
'''
from pprint import _id

__AUTHOR__ = "Mohammed Hamdy"

from random import randrange, choice
import codecs
from subprocess import Popen
from tempfile import TemporaryFile
import json
from yowsup.registration import WACodeRequest

def generate_random_phone_numbers():
  """
  Generates random phone numbers with valid country codes infinitely
  """
  # collected from http://www.ipipi.com/help/telephone-country-codes.htm
  country_codes = ['1', 
                  '7', '20', '27', '30', '31', '32', '33', '34', '36', '39', 
                  '40', '41', '43', '44', '45', '46', '47', '48', '49', '51', 
                  '52', '53', '54', '55', '56', '57', '58', '60', '61', '62', 
                  '63', '64', '65', '66', '81', '82', '84', '86', '90', '91', 
                  '92', '93', '94', '95', '98', '212', '213', '216', '218', '220', 
                  '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', 
                  '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', 
                  '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', 
                  '251', '252', '253', '254', '255', '256', '257', '258', '260', '261', 
                  '262', '263', '264', '265', '266', '267', '268', '269', '290', '291', 
                  '297', '298', '299', '350', '351', '352', '353', '354', '355', '356', 
                  '357', '358', '359', '370', '371', '372', '373', '374', '375', '376', 
                  '377', '378', '379', '380', '381', '385', '386', '387', '389', '420', 
                  '421', '423', '500', '501', '502', '503', '504', '505', '506', '507', 
                  '508', '509', '590', '591', '592', '593', '594', '595', '596', '597', 
                  '598', '599', '670', '672', '673', '674', '675', '676', '677', '678', 
                  '679', '680', '681', '682', '683', '684', '685', '686', '687', '688', 
                  '689', '690', '691', '692', '800', '850', '852', '853', '855', '856', 
                  '870', '871', '872', '873', '874', '880', '881', '886', '960', '961', 
                  '962', '963', '964', '965', '966', '967', '968', '970', '971', '972', 
                  '973', '974', '975', '976', '977', '992', '993', '994', '995', '996', 
                  '997', '998']
  while True:
    next_phone_number = randrange(1111111, 9999999999)
    yield (choice(country_codes), str(next_phone_number))
    
def make_registration_request(country_code, phone_number):
  # country_code : str/unicode
  # phone_number : str/unicode
  whatsapp_request = WACodeRequest(country_code, phone_number, method="voice")
  result = whatsapp_request.send()
  return {key:value for key, value in result.iteritems() if value is not None}

def read_numbers_file(path_numbers):
  # yields country codes, numbers and ids successively from file
  file_numbers = codecs.open(path_numbers, 'r', "utf-8")
  for line in file_numbers:
    if line:
      cc_phone, _id = line.split(',')
      country_code, phone = cc_phone.split('-')
      yield country_code, phone, _id
      
def get_text_from_speech(wav_path):
  number_words = {"one":'1', "two":'2', "three":'3', "four":'4', "five":'5', 
                  "six":'6', "seven":'7', "eight":'8', "nine":'9', "zero":'0'}
  out = TemporaryFile()
  info_command = Popen(["/root/textvoice/speech_to_text", wav_path], stdout=out)
  info_command.wait()
  out.seek(0)
  result = json.loads(out.read())
  speech = result["Words"]
  numbers_found = ""
  for word in speech:
    if word in number_words:
      numbers_found = numbers_found + number_words[word]
      if len(numbers_found) == 6:
        break
  return numbers_found

def get_token():
  out = TemporaryFile()
  get_token_command = Popen(["php", "/root/textvoice/get-token.php"], stdout=out)
  get_token_command.wait()
  out.seek(0)
  return out.read()

def get_account_id(phone_number):
  out = TemporaryFile()
  wart_command = Popen(["xvfb-run", "mono", "WART.exe", "id" "raw=true" "number={}".format(phone_number)],
                       stdout=out)
  wart_command.wait()
  out.seek(0)
  return out.read()
