import exec

def main():
    diregex = input("enter diregex: ")
    command = ''
    line = input("enter command: ")
    while line != '':
        command += line + '\n'
        line = input("enter command: ")

    exec.test(diregex, command)




if __name__ == "__main__":
    # execute only if run as a script
    main()
