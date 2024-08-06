import discord
from discord.ext import commands
from SirDanBot import SirDan
import logging
# testing
import random

# ============================================================================
# COMMANDS
# ============================================================================
class Commands( commands.Cog ):
	def __init__( self, _bot: commands.Bot ):
		self.bot = _bot

	# ---------------------------------
	# Simple test command
	# ---------------------------------
	@commands.command()
	async def ping( self, ctx ):
		await ctx.send( "pong" )

	# ---------------------------------
	# Generate a Is There Any Deal search link from given game name
	# ---------------------------------
	@commands.command()
	async def deal( self, ctx: commands.Context, *_game ):
		game_name = " ".join( _game ).title()
		link_end = "+".join( _game )
		await ctx.send( f"Recherche Is There Any Deal: **[{ game_name }](<https://isthereanydeal.com/search/?q={ link_end }>)**")

	# ---------------------------------
	# Toss a coin
	# ---------------------------------
	@commands.command()
	async def pièce( self, ctx: commands.Context ):
		result: str = "Pile"

		if random.randint( 0, 1 ) == 1:
			result = "Face"
		
		await ctx.send( f"J'ai lancé une pièce, elle est tombé sur **{result}**!" )

	# ---------------------------------
	# Roll the given amount of dice, give the detail of each throw and add them
	# ---------------------------------
	@commands.command()
	async def dé( self, ctx: commands.Context, type: int = 20, number: int = 1 ):
		if type <= 0:
			type = 2

		if number <= 0:
			number = 1

		if number > 100:
			number = 100

		if number == 1:
			await ctx.send( f"J'ai lancé un D{type}, il est tombé sur **{random.randint( 1, type )}**!" )
			return

		max_result = number * type

		launch_detail: str = ""
		total_score: int = 0

		for launch in range( 1, number + 1 ):
			dice_result = random.randint( 1, type )
			total_score += dice_result
			launch_detail += f"Lancé {launch}: **{dice_result}**\n"

		average: int = round( total_score / number )
		launch_detail += f"### Scores\n Total: **{total_score}**\nMax: {max_result}"

		dice_embed = discord.Embed( colour=discord.Colour.random(), title=f"J'ai lancé {number} D{type}...", description=launch_detail)
		await ctx.send( embed=dice_embed )
# ============================================================================


async def setup( _bot ):
	log = logging.getLogger("SDB - Commands")
	log.info( "Commands setup." )
	await _bot.add_cog( Commands( _bot ) )