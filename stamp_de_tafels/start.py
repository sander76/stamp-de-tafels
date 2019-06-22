import asyncio
import random

import questionary
from prompt_toolkit import prompt
from prompt_toolkit.eventloop.defaults import use_asyncio_event_loop
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style

use_asyncio_event_loop()

jumbo = r"""
  _____ _                              _        _______     __     _     
 / ____| |                            | |      |__   __|   / _|   | |    
| (___ | |_ __ _ _ __ ___  _ __     __| | ___     | | __ _| |_ ___| |___ 
 \___ \| __/ _` | '_ ` _ \| '_ \   / _` |/ _ \    | |/ _` |  _/ _ \ / __|
 ____) | || (_| | | | | | | |_) | | (_| |  __/    | | (_| | ||  __/ \__ \
|_____/ \__\__,_|_| |_| |_| .__/   \__,_|\___|    |_|\__,_|_| \___|_|___/
                          | |                                            
                          |_|                                            

"""

style = Style.from_dict({"ok": "bg:green", "fail": "bg:red"})


def print_ok(text="OK !"):
    print_formatted_text(HTML("<ok>{}</ok>".format(text)), style=style)


def print_fail(text="Jammer !"):
    print_formatted_text(HTML("<fail>{}</fail>".format(text)), style=style)


async def calc_question(verm=None, tables=None):
    if verm is None:
        verm = 10
    if tables is None:
        tables = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    while True:
        try:
            first = random.randrange(0, verm)
            second = random.choice(tables)
            answer = first * second

            result = await prompt("{}x{}=".format(first, second), async_=True)

            if result == str(answer):
                print_ok()
            else:
                print_fail()
                print("Het goede antwoord is : {}".format(answer))
            print("")
        except KeyboardInterrupt:
            result = await prompt("Stoppen ? [y/n]", async_=True)
            if result == "y":
                return


loop = asyncio.get_event_loop()


def start():
    question = questionary.checkbox(
        "Selecteer de tafels die je wilt oefenen:",
        choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    )
    tafels = question.ask()
    tafels = [int(tafel) for tafel in tafels]
    print(tafels)
    return tafels


def main():
    print_ok(text=jumbo)

    with patch_stdout():
        tafels = start()

        loop.run_until_complete(calc_question(tables=tafels))

        print("bye bye")


if __name__ == "__main__":
    main()
