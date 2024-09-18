# SEON-sint
Utilizes the [SEON](https://seon.io) API to fetch registered accounts on a phone number or email

# Installation
1. Install [Python](https://python.org)
2. Download the repository as a zip file and unzip it
3. Open a command terminal in the repository's directory [like so](https://streamable.com/v8ysk8)
4. Run the command `pip install requests`
5. Create an account @ https://seon.io (or log in)
6. Copy the cookie from your browser called "seon-refresh"
7. Open the file 'config.json' in your installed directory
8. Input the copied cookie inside the empty quotation marks next to "session"
9. You'll now be able to run the usage commands

# Usage
- Supported search types: phone, email

`python main.py SEARCH_TYPE SEARCH_QUERY`

# Example Usage
`python main.py phone 1234567890`

`python main.py email email@domain.tld`
