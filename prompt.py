import os , sys

from app_core import *

from termcolor import colored
import pyfiglet

info = """
    The crowdfunding app is a platform that allows  individuals or 
    organizations  to  raise funds for various  projects or causes 
    through  an  online  platform. With the help  of  crowdfunding,
    people can  raise funds for  their  innovative ideas, startups, 
    social causes, or creative projects from a larger audience.
"""
banner = '''
   ______                       __   ______                ___            
  / ____/________ _      ______/ /  / ____/_  ______  ____/ (_)___  ____ 
 / /   / ___/ __ \ | /| / / __  /  / /_  / / / / __ \/ __  / / __ \/ __ \
/ /___/ /  / /_/ / |/ |/ / /_/ /  / __/ / /_/ / / / / /_/ / / / / / /_/ / 
\____/_/   \____/|__/|__/\__,_/  /_/    \__,_/_/ /_/\__,_/_/_/ /_/\__, /  
                                                                 /____/   
				BY MohandZaid

                '''


def prompt_functions(user_email, user_prompt):

    if user_prompt in ['help', 'h'] :
        print('\n- view-all\n- help\n- create\n- edit\n- delete\n- search\n- clear\n- restart\n- exit\n')

    elif user_prompt in ['view-all','va'] :
        view_db(user_email, projects)

    elif user_prompt in ['view','v'] :
        if projects[user_email] :
            check_projects_db(user_email)
            view_db(user_email, projects[user_email]) #need test (err when viewing new user projects)

    elif user_prompt == 'create':
        project_info = project_temp()
        create_status = create_fund(user_email, project_info)

        if create_status :
            print(create_status)

    elif user_prompt == 'edit' :
        project_id = input(f"(EDIT) Project ID : ").strip().lower()

        edit_status = edit_delete(user_email, 'edit', project_id)
        
        if not edit_status :
            print("(EDIT) done.")
        else :
            print(f"\n(EDIT) {edit_status}")
        

    elif user_prompt == 'delete' :
        project_id = input(f"(DELETE) Project ID : ").strip().lower()
        delete_status = edit_delete(user_email, 'delete', project_id)

        if not delete_status :
            print("(DELETE) done.")
    
    elif user_prompt == 'search' :
        srch_date = input('(SEARCH dd-mm-yyyy) : ')
        if check_valid(srch_date, 'date'):
            res = search(srch_date)
            if res :
                print(f'- {len(res)} results found :\n')
                for r in res :
                    print(f'\tUser ({r[0].capitalize()}_{r[1].capitalize()}) : ProjectID ({r[2]})')
                print()
            else :
                print('No results')
        else :
            print('Invalid date formula')

    elif user_prompt in ['clear', 'c'] :
        os.system('clear')
    
    elif user_prompt in ['restart', 're'] :
        restart()

    elif user_prompt == '':
        pass
    else :
        print('Command Not Found')


#In Development
def admin_console():
    pass


@safe_exit
def user_prompt(user, mode):
    if user is False :
        return
    while True :
        if mode :
            prompt = input(colored(f'{user[1].capitalize()}@Crowd-Funding > ', 'yellow'))\
            .lower().strip()
        else :
            prompt = input(f'{user[1].capitalize()}@Crowd-Funding > ')\
            .lower().strip()

        if prompt in ['exit','e'] :
            print('Logout')
            break
        prompt_functions(user[0], prompt)


def intro(mode=None) :
    
    title = 'Crowd Funding App'
    dev = 'Developed By: Mohand Zaid (muhanadaleem@gmail.com)'
    help_msg = '(h)help to show commands!'
    if mode == 'colored':
        title = pyfiglet.figlet_format('Crowd Funding', font='slant')
        title = colored(title,'yellow')
        print(title)
        print(colored(dev, 'yellow'))
        print()
        print(colored(help_msg, 'yellow'))
        print()

        return
    
    print(f'\n{title}\n{dev}\n{help_msg}\n')
    print("Colored Mode Off\nrun 'pip install pyfiglet termcolor'\n")



def main():

    color_mode = True

    # print(banner)
    
    try :
        intro('colored')
    except :
        intro()
        color_mode = False


    while True :

        if color_mode :
            main_prompt = input(colored('Crowd-Funding > ', 'yellow')).lower().strip()
        else :
            main_prompt = input('Crowd-Funding > ').lower().strip()
        
        if main_prompt in ['help','h']:
            print("\n-(l)login\n-(r)register\n-(h)help\n-(c)clear\n-(f)fixdb\n-(re)restart\n-(e)exit\n")
        
        elif main_prompt in ['info', 'i'] :
            print(info)

        elif main_prompt in ['login','l'] :

            user_prompt(login(), color_mode)

        elif main_prompt in ['register', 'r'] :
            try:
                print('\nCrowd-Funding Registration\n')

                user_data = registration_temp()

                registration(user_data, user_data['confirm_pass'])
            except KeyboardInterrupt :
                print()

        elif main_prompt in ['exit','e'] :
            sys.exit()
        
        elif main_prompt in ['clear','c'] :
            os.system('clear')

        #Just for debuging
        elif main_prompt == 'vdb' :
            print(users)
        elif main_prompt == 'vdp' :
            print(projects)
        elif main_prompt in ['save','s'] :
            save_db(users, 'users.json')
            save_db(projects, 'projects.json')
        elif main_prompt in ['vu', 'view-users']:
            for email in users :
                u = users[email]['fname'].capitalize()+'-'+users[email]['lname'].capitalize()
                p = users[email]['password']
                print(f'\t<{u}> <{email}> <{p}>')
        elif main_prompt in ['d', 'debug'] :

            user_prompt(login(True), color_mode)

        elif main_prompt == '':
            pass
        elif main_prompt in ['fixdb', 'f'] :
            os.system('./db/fix_db.sh')
            print("\nrun 'restart' to reconnect db")

        elif main_prompt in ['restart', 're'] :
            restart()

        else :
            print('Command Not Found')

