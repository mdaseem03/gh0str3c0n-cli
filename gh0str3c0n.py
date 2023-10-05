from concurrent.futures import ThreadPoolExecutor
from pwn import *
from termcolor import *
import socket
import sys


def banner():

    print(
    colored('''
   ______      ____       __  ____ _____      ____      
  / ____/ /_  / __ \_____/ /_/ __ \__  /_____/ __ \____ 
 / / __/ __ \/ / / / ___/ __/ /_/ //_ </ ___/ / / / __ \\''','magenta'),colored('''
/ /_/ / / / / /_/ (__  ) /_/ _, _/__/ / /__/ /_/ / / / /
\____/_/ /_/\____/____/\__/_/ |_/____/\___/\____/_/ /_/    v1.0''','cyan'))
    
    print(colored("\n\n💻 CLI Version: mdaseem03  (https://github.com/mdaseem03/gh0str3c0n-cli)",'blue'))
    print(colored("📊 GUI Version: karthi-the-hacker (https://github.com/karthi-the-hacker/Gh0stR3c0n) ",'blue'))
    print(colored("🏢 Company    : Cappricio Securities (https://cappriciosec.com/)",'green'))

    print("_"*90)
    print('\n')


def intro():
    try:
        print(colored('Hey Hacker 👑 .....','white',attrs=['bold']))
        print(colored('\n⚠️ Use this tool for ethical purposes only! Author doesn\'t supports any kind of unethical activities','yellow'))
        print("Let's start our recon 🚀\n")
    except:
        print(colored("\nExiting ....",'red'))
        print(colored("See you again 👋",'white',attrs=['bold']))
        sys.exit()

def scope():       
    domain_names = []

    try:   
        domain = input("🕸️ Enter domain name: ").strip().lower()
        if domain == "":
            print("❌ Invalid Domain")
        else:
            try:
                ip = socket.gethostbyname(domain)
                domain_names.append(domain)
                print(f"✔️ {domain} added to scope")
            except Exception:
                print(f"❌ Invalid domain {domain}")

        ch = input("\nDo you want to add more domains to the scope (y/n): ").lower().strip()

        while True:
            if ch == 'y':
                while True:   
                    print("\nEnter domain names (or",colored('!q','red',attrs=['bold']),"to exit):\n")
                    while True:   
                        domain = input(">> ").strip().lower()
                        if domain == "":
                            print("❌ Invalid Domain")
                        elif domain == "!q":
                            break
                        else:
                            try:
                                ip = socket.gethostbyname(domain)
                                domain_names.append(domain)
                                print(f"✔️ {domain} added to scope")
                            except Exception:
                                print(f"❌ Invalid domain {domain}")
                    break 
    
                
            elif ch == 'n':
                break  # Exit the outer loop if the user doesn't want to add more domains
            else:
                ch = input("😓 Invalid choice. Please enter 'y' or 'n': ").lower().strip()
                continue
            break

    except:
        print('')            

        # Write the domain names to the 'scope.txt' file
    with open(f'recon/{project}/scope.txt', 'w') as file:
        for domain in domain_names:
            file.write(domain + '\n')

    



def url_create():
    # Initialize an empty list to store URLs
    urls = []
    try: 
        # Read domain and port information from a text file
        with open(f"recon/{project}/naabu.txt", "r") as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if not line:
                    continue  # Skip empty lines
                domain, port = line.split(":")
                port = int(port)  # Convert port to an integer

                # List of ports and corresponding protocols
                ports = {
                    80: "http",
                    443: "https",
                    2000: "http"
                }

                # Check if the port is in the dictionary
                if port in ports:
                    protocol = ports[port]
                    url = f"{protocol}://{domain}:{port}"
                    urls.append(url)

        # Save the generated URLs to "url.txt"
        with open(f"recon/{project}/url.txt", "w") as output_file:
            for url in urls:
                output_file.write(url + "\n")
    except():
        return colored("Insufficient data to recon",'red')

#subfinder
def run_subfinder():
    subfinder_command = f'subfinder -dL recon/{project}/scope.txt -o recon/{project}/subfinder.txt'
    
    with open(os.devnull, 'w') as null_file:
        try:
            subprocess.run(subfinder_command, shell=True, check=True, stdout=null_file, stderr=null_file)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running Subfinder: {e}", 'red'))

def subfinder():
    
    with log.progress(f' Subfinder: ') as p:
       with ThreadPoolExecutor(max_workers=1) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_subfinder)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
        
        
       p.success(colored("Completed", 'green', attrs=['bold']))

#sort all subdomains
def sort():
    
    sorting = f'cat recon/{project}/*.txt | sort -u >> recon/{project}/all.txt'
    os.system(sorting)



#naabu

def run_naabu():
    naabu_cmd = f'naabu -list recon/{project}/all.txt -o recon/{project}/naabu.txt'
    
    with open(os.devnull, 'w') as null_file:
        try:
            subprocess.run(naabu_cmd, shell=True, check=True, stdout=null_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running Naabu", 'red'))

def naabu():
    with log.progress(f' Naabu: ') as p:
       with ThreadPoolExecutor(max_workers=1) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_naabu)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
       p.success(colored("Completed", 'green', attrs=['bold']))
        

def run_m4skup():
    m4skup_cmd = f'bash tools/m4skup/m4skup {project}'
    with open(os.devnull, 'w') as null_file:
        try:
            subprocess.run(m4skup_cmd, shell=True, check=True, stdout=null_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running M4skup", 'red'))

def m4skup():
    with log.progress(f' M4skup: ') as p:
       with ThreadPoolExecutor(max_workers=1) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_m4skup)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
       p.success(colored("Completed", 'green', attrs=['bold']))

def run_gau():
    gau_cmd = f'cat recon/{project}/url.txt | gau | sort -u >> recon/{project}/gau.txt'
    with open(os.devnull, 'w') as null_file:
        try:
            subprocess.run(gau_cmd, shell=True, check=True, stdout=null_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running Gau", 'red'))

def gau():
    with log.progress(f' Get All Urls(Gau): ') as p:
       with ThreadPoolExecutor(max_workers=1) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_gau)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
       p.success(colored("Completed", 'green', attrs=['bold']))

def run_waybackurls():
    waybackurls_cmd = f'cat recon/{project}/url.txt | waybackurls | sort -u >> recon/{project}/waybackurls.txt'
    with open(os.devnull, 'w') as null_file:
        try:
            subprocess.run(waybackurls_cmd, shell=True, check=True, stdout=null_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running Waybackurls", 'red'))

def waybackurls():
    with log.progress(f' Waybackurls: ') as p:
       with ThreadPoolExecutor(max_workers=1) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_waybackurls)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
       p.success(colored("Completed", 'green', attrs=['bold']))

def run_dirsearch():
    dirsearch_cmd = f'python3 tools/dirsearch/dirsearch.py -l recon/{project}/url.txt -e php,asp,aspx,net,js,cs,php2,php3,php4,php5,php6,php7,jsp,java,python,yaml,yml,config,conf,htaccess,htpasswd,shtml -o recon/{project}/dirse.txt'
    with open(os.devnull, 'w') as null_file:
        try:
            subprocess.run(dirsearch_cmd, shell=True, check=True, stdout=null_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running Dirsearch", 'red'))

def dirsearch():
    with log.progress(f' Dirsearch: ') as p:
       with ThreadPoolExecutor(max_workers=1) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_dirsearch)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
       p.success(colored("Completed", 'green', attrs=['bold']))

def run_amass():
    amass_cmd = f'amass enum -df recon/{project}/scope.txt -o recon/{project}/amass.txt'
    with open(os.devnull, 'w') as null_file:
        try:
            subprocess.run(amass_cmd, shell=True, check=True, stdout=null_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running Amass", 'red'))

def amass():
    with log.progress(f' Amass: ') as p:
       with ThreadPoolExecutor(max_workers=1) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_amass)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
       p.success(colored("Completed", 'green', attrs=['bold']))

def run_paramspi():
    paramspi_cmd = f'cat recon/{project}/all.txt | xargs -n1 -P4 python3 tools/ParamSpider/paramspider.py -d >> recon/{project}/paramspider.txt'
    with open(os.devnull, 'w') as null_file:
        try:
            subprocess.run(paramspi_cmd, shell=True, check=True, stdout=null_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running ParamSpider", 'red'))

def paramspi():
    with log.progress(f' ParamSpider: ') as p:
       with ThreadPoolExecutor(max_workers=1) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_paramspi)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
       p.success(colored("Completed", 'green', attrs=['bold']))

def run_gf():

    commands = [
        f'cat recon/{project}/paramspider.txt | gf xss > recon/{project}/xss.txt',
        f'cat recon/{project}/paramspider.txt | gf sqli > recon/{project}/sqli.txt',
        f'cat recon/{project}/paramspider.txt | gf ssrf > recon/{project}/ssrf.txt',
        f'cat recon/{project}/paramspider.txt | gf ssti > recon/{project}/ssti.txt',
        f'cat recon/{project}/paramspider.txt | gf idor > recon/{project}/idor.txt',
        f'cat recon/{project}/paramspider.txt | gf lfi > recon/{project}/lfi.txt',
        f'cat recon/{project}/paramspider.txt | gf rce > recon/{project}/rce.txt',
        f'cat recon/{project}/paramspider.txt | gf redirect > recon/{project}/redirect.txt'
    ]

    for cmd in commands:
        try:
            with open(os.devnull, 'w') as null_file:
                subprocess.run(cmd, shell=True, check=True, stdout=null_file, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(colored(f"Error running gf", 'red'))

def gf():
    with log.progress(f' Pattern Matching for (XSS, SQLI, SSRF, SSTI, IDOR, LFI, RCE, and Open Redirect): ') as p:
        with ThreadPoolExecutor(max_workers=8) as executor:
            p.status(colored("Running.",'yellow', attrs=['bold']))
            futures = [executor.submit(run_gf)]
            try:
                for future in futures:
                    future.result()
            except:
                p.failure(colored("Skipped.",'red', attrs=['bold']))
        p.success(colored("Completed", 'green', attrs=['bold']))


if __name__ == "__main__":
    try:
    
        print("\033c\033[3J\033[2J\033[0m\033[H")
        banner()

        intro()
        try:
            project = input("📁 Enter Project Name:  ").strip() #folder name
            os.system(f'mkdir -p recon/{project}/')
            pd = os.getcwd()
            print(f'\nOutput ---> {pd}/recon/{project}\n')
        except:
            print('')
        

        scope()
        file_path = f'recon/{project}/scope.txt'

        def is_file_empty(file_path):
            try:
                with open(file_path, 'r') as file:
                    return not bool(file.read())
            except FileNotFoundError:
                return True

        if is_file_empty(file_path):
            print("No domain added")
            print(colored("Insufficient data to recon",'red'))
            print(colored("\nExiting ....",'red'))
            print(colored("See you again 👋",'white',attrs=['bold']))
            
        else:
            print(" \nScope:")
            with open(f'recon/{project}/scope.txt', 'r') as file:
            # Read and print each line
                for line in file:
                    print("-",end=' ')
                    print(line.strip())
            print('\n')
            
            print(colored("GRAB YOUR COFFEE ☕ AND WAIT FOR RECON TO COMPLETE",'white',attrs=['bold']))
            print('\n')

            try:
                subfinder()
                print('\n')
            except:
                print('')
            
            sort()

            try:
                naabu()
                print('\n')
            except:
                print('')

            try:
                m4skup()
                print('\n')
            except:
                print('')

            try:
                url_create()
            except:
                print(colored("Insufficient data to recon",'red'))
                print('\n')
                sys.exit()

            try:
                gau()
                print('\n')
            except:
                print('')

            try:
                waybackurls()
                print('\n')
            except:
                print('')

            try:
                paramspi()
                print('\n')
            except:
                print('')

            try:
                gf()
                print('\n')
            except:
                print('')

            
            try:
                print("Do you want to run",colored("amass",'red',attrs=['bold']),"and",colored("dirsearch",'red',attrs=['bold'])," ?")
                print("[",colored("1",'green',attrs=['bold']),"] Run amass only")
                print("[",colored("2",'green',attrs=['bold']),"] Run dirsearch only")
                print("[",colored("3",'yellow',attrs=['bold']),"] Run both")
                print("[",colored("4",'red',attrs=['bold']),"] No, finish Recon!")
                while True:
                    inp = input(">> ").strip()

                    if inp == '1':
                        try:
                            amass()
                            break
                        except:
                            break
                    elif inp == '2':
                        try:
                            dirsearch()
                            break
                        except:
                            break
                    elif inp == '3':
                        try:
                            amass()
                            print('\n')
                        except:
                            print('')
                        try:
                            dirsearch()
                            break
                        except:
                            break
                    elif inp == '4':
                        break
                    else:
                        print("Invalid Option 😓")
                        continue

                print(colored("\n\nRECON COMPLETED....🔍 ",'white',attrs=['bold']))
            
            except:
                print(colored("\nExiting ....",'red'))
                print(colored("\n\nRECON COMPLETED....🔍 ",'white',attrs=['bold']))
                sys.exit()  # Stop program execution

        
    except:
        print(colored("\nExiting ....",'red'))
        print(colored("See you again 👋",'white',attrs=['bold']))
        sys.exit()  # Stop program execution
