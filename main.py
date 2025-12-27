import discord
from SirDanBot import SirDan

sir_dan_intents = discord.Intents.default()
sir_dan_intents.message_content = True

sir_dan = SirDan( _intents = sir_dan_intents )
sir_dan.run( sir_dan.m_token, root_logger=True )
