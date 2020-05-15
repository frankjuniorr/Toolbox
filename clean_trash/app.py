import os
from trash_manager import TrashManager

if __name__ == '__main__':

  home = os.environ['HOME']
  trash_info_path = f"{home}/.local/share/Trash/info/"
  exist_trash = os.path.isdir(trash_info_path)
  EMPTY = 0

  trash_manager = TrashManager()

  # only run the script if trash folder exist
  if exist_trash:
    trashed_files_info = os.listdir(trash_info_path)

    # if folder is not empty
    if len(trashed_files_info) != EMPTY:
        trashed_files_list = []
        summary_files = []

        # get the information about trashed files
        for file_trashed in trashed_files_info:
            file_trashed = f"{trash_info_path}{file_trashed}"
            trashed_files_list.append(trash_manager.get_file_info(file_trashed))

        # compare trashedFiles deletionDates with currentdate
        for trashed_file in trashed_files_list:
            file_size = trash_manager.compare_dates(trashed_file)
            if not file_size is None:
                summary_files.append(file_size)

        deleted_files = trash_manager.build_summary(summary_files)
        trash_manager.notification(deleted_files)