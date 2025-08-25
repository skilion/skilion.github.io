import subprocess
from pathlib import Path
import time
import sys

# The state file name is now the only global constant.
STATE_FILE_NAME = ".last_mod_time"

def get_max_last_modified_time(directory_path: Path) -> float:
    """
    Recursively finds the most recent modification time of any file
    in the given directory.
    """
    max_mtime = 0.0
    # Use rglob('*') to recursively find all files and directories.
    # We then filter to ensure we're only checking files.
    files = [p for p in directory_path.rglob('*') if p.is_file()]

    if not files:
        return 0.0 # No files in the directory.

    max_mtime = max(p.stat().st_mtime for p in files)

    return max_mtime

def read_last_known_time(file_path: Path) -> float:
    """Reads the timestamp from the state file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            return float(content)
    except (FileNotFoundError, ValueError):
        # If the file doesn't exist or is empty/corrupt, start from time 0.
        return 0.0

def write_last_known_time(file_path: Path, timestamp: float):
    """Writes the given timestamp to the state file."""
    try:
        with open(file_path, 'w') as f:
            f.write(str(timestamp))
        print(f"Successfully updated state file: {file_path}")
    except IOError as e:
        print(f"Error: Could not write to state file {file_path}. Reason: {e}")


def run_git_commands(directory: str):
    """
    Executes git add, commit, and push commands in the specified directory.
    """
    try:
        print("Executing 'git add .'...")
        # The 'capture_output=True' and 'text=True' arguments allow us to see the command's output.
        add_result = subprocess.run(["git", "add", "."], cwd=directory, check=True, capture_output=True, text=True)
        print(add_result.stdout)

        # Check if there are changes to commit by checking the status.
        status_result = subprocess.run(["git", "status", "--porcelain"], cwd=directory, check=True, capture_output=True, text=True)
        if not status_result.stdout.strip():
            print("No changes to commit.")
            return True # Nothing to do, so we consider it a success.

        print("Executing 'git commit'...")
        commit_message = f"Auto-commit: Files updated on {time.strftime('%Y-%m-%d %H:%M:%S')}"
        commit_result = subprocess.run(["git", "commit", "-m", commit_message], cwd=directory, check=True, capture_output=True, text=True)
        print(commit_result.stdout)

        print("Executing 'git push'...")
        push_result = subprocess.run(["git", "push"], cwd=directory, check=True, capture_output=True, text=True)
        print(push_result.stdout)

        print("\nGit commands executed successfully.")
        return True

    except FileNotFoundError:
        print("Error: 'git' command not found. Is Git installed and in your system's PATH?")
        return False
    except subprocess.CalledProcessError as e:
        # This exception is raised if a command returns a non-zero exit code (i.e., an error).
        print(f"Error executing Git command in '{directory}'.")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"Output:\n{e.stdout}")
        print(f"Error Output:\n{e.stderr}")
        return False

def main():
    # Check if a directory path was provided as a command-line argument.
    if len(sys.argv) < 2:
        print("Error: No directory specified.")
        print("Usage: python your_script_name.py /path/to/your/git/repository")
        sys.exit(1) # Exit the script with an error code.

    directory_to_watch = sys.argv[1]

    # Validate the directory path
    directory_path = Path(directory_to_watch)
    if not directory_path.is_dir() or not (directory_path / ".git").is_dir():
        print(f"Error: The provided path '{directory_to_watch}' is not a valid Git repository.")
        return

    print(f"Watching directory: {directory_path}")

    state_file_path = directory_path / STATE_FILE_NAME

    # 1. Get the most recent modification time from the files in the directory.
    current_max_time = get_max_last_modified_time(directory_path)
    if current_max_time == 0.0:
        print("No files found in the directory to check. Exiting.")
        return

    # 2. Get the last saved modification time from our state file.
    last_known_time = read_last_known_time(state_file_path)

    print(f"Current max modified time: {current_max_time} ({time.ctime(current_max_time)})")
    print(f"Last known modified time:  {last_known_time} ({time.ctime(last_known_time)})")

    # 3. Compare times and decide whether to run Git commands.
    if current_max_time > last_known_time:
        print("\nChanges detected. Running Git commands...")

        # 4. Run the git add, commit, and push commands.
        success = run_git_commands(str(directory_path))

        # 5. If the commands were successful, update the state file with the new time.
        if success:
            write_last_known_time(state_file_path, current_max_time)
        else:
            print("\nGit commands failed. State file will not be updated.")
    else:
        print("\nNo new modifications found. Nothing to do.")

if __name__ == "__main__":
    main()
