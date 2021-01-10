""""
Entry point for RBAC system
This is kept separate from controller because this will handle all inits and callings and will not worry about the logic
for initialisation of multiple parts
Idea is to separate knowledge of all other modules, meaning, only this will know about controller and controller will
further know about all different modules existing and module/entities will know nothing/less about each other so we can
enforce more cohesion and less coupling
"""

import traceback

from controller import Controller
from exceptions.base import CustomExceptionBase

try:
    controller = Controller()
    controller.run()
except CustomExceptionBase as exc:
    print(f'Exception occurred - {exc}. Traceback - {traceback.format_exc(5)}')
except KeyboardInterrupt:
    print(f'Make up for your mind for god"s sake')
