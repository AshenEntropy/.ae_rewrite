from discord.ext import commands
from discord import app_commands
from discord.ui import View
import discord

from zenlog import log
import sqlite3
import os

from misc import ashen_utils as au

selection_embed = (discord.Embed(title='Select',
                                 description='',
                                 color=au.embed_colors["purple"]))

note_embed = (discord.Embed(title='Note',
                            description='',
                            color=au.embed_colors["dark_yellow"]))

selectionOptions = [
    discord.SelectOption(
        label='Make', value='make', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Read', value='read', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Edit', value='edit', emoji='<:snek:785811903938953227>'
    ),
    discord.SelectOption(
        label='Delete', value='delete', emoji='<:snek:785811903938953227>'
    )]


class NoteView(View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Left', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def left_button_callback(self, interaction, button):
        await interaction.response.edit_message(embed=None, view=None)

    @discord.ui.button(label='Exit', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=0)
    async def exit_button_callback(self, interaction, button):
        await interaction.response.edit_message(embed=None, view=None)

    @discord.ui.button(label='Right', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def right_button_callback(self, interaction, button):
        await interaction.response.edit_message(embed=None, view=None)

    @discord.ui.button(label='Edit', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.green, row=1)
    async def edit_button_callback(self, interaction, button):
        await interaction.response.edit_message(embed=None, view=None)

    @discord.ui.button(label='Exit', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def exittwo_button_callback(self, interaction, button):
        await interaction.response.edit_message(embed=None, view=None)

    @discord.ui.button(label='Delete', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def delete_button_callback(self, interaction, button):
        await interaction.response.edit_message(embed=None, view=None)


class EXONOTES(commands.Cog):
    def __init__(self, CLIENT):
        self.CLIENT = CLIENT

    @app_commands.command(name="note_make", description="exoNote Make")
    @app_commands.describe(title='Note Title')
    @app_commands.describe(handle='Note Handle')
    @app_commands.describe(tags='Note Tags')
    @app_commands.describe(content='Note Content')
    async def note_make(self, interaction: discord.Interaction, title: str, handle: str, tags: str, content: str):
        note_embed.clear_fields()

        note_embed.add_field(name='Title:', value=f'{title}', inline=True)
        note_embed.add_field(name='Handle:', value=f'{handle}', inline=True)
        note_embed.add_field(name='Tags:', value=f'{tags}', inline=True)
        note_embed.add_field(name='Content:', value=f'{content}', inline=True)
        await interaction.response.send_message(embed=note_embed, view=NoteView(self.CLIENT))

    @app_commands.command(name="note_read", description="exoNote Read")
    @app_commands.describe(handle='Note Handle')
    async def note_read(self, interaction: discord.Interaction, handle: str):
        match handle:
            case 'all':
                # ! Shows all notes of the user, have a | <- Del Edi -> | menu
                return
            case 'test':
                # ! Just to test/debug the command
                note_embed.clear_fields()

                title, tags, content = 1, 1, 1
                note_embed.add_field(name='Title:', value=f'{title}', inline=True)
                note_embed.add_field(name='Handle:', value=f'{handle}', inline=True)
                note_embed.add_field(name='Tags:', value=f'{tags}', inline=True)
                note_embed.add_field(name='Content:', value=f'{content}', inline=True)
                await interaction.response.send_message(embed=note_embed, view=NoteView(self.CLIENT))
            case _:
                # ! use HANDLE
                return


async def setup(CLIENT):
    await CLIENT.add_cog(EXONOTES(CLIENT))
    log.info('> exoNotes Loaded')