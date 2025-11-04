from abc import ABC, abstractmethod
from typing import TypedDict


class CheckParams(TypedDict):
    user_type: str
    user_id: str
    resource_id: str
    resource_type: str
    action: str

class AddRelationParams(TypedDict):
    user_type: str
    user_id: str
    resource_id: str
    resource_type: str
    action: str


class CheckResponse(TypedDict):
    allowed: bool


class IFGAAuthorizer(ABC):
    @abstractmethod
    def check(self, params: CheckParams) -> CheckResponse:
        pass

    @abstractmethod
    def batch_check(self, ):
        pass

    @abstractmethod
    def add_relation(self, AddRelationParams):
        pass

    @abstractmethod
    def delete_relation(self):
        pass
