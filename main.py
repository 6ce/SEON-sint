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
        if not query.startswith("+"):
            query = "+1" + query
        query = query.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        results = searcher.phone(query)
    elif type.lower() == "email":
        results = searcher.email(query)
    else:
        print("Invalid search type passed")
        print("Search Types: phone, email")
        exit()
    
    print(json.dumps(results, indent=4))
