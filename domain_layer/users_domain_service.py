from ExceptJohn.domain_object import except_john


@dataclass
class User:
    id: str
    firstname: str
    lastname: str
    email: str


class UsersDomainServices:
    """
    user_repo: Resource = Repositories.get('User')
    product_repo: Resource = Repositories.get('Product')

    user: User = user_repo.get(id)
    """

    def get(self, id):
        # TODO: implement users domain service
        return 0
