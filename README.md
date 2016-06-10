### express-db-address-book
The parse.py script parses a Crestron RoomView Express database and output a Crestron Toolbox Address Book file

Example invocation is 

    python parse.py --db RoomviewDatabase.rve --output ShinyNewAddressBook

the *--db* flag is required, *--output* is optional and (if omitted) will output to the file *ServiceCenterAddressBook.xadr*
