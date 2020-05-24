import sys, os, re

class LogFilter:

    # ============================================
    def __init__(self, log_path):
        self.log_path = self.validation(log_path)

        self.renamed_files = []
        self.all_lines = []

    # ============================================
    def validation(self, log_file):
        """
        Function to validate path passed by param
        """
        home = os.environ['HOME']
        log_file = log_file.replace("~", home)

        if log_file != None and \
            not os.path.isfile(log_file) \
            and os.path.getsize(log_file) == 0:
            print("Arquivo de log inválido")
            sys.exit()

        return log_file

    # ============================================
    def fixWhatsappImages(self, file_path):
        """
        Function to identify files saved by Whatsapp Mobile

        Params:
        file_path --> file to be analyzed

        Return:
        new_path --> new name to this pattern taht will be renamed. None in otherwise
        """
        whatsapp_mobile_pattern = 'WA[0-9]{4}'
        images_from_whatsapp = re.search(whatsapp_mobile_pattern, file_path)

        if images_from_whatsapp != None:
            basename = os.path.basename(file_path)
            dirname = os.path.dirname(file_path)
            parent_folder = os.path.basename(dirname).strip()
            file_extension = os.path.splitext(basename)[1]

            date = basename.split("-")[1]

            if not date.isdigit() or len(date) != 8:
                print(f"Formato de data inválido: {file_path}")
                return None
            else:
                ano = date[0:4]
                mes = date[4:6]
                dia = date[6:8]
                date = f"{ano}-{mes}-{dia}_00:00:00"

                new_filename = f"{date}_{parent_folder}{file_extension}"
                new_path = os.path.join(dirname, new_filename)

                count = 1
                while os.path.isfile(new_path):
                    new_filename = f"{date}_{parent_folder}-{count}{file_extension}"
                    new_path = os.path.join(dirname, new_filename)
                    count += 1
                else:
                    return new_path
        else:
            return None

    # ============================================
    def renameFile(self, path, new_path):
        """
        Function to rename a file and set EXIF with new datetime

        Params:
        path --> original path name
        new_path --> new path to rename
        """
        print(f"Antes: {path}")
        print(f"Depois: {new_path}")
        print("=======================")
        self.renamed_files.append(path)
        # TODO: setar o exif aqui
        os.rename(path, new_path)

    # ============================================
    def deleterenamedFilesFromLog(self):
        """
        Function to delete all file in log that have already been renamed
        """
        file = open(self.log_path, "w+")
        for line in self.all_lines:
            if not line in self.renamed_files:
                file.write(f"{line}\r\n")
        file.close()

    # ============================================
    def renameFilesFromLog(self):
        """
        Function to rename all files saved in log, based in patterns
        """
        self.renamed_files = []
        self.all_lines = []

        file = open(self.log_path, "r")
        for line in file:
            line = line.strip("\n")

            # se o endereço lido do log, não for um arquivo válido
            # logo, ele é um endereço inválido ou inexistente
            # então adicione na lista que será removida do arquivo de log
            if not os.path.isfile(line):
                self.renamed_files.append(line)
                self.all_lines.append(line)
            else:
                self.all_lines.append(line)
                new_file = None

                new_file = self.fixWhatsappImages(line)
                if new_file != None:
                    self.renameFile(line, new_file)
        file.close()

if __name__ == '__main__':

    # recebe o arquivo de log por parametro.
    # ex:
    # python3 log_filter.py ~/log/image_formatter/2020-05-21_23-01-59.log
    log_path = None
    try:
        log_path = sys.argv[1]
    except IndexError:
        print("type a valid path as argument")
        sys.exit()

    # renomea alguns arquivos identificados por padrões de nome
    logFilter = LogFilter(log_path)
    logFilter.renameFilesFromLog()

    # remove os arquivos renomeados do arquivo de log
    logFilter.deleterenamedFilesFromLog()

    


    