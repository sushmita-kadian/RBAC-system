# RBAC-system

### HOW TO:
python main.py

Initially you will be logged in as admin user


### How Role works:
* Role is dependent on three action levels DELETE, WRITE and READ
* Role entity include two things: ***role name*** and against every action level a boolean flag
  which says whether this access level is given to user or not
* ***role name*** looks like a 3 digit binary like *011*. In a ***role name*** the most
  significant bit decides ***DELETE ACCESS***, next significant bit decides ***WRITE ACCESS***,
  and the least significant bit decides ***READ ACCESS**
* Initially 3 random roles are created out of 8 possibilities 

### HOW USER WORKS:
* Enter `0`(numberical zero) for help on any user. It will list all possible actions
* User as of now can be of only two types: an admin and a normal user
* An admin user have all roles created in the system
* An admin user have following functionalities
```sh
            0 -> HELP
            1 -> Login as another user
            2 -> View all roles
            3 -> Create a new user
            4 -> Create a new role
            5 -> Edit an existing role
            6 -> Delete an existing role
            7 -> View user request
            8 -> Delete user
            9 -> List all users
            10 -> Assign a role to a user
```

* A normal user have following functionalities
```sh
            0 -> HELP
            1 -> Login as another user
            2 -> View all roles
            3 -> Request new role
            4 -> View my roles
```

***NOTE***

* Deleting an existing role is not supported as now
* While listing all users, admin user is not listed
* Editing an existing role will change it's *role name*