import os, sys, re
from ics import Calendar
import requests
import arrow
import PySimpleGUI as sg

WEBURLREGEX = re.compile(r'^((http|https)://)(www.)?')


def valid_readable_file(filename: str, quiet=False) -> bool:
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        return True
    else:
        if not quiet:
            print(f"The following file has issues loading: {filename}")
        return False


def is_web_link(ics):
    return WEBURLREGEX.match(ics)


class BadGitPath(Exception): pass


def dir_path(path):
    if os.path.isdir(path):
        return True
    else:
        raise BadGitPath


def is_git_repo_root(path):
    if os.system(f'cd {path} && git rev-parse') == 0:
        return True
    else:
        raise BadGitPath


def main(ics: str, git_dir: str, day_shift: int = 0) -> None:
    if dir_path(git_dir) and is_git_repo_root(git_dir):
        print(f"Provided valid path and git repo: {git_dir}")

    if is_web_link(ics):
        r = requests.get(ics, timeout=10)
        c = Calendar(r.text)
    elif valid_readable_file(ics):
        with open(ics, 'r') as f:
            r = f.readlines()
        c = Calendar(r)
    else:
        print(f"could not read url/file: {ics}")
        sys.exit(2)

    now_utc = arrow.now().to('utc').shift(days=day_shift)
    start_day, end_day = now_utc.span('day')

    todays_events = {}
    for event in c.events:
        if (event.begin < end_day) and (event.begin > start_day):
            e = event.begin.to('local')
            t = e.format('HH:mm')
            todays_events[e.timestamp] = event.name + f' - {t} ->'

    sorted_todays_events = {key: value for key, value in
                            sorted(todays_events.items(), key=lambda item: item[1], reverse=True)}
    print(sorted_todays_events)

    starting_text = f"# {now_utc.format('YYYY-MM-DD')} - {now_utc.format('dddd')} ReflectLog\n\n## Events\n\n - "

    starting_text += '\n - '.join({value for _, value in sorted_todays_events.items()})
    starting_text += "\n\n## Learnt\n"
    starting_text += "\n\n## Improvements\n"

    sg.theme('GreenTan')  # give our window a spiffy set of colors
    layout = [[sg.Text('Blog your days thoughts in Markdown:', size=(40, 1))],
              [sg.Multiline(default_text=starting_text, size=(110, 35), key='textbox_data', font=('Courier 10'))],
              [sg.Button('SAVE', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
               sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]]

    window = sg.Window('ReflectLog', layout, font=('Courier', ' 13'), default_button_element_size=(8, 2),
                       use_default_focus=True)

    while True:  # The Event Loop
        event, value = window.read()
        if event in (sg.WIN_CLOSED, 'EXIT'):  # quit if exit button or X
            break
        if event == 'SAVE':
            print('SAVE detected')
            md_text = value['textbox_data']

            # let's make the folders (if they don't exist... yyyy and month especially)
            y = os.path.join(git_dir, now_utc.to('local').format('YYYY'))
            m = os.path.join(y, now_utc.to('local').format('MM'))
            d = os.path.join(m, now_utc.to('local').format('DD')+".md")
            os.makedirs(y, exist_ok=True)
            os.makedirs(m, exist_ok=True)
            with open(d, 'w') as wr:
                wr.writelines(md_text)
            print(f"Success writing to {d} ... {len(md_text)} chars")

    window.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reflect Log - a place to put your daily log")
    parser.add_argument("--ics", help='ics file/url', required=True)
    parser.add_argument("--git_log_dir", help='the location where all log is saved', default="../logs")
    parsed_args = parser.parse_args()
    print(f"Starting with following arguments: {str(parsed_args)}")
    main(parsed_args.ics, parsed_args.git_log_dir)
