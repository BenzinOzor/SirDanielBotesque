import discord
from discord.ext import commands
import json
import logging
from BeReal import BeReal
from IsThereAnyDeal.Client import IsThereAnyDeal
from datetime import date
from datetime import time


# "Constant" variables
CONFIG_FILE = 'config.json'

CFG_TOKEN = 'Token'


# ============================================================================
# SIR DANIEL BOTESQUE
# ============================================================================
class SirDan( commands.Bot ):
	m_token: str = ''
	m_log: logging.Logger = None

# FUNCTIONS ------------------------------------------------------------------
	def __init__( self, _intents ):
		super().__init__( command_prefix = "/", intents = _intents )
		self.m_log = logging.getLogger( "SDB - Sir Dan" )

		# Reading bot token from config file
		file = open( CONFIG_FILE )
		json_data: dict = json.load( file )
		self.m_token = json_data[ CFG_TOKEN ]

		self.m_bereal = BeReal()
		self.m_bereal.load_config( json_data )

		self.m_itad = IsThereAnyDeal()
		self.m_itad.load_config( json_data )

		file.close()
		self.save_bot_config()

	def save_bot_config( self ):
		with open( CONFIG_FILE, "w" ) as outfile:
			self.m_log.info( "Saving bot config...")
			bot_config = {}
			bot_config[ CFG_TOKEN ] = self.m_token
			self.m_bereal.save_config( bot_config )
			self.m_itad.save_config( bot_config )

			outfile.write( json.dumps( bot_config, sort_keys = False, indent = 4 ) )


# BEREAL ------------------------------------------------------------------
	def generate_next_bereal( self ):
		self.m_bereal.generate_next_bereal()
		self.save_bot_config()

	def bereal_set_channel( self, _channel_id: int ):
		self.m_log.info( f"New BeReal channel id: {_channel_id}")
		self.m_bereal.m_channel_id = _channel_id
		self.save_bot_config()

	def bereal_set_role( self, _role_id: int ):
		self.m_log.info( f"New BeReal role id: {_role_id}")
		self.m_bereal.m_role_id = _role_id
		self.save_bot_config()

	def bereal_set_min_time( self, _time: time ):
		self.m_log.info( f"New BeReal time lower bound: {_time.isoformat()}")
		self.m_bereal.m_min_time = _time
		self.save_bot_config()

	def bereal_set_max_time( self, _time: time ):
		self.m_log.info( f"New BeReal time upper bound: {_time.isoformat()}")
		self.m_bereal.m_max_time = _time
		self.save_bot_config()

	# ---------------------------------
	# Always on thread managing bereal calls and sending alert to the channel
	# ---------------------------------
	async def remain_legitimate_thread( self ):
		self.m_log.info( "Entering thread.")
		while True:
			if self.m_bereal.are_date_and_time_valid() == False:
				self.generate_next_bereal()

			await self.m_bereal.manage_bereal()
			bereal_channel = self.get_channel( self.m_bereal.m_channel_id )
			await bereal_channel.send( f"c'est l'heure du <@&{self.m_bereal.m_role_id}> ! :camera_with_flash:" )

			self.generate_next_bereal()


# EVENTS ---------------------------------------------------------------------
	async def on_ready( self ):
		self.m_log.info( f'Logged in as {self.user.display_name}.' )

		self.m_log.info( "Starting thread.")
		self.loop.create_task(self.remain_legitimate_thread() )

		await self.load_extension( "SDBCommands" )
		await self.load_extension( "SDBModCommands" )
# ============================================================================
