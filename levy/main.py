from argparse import ArgumentParser
from datetime import datetime

from .styles import *
from .helper import *

import git
import os

def run(args):
    if not args.configure:
        if args.user == None:
            log("User is empty", 'error')
            return
        if args.track == None:
            log("What type of file should be tracked?", 'error')
            return
        config = load_config('./config.yml')
        if config == None:
            return
        try:
            repo = git.Repo(config['repo'])
        except:
            log("Invalid repo location. Please setup config file again.", "error")
            return
        if args.today:
            date = 'today {}'.format(CBEIGE + CBOLD + date_format('%Y-%m-%d') + CEND)
            commits = [x for x in repo.iter_commits(config['branch']) if x.author.name == args.user and date_format('%Y-%m-%d', x.committed_date) == date_format('%Y-%m-%d')]
        elif args.all:
            date = CBEIGE + CBOLD+'all time'+CEND
            commits = [x for x in repo.iter_commits(config['branch']) if x.author.name == args.user]
        else:
            if args.start == None or type(args.start) != type("string"):
                log('Argument for start time is invalid', "error")
                return
            if args.end == None or type(args.end) != type(1):
                log('Argument for end time is invalid so setting end date to today', 'warning')
                args.end = str(datetime.today()).split(" ")[0].replace("-", "/")
            args.start = int(datetime.timestamp(datetime.strptime(args.start, '%Y/%m/%d')))
            args.end = int(datetime.timestamp(datetime.strptime(args.end, '%Y/%m/%d')))
            date = 'from date {} to {}'.format(date_format('%Y-%m-%d', args.start), date_format('%Y-%m-%d', args.end))
            commits = [x for x in repo.iter_commits(config['branch']) if x.author.name == args.user and date_format('%Y-%m-%d', int(args.start)) <= date_format('%Y-%m-%d', x.committed_date) <= date_format('%Y-%m-%d', int(args.end))]
        log('Getting {} logs for {} for {}'.format(CBEIGE+CBOLD+args.track+CEND, CBEIGE+CBOLD+args.user+CEND, date))
        logger = Queue()
        for x in commits:
            files = process_files(x.stats.files, args.track)
            message = x.message
            commitid = x.hexsha
            for idx, onefile in enumerate(files):
                logger.add_row('{}_{}'.format(commitid, idx), args.user, onefile, message, date_format('%Y-%m-%d', x.committed_date))
        if args.export != None:
            filename = args.export
        else:
            filename = "./levy_{}_gitlogs.csv".format(args.user)
        logger.export_to_csv(filename, args.unique)
    else:
        log("Generating config.yml")
        options = {}
        key, value = prompt_question("Please paste the full path to the repository to track => ", 'repo')
        options[key] = value
        key, value = prompt_question("Which branch would you like to track? (Eg: main/master) => ", 'branch')
        options[key] = value
        if not os.path.exists(CONFIG_PATH):
            os.mkdir(CONFIG_PATH)
        with open(CONFIG_PATH+"config.yml", "w") as f:
            f.write(yaml.dump(options))
        log("Finished generating config file. Please try to run the script again using "+ CITALIC+CBOLD+"levy --user {author} --today/--all/--start {date in YYYY/M/D format}")

def main():
    parser = ArgumentParser()
    parser.add_argument('-u', '--user', type=str, help = 'specify the user whose git commits are to be logged')
    parser.add_argument('-t', '--track', type=str, help = 'specify which type of file to track')

    controllers = [
        ['today', "flag to set the log to get only today's commit"],
        ['all', 'flag to specify the logger to pull all commits till today'],
        ['configure', 'specify the settings for this script'],
        ['unique', 'get only unique files per day in the log'],
    ]

    for controller, helper in controllers:
        parser.add_argument('--{}'.format(controller), action='store_true', help = helper)

    parser.add_argument('-b', '--branch', type=str, help = 'specify which branch to update from REQUIRES UPDATE FLAG')
    parser.add_argument('--start', type=str, help = 'specify which date should the logger start logging information')
    parser.add_argument('--end', type=str, help = 'specify which date should the logger stop logging information')
    parser.add_argument('-x', '--export', type=str, help = 'specify the name of the file to export the generated csv')

    args = parser.parse_args()
    run(args)