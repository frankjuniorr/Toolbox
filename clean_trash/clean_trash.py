#!/bin/python3

# ##############################################################################
# [Description]:
#   Script that clean Trash after 1 month of DeletionDate.
#   OBS: The script output is not terminal, but is logfile save in "$HOME/log/clean_trash"
#
# [Use]:
#   ./clean_trash.py
# ##############################################################################

from datetime import datetime
import os
import logging
import math
from enum import Enum


class LogType(Enum):
    SUMMARY = 0
    LOG = 1

# ============================================
def log_path(log_type_enum):
  """
  Function that return Log file path
  """
  log_date_format = '%Y-%m-%d_%H:%M:%S'
  log_date_time = datetime.now().strftime(log_date_format)

  script_name = os.path.basename(__file__)
  script_name = os.path.splitext(script_name)[0]
  home = os.environ['HOME']

  log_path = f"{home}/log/{script_name}/"

  if not os.path.exists(log_path):
    os.makedirs(log_path)

  if log_type_enum == LogType.SUMMARY:
    log_file = f"{log_path}/{log_date_time}_summary.log"
  elif log_type_enum == LogType.LOG:
    log_file = f"{log_path}/{log_date_time}.log"

  return log_file

# ============================================
def log_clean():
  """
  Function that remove log file if file is empty
  """
  for log_type in LogType:
    log_file = log_path(log_type)
    log_file_size = os.path.getsize(log_file)
    if log_file_size == 0:
      os.remove(log_file)

# ============================================
def configure_log(name, log_file):
  """
  Function that configure Log
  """
  formatter = logging.Formatter('%(message)s')
  handler = logging.FileHandler(log_file)
  handler.setFormatter(formatter)

  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)
  logger.addHandler(handler)

  return logger

# ============================================
def remove_files(filename):
  """
  Function that remove files in Trash
  """
  os.remove(f"{home}/.local/share/Trash/info/{filename}.trashinfo")
  file = f"{home}/.local/share/Trash/files/{filename}"
  if os.path.isfile(file):
    os.remove(file)
  else:
    os.rmdir(file)

# ============================================
def compare_dates(trashed_file_dict):
  """
  Function to compare file deletionTime with currentTime
  """
  summary = {"FileSize": None}

  date_format = '%Y-%m-%d %H:%M:%S'
  deletion_date = trashed_file_dict["deletionDate"]
  filename = trashed_file_dict["filename"]
  filename = os.path.basename(filename)

  # file deletion date
  deletion_date = deletion_date.replace("T", " ")
  deletion_datetime = datetime.strptime(deletion_date, date_format)

  # current time
  current_time_string = datetime.now().strftime(date_format)
  current_datetime = datetime.strptime(current_time_string, date_format)

  difference_in_days = (current_datetime - deletion_datetime).days

  real_filename = f"{home}/.local/share/Trash/files/{filename}"
  size = os.path.getsize(real_filename)

  if difference_in_days >= 30:
    # remove_files(filename)
    logger.info(filename)
    summary["FileSize"] = size

  return summary

# ============================================
def build_summary(summary_files):
  """
  Function to build summary
  """
  total_size = 0
  deleted_files = {"Files":None, "Size": None}

  # get total files
  total_files = len(summary_files)

  for index in range(total_files):
    total_size +=  summary_files[index]["FileSize"]

  # MB
  total_size = math.trunc(total_size/1024/1024)
  unit = "MB"

  # GB
  if total_size > 1024:
    total_size = (total_size / 1024)
    unit = "GB"

  if total_files != 0:
    logger_summary.info(f"Files: {total_files}")
    logger_summary.info(f"Size: {total_size} {unit}")
    deleted_files["Files"] = total_files
    deleted_files["Size"] = f"{total_size} {unit}"

  return deleted_files


# ============================================
def get_file_info(filename):
  """
  Function to get info about trashed file:
  like 'filename' and 'deletionTime'

  return: a dict with this info
  """
  trashed_file_dict = {"filename":None, "deletionDate":None}

  trashed_file_dict["filename"] = os.path.splitext(filename)[0]

  with open(filename, 'r', newline='') as file:
    content = file.read()
    search_index = content.find("DeletionDate")
    line = content[search_index:-1]

    deletion_date = line.split("=")
    deletion_date = deletion_date[1]
    trashed_file_dict["deletionDate"] = deletion_date
  file.close()

  return trashed_file_dict

# ============================================
def notification(deleted_files):
  """
  Function to send notification in the end of script execution
  """
  notification_title = os.path.basename(__file__)

  files = deleted_files["Files"]
  size = deleted_files["Size"]
  notification_description = f"{files} Arquivos removidos: {size} Liberados"
  notification_icon = f"{os.path.dirname(os.path.abspath(__file__))}/python-logo-64px.png"

  command = f"/usr/bin/notify-send \"{notification_title}\" \"{notification_description}\" --icon={notification_icon}"

  if files != None:
    os.system(command)

# ============================================
# Função Main
# ============================================
if __name__ == '__main__':
  home = os.environ['HOME']
  trash_info_path = f"{home}/.local/share/Trash/info/"
  exist_trash = os.path.isdir(trash_info_path)

  # only run the script if trash is not empty
  if exist_trash:
    # configure log
    logger_summary = configure_log("log_summary", log_path(LogType.SUMMARY))
    logger = configure_log("log_file", log_path(LogType.LOG))

    trashed_files_list = []
    summary_files = []

    trashed_files_info = os.listdir(trash_info_path)

    # get the information about trashed files
    for file_trashed in trashed_files_info:
      file_trashed = f"{home}/.local/share/Trash/info/{file_trashed}"
      trashed_files_list.append(get_file_info(file_trashed))

    # compare trashedFiles deletionDates with currentdate
    for index in range(len(trashed_files_list)):
      summary = compare_dates(trashed_files_list[index])
      if summary["FileSize"] != None:
        summary_files.append(summary)

    deleted_files = build_summary(summary_files)
    notification(deleted_files)
    log_clean()
