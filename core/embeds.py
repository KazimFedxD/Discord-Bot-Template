import random
from typing import Optional
from discord import Embed, Color
from discord.utils import utcnow


class CustomEmbed:
    def __init__(
        self,
        footer: Optional[str|list[str]] = None,
        include_timestamp: bool = True,
    ):
        self.footer = footer
        self.include_timestamp = include_timestamp
    
    def embed(self, title:str, description:str, color:Optional[str]="random", author:Optional[str]=None, footer:Optional[str]=None, image:Optional[str]=None):
        """Creates A Embed

        Args:
            title (str): Title Of The Embed
            description (str): Body Of The Embed
            color (Optional[str], optional): Color Of Embed. Defaults to "random".
            author (Optional[str], optional): Name Of Author Of Embed. Defaults to None.
            footer (Optional[str], optional): Footer Of Embed. Defaults to Provided In Init.
            image (Optional[str], optional): Image Attached To Embed. Defaults to None.

        Returns:
            Embed: Embed Object Created Using The Provided Arguments
        """
        
        
        colorvalue = getattr(Color, color.lower(), None) if color else None
        embed = Embed(
            title=title,
            description=description,
            color=colorvalue() if colorvalue else None
        )
        if self.include_timestamp:
            embed.timestamp = utcnow()
        if author:
            embed.set_author(name=author)
        if footer:
            embed.set_footer(text=footer)
        else:
            if self.footer:
                if isinstance(self.footer, list):
                    embed.set_footer(text=random.choice(self.footer))
                else:
                    embed.set_footer(text=self.footer)
        return embed
    
    def error(self, title:str, description:str, author:Optional[str]=None, footer:Optional[str]=None, image:Optional[str]=None):
        """Creates A Error Embed

        Args:
            title (str): Title Of The Embed
            description (str): Body Of The Embed
            author (Optional[str], optional): Name Of Author Of Embed. Defaults to None.
            footer (Optional[str], optional): Footer Of Embed. Defaults to Provided In Init.
            image (Optional[str], optional): Image Attached To Embed. Defaults to None.

        Returns:
            Embed: Embed Object Created Using The Provided Arguments
        """
        embed = Embed(
            title=title,
            description=description,
            color=Color.red()
        )
        if self.include_timestamp:
            embed.timestamp = utcnow()
        if author:
            embed.set_author(name=author)
        if footer:
            embed.set_footer(text=footer)
        elif self.footer:
            if isinstance(self.footer, list):
                embed.set_footer(text=random.choice(self.footer))
            else:
                embed.set_footer(text=self.footer)
        return embed
    
    def success(self, title:str, description:str, author:Optional[str]=None, footer:Optional[str]=None, image:Optional[str]=None):
        """Creates A Success Embed

        Args:
            title (str): Title Of The Embed
            description (str): Body Of The Embed
            author (Optional[str], optional): Name Of Author Of Embed. Defaults to None.
            footer (Optional[str], optional): Footer Of Embed. Defaults to Provided In Init.
            image (Optional[str], optional): Image Attached To Embed. Defaults to None.

        Returns:
            Embed: Embed Object Created Using The Provided Arguments
        """
        embed = Embed(
            title=title,
            description=description,
            color=Color.green()
        )
        if self.include_timestamp:
            embed.timestamp = utcnow()
        if author:
            embed.set_author(name=author)
        if footer:
            embed.set_footer(text=footer)
        elif self.footer:
            if isinstance(self.footer, list):
                embed.set_footer(text=random.choice(self.footer))
            else:
                embed.set_footer(text=self.footer)
        return embed
    
    def warning(self, title:str, description:str, author:Optional[str]=None, footer:Optional[str]=None, image:Optional[str]=None):
        """Creates A Warning Embed

        Args:
            title (str): Title Of The Embed
            description (str): Body Of The Embed
            author (Optional[str], optional): Name Of Author Of Embed. Defaults to None.
            footer (Optional[str], optional): Footer Of Embed. Defaults to Provided In Init.
            image (Optional[str], optional): Image Attached To Embed. Defaults to None.

        Returns:
            Embed: Embed Object Created Using The Provided Arguments
        """
        embed = Embed(
            title=title,
            description=description,
            color=Color.orange()
        )
        if self.include_timestamp:
            embed.timestamp = utcnow()
        if author:
            embed.set_author(name=author)
        if footer:
            embed.set_footer(text=footer)
        elif self.footer:
            if isinstance(self.footer, list):
                embed.set_footer(text=random.choice(self.footer))
            else:
                embed.set_footer(text=self.footer)
        return embed
    
    def info(self, title:str, description:str, author:Optional[str]=None, footer:Optional[str]=None, image:Optional[str]=None):
        """Creates A Info Embed

        Args:
            title (str): Title Of The Embed
            description (str): Body Of The Embed
            author (Optional[str], optional): Name Of Author Of Embed. Defaults to None.
            footer (Optional[str], optional): Footer Of Embed. Defaults to Provided In Init.
            image (Optional[str], optional): Image Attached To Embed. Defaults to None.

        Returns:
            Embed: Embed Object Created Using The Provided Arguments
        """
        embed = Embed(
            title=title,
            description=description,
            color=Color.blue()
        )
        if self.include_timestamp:
            embed.timestamp = utcnow()
        if author:
            embed.set_author(name=author)
        if footer:
            embed.set_footer(text=footer)
        elif self.footer:
            if isinstance(self.footer, list):
                embed.set_footer(text=random.choice(self.footer))
            else:
                embed.set_footer(text=self.footer)
        return embed
    
        
