people = ['Dr. Christopher Brooks', 'Dr. Kevyn Collins-Thompson', 'Dr. VG Vinod Vydiswaran', 'Dr. Daniel Romero']

def split_title_and_name(person):
    title = person.split()[0]
    lastname = person.split()[-1]
    return '{} {}'.format(title, lastname)

list(map(split_title_and_name, people))

# https://realpython.com/python-map-function/#:~:text=map()%20loops%20over%20the,in%20the%20original%20input%20iterable.&text=map()%20applies%20function%20to,yields%20transformed%20items%20on%20demand.