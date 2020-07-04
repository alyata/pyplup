# Pyplup
[Pokémon Showdown](https://pokemonshowdown.com/) battle API in python.

## Overview
Pyplup is still in a very early stage of development: as of this commit, it can login and accept battle invites, to which it will select the Showdown 'default' battle option, which is the first possible move. This is currently just a proof of concept.

The __primary goal__ is to abstract the details of the [Showdown protocol](https://github.com/smogon/pokemon-showdown/blob/master/PROTOCOL.md) from the user, and instead have users interact with a battle interface which contains information about the current state as well as the history of the battle. This makes it very easy to use for machine learning, which is what I intended Pyplup for.

Pokémon Showdown uses websockets to exchange messages with the client. The low-level API is designed to execute procedures in response to received messages. A __secondary goal__ is to allow the user to override some of the response functionality to suit their needs. For example, the appropriate response to the end of a battle might to ask for feedback from the user (in order to help train the underlying ML algorithm, perhaps).

## Example Usage
The API must be used in an async function, and therefore requires the `asyncio` built-in library. Additionally, the `Showdown` class must be imported as well:
```python
import asyncio
from src.showdown import Showdown
```
For example, the following async function initializes the API for usage:

_Note: the API currently does not permit interaction..._
```python
async def main():
    # initalize the API
    show = Showdown("username", "password")
    # open a connection to the server
    await show.connect()
    # start the processing task
    task = asyncio.create_task(show.run())

    #TODO: interaction with the API...

    #wait for bot to terminate itself,
    #which should only happen if a fatal error is encountered
    await task
```
The async function must then be run by `asyncio` as well:
```python
if __name__ == "__main__":
    asyncio.run(main())
```
The above code is given in `example_run.py`. Running the code will give you your very own (albeit rather stupid) bot, which you can challenge on Pokemon Showdown. It will only accept Generation 8 random battle invites, and will not respond to any messages you send to it.  

## Dependencies
- Python 3.7.6
- Python libraries:
  - websockets 8.1
  - requests 2.24.0
