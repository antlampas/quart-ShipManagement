from abc import ABC, abstractmethod

class Editable(ABC):
    @abstractmethod
    def edit(self,attributes:dict):
        pass

class Addable(ABC):
    @abstractmethod
    def add(self,obj:Editable):
        pass
