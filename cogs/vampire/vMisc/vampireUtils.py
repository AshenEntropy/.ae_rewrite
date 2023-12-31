import sqlite3
from os import path
from zenlog import log
from discord import Embed
from random import randint

import misc.utils.yamlUtils as yU
import misc.config.mainConfig as mC


async def writeCharacterName(interaction, character_name) -> bool:
    targetDB = f'cogs//vampire//characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite'

    log.debug(f'> Checking if [ `{targetDB}` ] exists')
    if not path.exists(targetDB):
        log.warn(f'*> Database [ `{targetDB}` ] does not exist')
        await interaction.response.send_message(embed=Embed(
            title='Database Error', color=mC.embed_colors["red"],
            description=f'[ `{character_name}` ] Does Not Exist.. \n\n {mC.ISSUE_CONTACT}'), ephemeral=True)
        return False
    else:
        log.debug(f'> Successful Connection to [ `{targetDB}` ]')

    with sqlite3.connect(targetDB) as db:
        char_owner_id = db.cursor().execute('SELECT userID FROM ownerInfo').fetchone()[0]
        if char_owner_id != interaction.user.id:  # ? If interaction user doesn't own the character
            await interaction.response.send_message(f'You don\'t own {character_name}', ephemeral=True)
            return False

        targetCache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
        await yU.cacheClear(targetCache)
        await yU.cacheWrite(targetCache, dataInput={'characterName': f'{character_name}'})

    return True


async def getCharacterName(interaction) -> str:
    target_cache = f'cogs/vampire/characters/{str(interaction.user.id)}/{str(interaction.user.id)}.yaml'
    use_data: dict = {}
    use_data.update(await yU.cacheRead(f'{target_cache}'))
    character_name: str = str(use_data['characterName'])
    return character_name


async def rouseCheck(interaction, targetcharacter) -> str:
    try:
        with sqlite3.connect(f'cogs//vampire//characters//{str(interaction.user.id)}//{targetcharacter}//{targetcharacter}.sqlite') as db:
            cursor = db.cursor()
            hunger = int(cursor.execute('SELECT hunger from charInfo').fetchone()[0])
            rouse_num_result: int = randint(1, 10)

            if hunger >= 5:
                # TODO: HANDLE FRENZY STUFF
                return 'Frenzy'  # * Hunger Frenzy, No Hunger Gain Too High Already

            elif rouse_num_result >= 6:
                return 'Pass'  # * No Hunger Gain

            elif rouse_num_result <= 5:
                cursor.execute('UPDATE charInfo SET hunger=?', (str(int(hunger + 1))))
                db.commit()
                return 'Fail'  # * Hunger Gain
    except sqlite3.Error as e:
        log.error(f'rouseCheck | SQLITE3 ERROR | {e}')

