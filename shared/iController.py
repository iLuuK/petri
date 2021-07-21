from abc import abstractmethod
from shared.action import Action


class IController:
    @abstractmethod
    def performAction(self, action: Action):
        ...

