import re
def logs():

    with open("logdata.txt", "r") as file:
        logdata = file.read()

        pattern = """
        (?P<host>[0-9]*.[0-9]*.[0-9]*.[0-9]* )
        (\ -\ )
        (?P<user_name>[a-z0-9-]*)
        (\ \[)
        (?P<time>.*)
        (\]\ \")
        (?P<request>.*)
        (")
        """
        list = []
        for item in re.finditer(pattern, logdata, re.VERBOSE):
            list.append (item.groupdict())
        return list

print(len(logs()))