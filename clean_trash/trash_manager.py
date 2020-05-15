from datetime import datetime
import os

from log_manager import LogManager

class TrashManager:

    # ============================================
    def __init__(self):
        self.home = os.environ['HOME']

    # ============================================
    def remove_files(self, filename):
        """
        Function that remove files in Trash
        """
        file_info = f"{self.home}/.local/share/Trash/info/{filename}.trashinfo"
        file = f"{self.home}/.local/share/Trash/files/{filename}"

        os.remove(file_info)

        if os.path.isfile(file):
            os.remove(file)
        else:
            os.rmdir(file)

    # ============================================
    def compare_dates(self, trashed_file_dict, logger):
        """
        Function to compare file deletionTime with currentTime
        """
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

        real_filename = f"{self.home}/.local/share/Trash/files/{filename}"
        size = os.path.getsize(real_filename)

        if difference_in_days >= 30:
            # remove_files(filename)
            logger.info(filename)
            return size

        return None

    # ============================================
    def build_summary(self, summary_files):
        """
        Function to build summary
        """
        total_size = 0
        DECIMAL = 2
        deleted_files = {"Files":None, "Size": None}

        # get total files
        total_files = len(summary_files)

        for index in range(total_files):
            # get total size in bytes
            total_size +=  summary_files[index]

        # MB
        total_size = round(total_size/1024/1024, DECIMAL)
        unit = "MB"

        # GB
        if total_size > 1024:
            total_size = round(total_size/1024, DECIMAL)
            unit = "GB"

        if total_files != 0:
            logger_summary = LogManager.instance().getLoggerSummary

            logger_summary.info(f"Files: {total_files}")
            logger_summary.info(f"Size: {total_size} {unit}")
            deleted_files["Files"] = total_files
            deleted_files["Size"] = f"{total_size} {unit}"

        return deleted_files


    # ============================================
    def get_file_info(self, filename):
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
    def notification(self, deleted_files):
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

        LogManager.instance().log_clean()