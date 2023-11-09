from datetime import datetime

async def WhatTimeIs():
    Time = datetime.now()
    return f"Now is {Time.hour}:{Time.minute} of {Time.day}/{Time.month}/{Time.year}"

async def CreateAlarm():
    return "Alarm created"

async def RemoveAlarm():
    return "Alarm removed"

async def SendMessage():
    return "Message sent"

async def TellNews():
    return "News"

async def OrderFood():
    return "Food ordered"

Commands = [
    {
        "name": "What time is?",
        "run": WhatTimeIs
    },
    {
        "name": "Create an alarm",
        "run": CreateAlarm,
    },
    {
        "name": "Send a message",
        "run": SendMessage,
    },
    {
        "name": "Tell me the news of the day",
        "run": TellNews,
    },
    {
        "name": "Order food",
        "run": OrderFood,
    },
]

def GetCommands():
    return Commands

async def RunCommand(commandName: str):
    CMDS = GetCommands()
    for Command in CMDS:
        if Command["name"] == commandName:
            return await Command["run"]()