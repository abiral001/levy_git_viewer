# levy_git_viewer


A git log helper to detect and log local commit messages to a csv file that is filtered using author and date of commit.

Can be installed by downloading pre compiled packages from github actions.

Download the .whl file and install using pip install {downloaded_file}.whl

First run levy --configure to set the repo link and the branch to track.

Run using levy --user {author} --today --track php