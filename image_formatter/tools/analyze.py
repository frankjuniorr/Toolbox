import os
import shutil
import sys

class Analyze:
    """
    Analyze folder path and show some information about this path
    """

    # ============================================
    def __init__(self, path):
        self.path = path

    # ============================================
    def _convert_size(self, size_bytes):
        """
        Function to convert byte size, to better human read
        """
        DECIMAL = 2

         # KB
        total_size = size_bytes/1024
        unit = "KB"

        # MB
        if total_size > 1024:
            total_size = total_size/1024
            unit = "MB"

        # GB
        if total_size > 1024:
            total_size = total_size/1024
            unit = "GB"
        
        total_size = f"{round(total_size, DECIMAL)} {unit}"
        return total_size

    # ============================================
    def get_path_data(self):
        """
        Function to extract some datas about this path, 
        like AllFileFormats, path Size and Total Files
        """
        path_data = {"AllFormats": None, "Size":None, "TotalFiles": None}
        size_bytes = 0
        total_files = 0
        # this set() is same to "uniq" values
        file_formats = set()
        for root, dirs, files in os.walk(self.path):
            for name in files:
                file_extension = os.path.splitext(name)
                file_extension = file_extension[1].replace(".", "")
                file_formats.add(file_extension)
                total_files += 1

                filepath = os.path.join(root, name)
                # skip if it is symbolic link
                if not os.path.islink(filepath):
                    size_bytes += os.path.getsize(filepath)

        
        total_size = self._convert_size(size_bytes)
        path_data["TotalFiles"] = total_files
        path_data["Size"] = total_size
        path_data["AllFormats"] = file_formats

        return path_data

    # ============================================
    def make_backup(self):
        """
        Function that make backup from this path to "{home}/Documents/backup_photos"
        """
        home = os.environ['HOME']
        backup_destiny = f"{home}/Documents/backup_photos"

        if os.path.isdir(path):
            print(f"backup folder: {backup_destiny}")
            print("already exist")
            sys.exit()

        try:
            print("backuping...")
            shutil.copytree(self.path, backup_destiny)
        except shutil.Error as e:
            print('Directories are the same: %s' % e)
        except OSError as e:
            print('Any error saying that the directory doesnt exist: %s' % e)

    # ============================================
    def print_result(self):
        """
        Print the final result of path data extracted, to human analyze
        """
        folder_data = self.get_path_data()

        all_formats = " "
        all_formats = all_formats.join(folder_data["AllFormats"])
        size = folder_data["Size"]
        total_files = folder_data["TotalFiles"]

        print("Analyze folder:")
        print(path)
        print("===================================")
        print(f"Total files in this folder: {total_files}")
        print(f"All file formats in folder: {all_formats}")
        print(f"Folder Size: {size}")
        print("===================================")

        print()
        value = input("Make the Backup?: ").lower()
        if value == "yes":
            self.make_backup()

# ============================================
# MAIN
# ============================================
if __name__ == '__main__':

    # get path from script arguments
    path = None
    try:
        path = sys.argv[1]
    except IndexError:
        print("type a valid path as argument")
        sys.exit()

    if not os.path.isdir(path):
        print(f"Path not found: {path}")
        sys.exit()

    print()
    analyze = Analyze(path)
    analyze.print_result()
        