import json

from core.objects import User


def main():
    user_json = json.load(open("user.json"))
    user = User.model_validate(user_json)
    print(user)


if __name__ == '__main__':
    main()
