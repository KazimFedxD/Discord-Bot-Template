from typing import Awaitable, Callable
from discord import Interaction
from discord.app_commands import Choice

def make_autocomplete(*args: str) -> Callable[[Interaction, str], Awaitable[list[Choice[str]]]]:
    """
    Create an autocomplete function for the given arguments
    Args:
        *args (str): Options for the autocomplete

    returns:
        A function that can be put in @discord.app_commands.autocomplete
    Usage:
        @app_commands.autocomplete(choice=make_autocomplete("heads", "tails"))
        @app_commands.command(name="coinflip")
        async def command(self, interaction, choice:str):
        """
        
    
    
    choices = [Choice(name=arg, value=arg) for arg in args]
    if len(choices) > 25:
        raise ValueError("You can only have a maximum of 25 choices")
    async def _autocomplete(interaction:Interaction, current:str) -> list[Choice[str]]:
        return choices
    return _autocomplete

