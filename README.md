# Simple client server palindrome protocol aka paldcol

# Getting Started

  Ensure you have the following installed on your machines...
  
    Requirements:
        Python 2.7
        pip libraries socket, threading & json
        virtualenv (optional...somewhat)
        bash/*sh terminal
        admin priviliges on the listening server
        
        thats it for now....
        
# Running

    python server.py
    
then

    python client.py
    $ paldcol : help
    
            paldcol protocol usage:
            connect [ip] [port] : connects with a paldcol server listening on this ip, port
            echo [item] : prints out the supplied item command
            check [item] [item] .. : checks if the supplied items are palindromes, if yes stores them
            state [option]:
                    option == num  : return the number of palindromes found so far
                    option == list : returns a list of palindromes found so far
                    option == last : returns the last element that is a palindrome
            del [index]:
                    index >= 0  : deletes the palindrome at that specified location
                    index == -1 : deleted everything in the palindrome database
            help : prints usage
            term : terminates the current connection with a paldcol server
            exit : exits the paldcol cli
            
    $ paldcol : connect localhost 5555 # sets up a persistent connection 
    $ paldcol : once localhost 5555 del -1 # deletes everything in pal db, non persistent connection
    
to run tests, type

        python server.py --test
