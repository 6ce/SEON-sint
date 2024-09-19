import json
from seon import SEON
from sys import argv

if __name__ == "__main__":
    if len(argv) < 3:
        print("Usage: python main.py SEARCH_TYPE SEARCH_QUERY")
        print("Example: python main.py email email@domain.org")
        print("Search Types: phone, email")
        exit()
    
    searcher = SEON()

    type = argv[1]
    query = "".join(argv[2::])

    if type.lower() == "phone":
        results = searcher.phone(query)
    elif type.lower() == "email":
        results = searcher.email(query)
    elif type.lower() == "file":
        fileType = argv[2]
        if fileType.lower() == "phone":
            results = searcher.phoneFile("tosearch.txt")
        elif fileType.lower() == "email":
            results = searcher.emailFile("tosearch.txt")
        else:
            print("Invalid file search type passed")
            print("Search Types: phone, email")
            exit()
        
        print("You can also view the results in 'search.json'")
    else:
        print("Invalid search type passed")
        print("Search Types: phone, email")
        exit()
    
    dumped = json.dumps(results, indent=4)
    print(f"Registered socials: {dumped}")
