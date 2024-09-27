import os
import shutil


def print_cd_results(cmd: str) -> None:
    try:
        os.chdir(cmd[3:])
    except FileNotFoundError:
        print('Invalid command')
    else:
        print(os.getcwd().split('/')[-1])


def print_ls_results(cmd: str) -> None:
    ls_dir_files = os.listdir()
    if len(ls_dir_files) != 0:
        ls_ext_valid = True
        ls_dir_files_sorted = ls_dir_files.copy()
        for dir_file in ls_dir_files:
            if dir_file.rfind('.') > 0:
                ls_dir_files_sorted.remove(dir_file)
                if cmd.endswith('ls'):
                    pass
                elif cmd.endswith(' -l'):
                    dir_file += f' {os.stat(dir_file).st_size}'
                elif cmd.endswith(' -lh'):
                    file_size_rounded = round(os.stat(dir_file).st_size)
                    if file_size_rounded < 1_024:
                        dir_file += f' {file_size_rounded}B'
                    elif 1_024 <= file_size_rounded < 1_024_000:
                        dir_file += f' {str(file_size_rounded)[:-3]}KB'
                    elif 1_024_000 <= file_size_rounded < 1_024_000_000:
                        dir_file += f' {str(file_size_rounded)[:-6]}MB'
                    elif 1_024_000_000 >= file_size_rounded:
                        dir_file += f' {str(file_size_rounded)[:-9]}GB'
                else:
                    print('Invalid command')
                    ls_ext_valid = False
                    break
                ls_dir_files_sorted.append(dir_file)
        if ls_ext_valid is True:
            for dir_file in ls_dir_files_sorted:
                print(dir_file)


def delete_file_folder(cmd: str) -> None:
    abs_rel_path = cmd[3:].strip()
    if len(abs_rel_path) == 0:
        print('Specify the file or directory')
    elif abs_rel_path.startswith('.') and len(abs_rel_path) >= 2:
        file_ext_exists = False
        for dir_file in os.listdir():
            if dir_file.endswith(abs_rel_path):
                os.remove(dir_file)
                file_ext_exists = True
        if not file_ext_exists:
            print(f'File extension {abs_rel_path} not found in this directory')
    elif abs_rel_path.rfind('.') > 0:
        try:
            os.remove(abs_rel_path)
        except FileNotFoundError:
            print('No such file or directory')
    elif abs_rel_path.rfind('.') <= 0:
        try:
            shutil.rmtree(abs_rel_path)
        except FileNotFoundError:
            print('No such file or directory')


def move_file_folder(cmd: str) -> None:
    if len(mv_commands := cmd[3:].split()) != 2:
        print('Specify the current name of the file or directory and the new location and/or name')
    elif len(mv_commands[0]) >= 2 and mv_commands[0].startswith('.'):
        file_ext_exists = False
        for dir_file in os.listdir():
            if dir_file.endswith(mv_commands[0]):
                if dir_file in os.listdir(mv_commands[1]):
                    print(f'{dir_file} already exists in this directory. Replace? (y/n)')
                    user_input = input()
                    if user_input == 'n':
                        continue
                    elif user_input == 'y':
                        os.remove(f'{os.path.abspath(mv_commands[1])}/{dir_file}')
                        shutil.move(dir_file, mv_commands[1])
                else:
                    shutil.move(dir_file, mv_commands[1])
                file_ext_exists = True
        if not file_ext_exists:
            print(f'File extension {mv_commands[0]} not found in this directory')
    elif ((this_dir := os.path.dirname(os.path.abspath(mv_commands[0]))) ==
          (os.path.dirname(os.path.abspath(mv_commands[1]))) and mv_commands[1].split('/')[-1] in os.listdir(this_dir)
          and os.path.isfile(mv_commands[0]) and os.path.isfile(mv_commands[1])):
        print('The file or directory already exists')
    elif len(mv_commands) == 2:
        try:
            shutil.move(mv_commands[0], mv_commands[1])
        except shutil.Error:
            print('The file or directory already exists')
        except FileNotFoundError:
            print('No such file or directory')


def make_new_directory(cmd: str) -> None:
    if len(folder_path := cmd[6:]) == 0:
        print('Specify the name of the directory to be made')
    else:
        try:
            os.makedirs(folder_path)
        except FileExistsError:
            print('The directory already exists')


def copy_file(cmd: str) -> None:
    fp_dst = cmd[3:].split()
    if len(cp_commands := cmd[3:]) == 0:
        print('Specify the file')
    elif len(fp_dst[0]) >= 2 and fp_dst[0].startswith('.') and os.path.isdir(fp_dst[1]):
        file_ext_exists = False
        for dir_file in os.listdir():
            if dir_file.endswith(fp_dst[0]):
                if dir_file in os.listdir(fp_dst[1]):
                    print(f'{dir_file} already exists in this directory. Replace? (y/n)')
                    user_input = input()
                    if user_input == 'n':
                        continue
                    elif user_input == 'y':
                        os.remove(f'{os.path.abspath(fp_dst[1])}/{dir_file}')
                        shutil.copy(dir_file, fp_dst[1])
                else:
                    shutil.copy(dir_file, fp_dst[1])
                file_ext_exists = True
        if not file_ext_exists:
            print(f'File extension {fp_dst[0]} not found in this directory')
    elif len(fp_dst) == 2:
        if os.path.isdir(fp_dst[1]) is True:
            try:
                shutil.copy(fp_dst[0], fp_dst[1])
            except FileNotFoundError:
                print('No such file or directory')
            except IsADirectoryError:
                print('Specify the file')
            except shutil.SameFileError:
                print(f'{fp_dst[0].split("/")[-1]} already exists in this directory')
            else:
                if (filename := fp_dst[0].split('/')[-1]) in os.listdir(fp_dst[1]):
                    print(f'{filename} already exists in this directory')
        else:
            print('No such file or directory')

    elif len(cp_commands.split()) > 2:
        print('Specify the current name of the file or directory and the new location and/or name')


def main():
    os.chdir('module/root_folder')

    print('Input the command')

    while (command := input().strip()) != 'quit':
        if command == 'pwd':
            print(os.getcwd())
        elif command == 'cd':
            print('Invalid command')
        elif command.startswith('cd'):
            print_cd_results(command)
        elif command.startswith('ls'):
            print_ls_results(command)
        elif command.startswith('rm'):
            delete_file_folder(command)
        elif command.startswith('mv'):
            move_file_folder(command)
        elif command.startswith('mkdir'):
            make_new_directory(command)
        elif command.startswith('cp'):
            copy_file(command)
        else:
            print('Invalid command')


if __name__ == '__main__':
    main()
