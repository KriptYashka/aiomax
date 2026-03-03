import json

from core.events.message import EventMessageCreated


def main():
    with open("fixtures/message_created.json") as f:
        data = json.load(f)
        event = EventMessageCreated.model_validate(data)
        print(event, sep="\n")


if __name__ == '__main__':
    main()
