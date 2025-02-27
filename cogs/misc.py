from discord.ext import commands
import aiosqlite
import discord
import random


class Misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.utils = self.bot.get_cog('Utils')

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def prefix(self, ctx: commands.Context, *, prefix: str = None) -> None:
		if prefix is None:
			prefix = await self.utils.get_prefix(ctx.guild.id)
			embed = discord.Embed(title='Prefix', description=f'My prefix is `{prefix}`.')
			embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
			await ctx.send(embed=embed)
			return

		if len(prefix) > 4:
			embed = discord.Embed(title='Error', description='Prefixes are limited to 4 characters or less.')
			await ctx.send(embed=embed)
			return

		async with aiosqlite.connect('Data/autotss.db') as db:
			await db.execute('UPDATE prefix SET prefix = ? WHERE guild = ?', (prefix, ctx.guild.id))
			await db.commit()

		embed = discord.Embed(title='Prefix', description=f'Prefix changed to `{prefix}`.')
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))

		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def invite(self, ctx: commands.Context) -> None:
		embed = discord.Embed(title='Invite', description=f'[Click here]({self.utils.invite}).')
		embed.set_thumbnail(url=self.bot.user.avatar_url_as(static_format='png'))
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))

		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def ping(self, ctx: commands.Context) -> None:
		num = random.randint(0, 1500)

		if num == 69: # nothing like some easter eggs, right?
			title = 'Nice'
		elif num == 1337:
			title = 'L33t'
		elif num == 420:
			title = '420BlazeIt'
		elif num == 666:
			title = 'Whoa there Satan, calm down'
		else:
			title = 'Pong!'

		embed = discord.Embed(title=title, description=f'Ping: `{round(self.bot.latency * 1000)}ms`')
		embed.set_footer(text=ctx.message.author.name, icon_url=ctx.message.author.avatar_url_as(static_format='png'))
		await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def info(self, ctx: commands.Context) -> None:
		prefix = await self.utils.get_prefix(ctx.guild.id)

		embed = discord.Embed(title="Hi, I'm AutoTSS!")
		embed.add_field(name='What do I do?', value='I can automatically save SHSH blobs for all of your iOS devices!', inline=False)
		embed.add_field(name='Prefix', value=f'My prefix is `{prefix}`. To see what I can do, run `{prefix}help`!', inline=False)
		embed.add_field(name='Creator', value=(await self.bot.fetch_user(728035061781495878)).mention, inline=False)
		embed.add_field(name='Disclaimer', value='This should NOT be your only source for saving blobs. I am not at fault for any issues you may experience with AutoTSS.', inline=False)
		embed.add_field(name='Notes', value='- There is a limit of 10 devices per user.\n- You must be in a server with AutoTSS, or your SHSH blobs will no longer be automatically saved. This **does not** have to be the same server that you added your devices to AutoTSS in.\n- Blobs are automatically saved every 30 minutes.', inline=False)
		embed.add_field(name='Source Code', value="AutoTSS's source code can be found on [GitHub](https://github.com/m1stadev/AutoTSS).", inline=False)
		embed.add_field(name='Support', value='For any questions about AutoTSS, join my [discord](https://m1sta.xyz/discord).', inline=False)
		embed.set_thumbnail(url=self.bot.user.avatar_url_as(static_format='png'))
		embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Misc(bot))
