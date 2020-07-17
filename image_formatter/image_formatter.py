import exiftool, os, re, sys, glob, unidecode, subprocess

from tqdm import tqdm
from log_manager import LogManager

class ImageFormatter:

    # ============================================
    def __init__(self, path):
        # path that script will run
        self.path = path

        # flag to enable debug messages
        # if this flag "True", any file is renamed
        self.debug_mode = True

        # flag to enable log messages
        self.log_mode =  True

        # object logs instances
        self.logger_duplicate = LogManager.instance().getLoggerDuplicateFile

        # list of files supported:
        self.images_list = ["jpg", "png"]
        self.video_list = ["mp4", "avi"]

        # total folders renamed by script
        self.total_folders = 0
        # total files renamed by script
        self.total_files_renamed = 0
        # total duplicated files save in log folder
        self.total_duplicated_files = 0
        # total of files analyzed based on "self.images_list" and "self.video_list"
        self.total_files = 0
        # files that already renamed and not to do with its
        self.total_files_ok = 0

    # ============================================
    def _find_files(self, path):
        """
        Function search image and video files in "path"

        Return: a list with all files searched
        """
        all_files = []
        path = f"{path}/**/"

        self.printLog("Finding files...")

        # find for image files
        for images in self.images_list:
            search = f"{path}*.{images}"
            images_files = glob.glob(search, recursive = True)
            all_files += images_files

        # find for video files
        for videos in self.video_list:
            search = f"{path}*.{videos}"
            videos_files = glob.glob(search, recursive = True)
            all_files += videos_files

        return all_files

    # ============================================
    def checkFilesAlreadyRenamed(self, file_list):
        """
        Function that check which files already renamed

        Return: a list with all files except the files that are with name ok
        """
        files_ok = []
        for file_index in range(len(file_list)):
            basename =  os.path.basename(file_list[file_index])
            dirname = os.path.dirname(file_list[file_index])
            parent_folder = os.path.basename(dirname)
            filename_without_extension = os.path.splitext(basename)[0]

            # check if file startWith this pattern, i.e.: "2020-04-01_10:01:05"
            regex = "^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
            already_renamed = re.search(regex, basename)

            # if file match the pattern and contain the "parent_folder" in the name
            # the file is ok
            if already_renamed != None and filename_without_extension.endswith(parent_folder):
                item = file_list[file_index]
                files_ok.append(item)
                self.total_files_ok += 1

        # remove of list, all files that are with name ok
        for file_ok in files_ok:
            file_list.remove(file_ok)

        return file_list

    # ============================================
    def _extract_metatags(self):
        """
        Function that extract all exif tags of a file_lit
        
        Return: a list with all exiftags of all files
        """
        # get the file list
        files_list = self._find_files(self.path)
        self.total_files = len(files_list)
        metadata_list = []
        EMPTY = 0

        # filter the file list
        files_list = self.checkFilesAlreadyRenamed(files_list)

        # if list not empty, extract all exif tags and save in the "metadata_list"
        if self.total_files != EMPTY:
            with exiftool.ExifTool() as exif:
                progress_bar = tqdm(files_list)
                for item in progress_bar:
                    progress_bar.set_description("[LOG]: Extracting exif...")
                    metadata_list.append(exif.get_metadata(item))
        else:
            print("All files analyzed, already renamed =D")
            sys.exit()

        return metadata_list

    # ============================================
    def generateNewFileName(self, file_dict):
        """
        Function with rules to rename a filename

        Params:
        - file_dict
        example:
        {"filename":value, "Createdate":value}

        Return: new filename string
        """
        basename = os.path.basename(file_dict["filename"]).strip()
        dirname = os.path.dirname(file_dict["filename"])
        parent_folder = os.path.basename(dirname).strip()

        # format date string
        date = file_dict["Createdate"].split("-")

        # se for um CreateDate, o array vem assim: "['2012:04:07', '02:02:10']"
        # mas se for um Modificationdate, vem com timezone: "['2012:04:08', '21:41:17', '03:00']".
        # Então esse slice é pra remover o timezone, caso tenha
        date = date[0:2]

        date_year, date_hour = date
        
        date_year = date_year.replace(":", "-")
        create_date = f"{date_year}_{date_hour}"

        file_extension = os.path.splitext(basename)[1]

        new_filename = f"{create_date}_{parent_folder}{file_extension}"
        new_path = os.path.join(dirname, new_filename)

        return new_path

    # ============================================
    def _remove_special_caracteres(self, string):
        """
        Function with many rules to remove special caractres of string

        Params:
        - string, to apply this rules
        
        Return: modified string
        """
        underline = "_"
        empty = ""
        hifen = "-"
        regex_dict = {
            # remove quotes
            "[\"']": empty,
            # replace any strange caractere to 'underline'
            "[^a-z0-9._-]": empty,
            # remove consecutive underlines
            "__*": underline,
            # remove consecutive hífens
            "--*": hifen,
            # remove underline that are before hífens and dots
            "_([.-])": r"\1",
            # remove underline that are after hífens and dots
            "([.-])_": r"\1",
            # replace hífens in begin of string to underline
            "^-": underline,
            # empty strings replace to underline
            "^$": underline
        }

        # first of all, modify the string to lowerCase and replace space to hífer
        string = string.strip().lower().replace(" ", hifen)

        # remove acentos
        string = unidecode.unidecode(string)

        # loop in all regex, to replace.
        for regex, to_replace in regex_dict.items():
            string = re.sub(regex, to_replace, string)

        return string

    # ============================================
    def _extractCreateDate(self):
        """
        Function that extract only CreateDate of exiftags list

        Return: a dict list with filename and exif:CreateDate
        """
        files_list = []
        exif_tag = ""

        self.printLog("Extract dates from files...")

        for metadata in self._extract_metatags():
            file_date = ""
            file = {"filename": None, "Createdate":None}

            # extract "SourceFile" from exif
            source_file = metadata["SourceFile"]

            file_extension = os.path.splitext(source_file)
            file_extension = file_extension[1].replace(".", "")

            # if file is a image, get a kind of exif tag,
            # if a video file, get other kind of exif tag
            if file_extension in self.images_list:
                exif_tag = "EXIF:CreateDate"
            elif file_extension in self.video_list:
                exif_tag = "QuickTime:MediaCreateDate"

            try:
                file_date = metadata[exif_tag]
            except KeyError:
                # se o arquivo não tiver a tag "EXIF:CreateDate", vai cair nesse catch
                #  então, procure pela tag 'File:FileModifyDate'
                file_date = metadata["File:FileModifyDate"]

            # reforce aqui também, porque pode ser que ele tenha a tag
            # não caia no catch, mas venha nese formato: '0000:00:00 00:00:00'
            # (principalmente em arquivos de vídeo)
            if file_date == '0000:00:00 00:00:00':
                file_date = metadata["File:FileModifyDate"]

            file["filename"] = source_file
            file["Createdate"] = file_date.replace(" ", "-")
            files_list.append(file)

        return files_list

    # ============================================
    def standardizeFileFormats(self):
        """
        Function that normalize file formats
        (like "JPG" to "jpg", ""jpeg", to "jpg", and so on)
        """
        self.printLog("Normalizing fileformats...")
        for root, dirs, files in os.walk(self.path):
            for name in files:
                original_file_path = os.path.join(root, name)
                filename, file_extension = os.path.splitext(name)

                # fix file_extensions.
                # lower case and normalize formats
                file_extension = file_extension.lower().replace(".jpeg", ".jpg")
                filename = filename + file_extension
                new_file_path = os.path.join(root, filename)

                if original_file_path != new_file_path:
                    self.printLog(f"Before: {original_file_path}")
                    self.printLog(f"After: {new_file_path}")
                    self.printLog("=======================")
                    os.rename(original_file_path, new_file_path)

    # ============================================
    def renameAllFolders(self):
        """
        Function to rename all folder inside 'path'

        params:
        - root path
        """

        print()
        self.printLog("Renaming folders...")

        for root, dirs, files in os.walk(self.path):
            for name in dirs:

                new_folder_name = self._remove_special_caracteres(name)
                original_path = os.path.join(root, name)
                new_folder_path = os.path.join(root, new_folder_name)

                if original_path != new_folder_path:
                    self.total_folders += 1
                    if self.debug_mode == False:
                        self.printLog(f"Before: {original_path}")
                        self.printLog(f"After: {new_folder_path}")
                        self.printLog("=======================")
                        os.rename(original_path, new_folder_path)
                    else:
                        self.printDebug(original_path)
                        self.printDebug(new_folder_path)
                        self.printDebug("=======================")

    # ============================================
    def renameAllFiles(self):
        """
        Function to rename only files
        """
        new_file_path = None

        metadata_list = self._extractCreateDate()

        self.printLog("Renaming files...")

        for item in metadata_list:
            original_file_path = item["filename"]

            # Check if file exist
            if not os.path.isfile(original_file_path):
                print(f"File not found: {original_file_path}")
                sys.exit()

            # get the new name
            new_file_path = self.generateNewFileName(item)

            if original_file_path != new_file_path:
                if self.debug_mode == False:
                    # if file not exist...
                    if not os.path.isfile(new_file_path):
                        self.printLog(f"Before: {original_file_path}")
                        self.printLog(f"After: {new_file_path}")
                        self.printLog("=======================")
                        self.total_files_renamed += 1
                        os.rename(original_file_path, new_file_path)
                    else:
                        # In this point, if file already exist, if because it already renamed
                        # so, is possible that this file is duplicated (by timedate)
                        self.logger_duplicate.info(original_file_path)
                        self.logger_duplicate.info(new_file_path)
                        EMPTY_MSG = ''
                        self.logger_duplicate.info(EMPTY_MSG)
                        self.total_duplicated_files += 1
                else:
                    self.printDebug(new_file_path)

        # print summary
        self.summary()

    # ============================================
    def summary(self):
        """
        Function to print summary in final of execution
        """
        print()
        print("----------- SUMMARY -----------")
        print(f"Total files analyzed: {self.total_files}")
        print(f"Files already ok: {self.total_files_ok}")
        print(f"Folders Renamed: {self.total_folders}")
        print(f"Files Renamed: {self.total_files_renamed}")
        print(f"Files in Log [Duplicated]: {self.total_duplicated_files}")
        print()

    # ============================================
    def checkDuplicateFilesByBytes(self):
        """
        Check if exist duplicate files (by byte)
        """
        command = ['fdupes', '-r', self.path]
        result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
        return result

    # ============================================
    def enableDebugMode(self, mode):
        """
        Enable/Disable debug mode
        """
        self.debug_mode = mode
    
    # ============================================
    def printLog(self, message):
        """
        Enable/disable log messages
        """
        if self.log_mode == True:
            print(f"[LOG]: {message}")

    # ============================================
    def printDebug(self, message):
        """
        Print debug messages
        """
        if self.debug_mode == True:
            print(f"[DEBUG]: {message}")
    