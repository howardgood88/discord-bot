#coding=utf-8
import discord
from discord.ext import commands
import random
import time
from collections import OrderedDict
import json

token = 'NjAyNDI0ODUzNTcxNjk4Njk4.XTl7yQ.0L9Ct2gljqbfoYTfJ4NLQz6PPUo'
#channel_id = 602424106389864460 #test
text_channel_id = 560861172648378391 #ours
voice_channel_id = 560861172648378393 #ours

description = '''online bot用法'''
bot = commands.Bot(command_prefix='!', description=description)

async def get_channel():
	'''取得voice和text channel物件'''
	v_channel = await bot.fetch_channel(voice_channel_id)
	t_channel = await bot.fetch_channel(text_channel_id)
	return v_channel, t_channel

@bot.event
async def on_ready():
	'''init'''
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('Read online data')
	with open('RC_info.txt', 'r') as f:
		user = json.loads(f.read())
		user = [(x, int(y)) for x, y in user.items()]
		user.sort(key=lambda s: s[1], reverse=True)
	global tmp_dict
	tmp_dict = {x: 0 for x, y in user}
	global online_dict
	online_dict = OrderedDict()
	for name, val in user:
		online_dict[name] = val
	print('------')
	del user, name, val

@bot.event
async def on_voice_state_update(member, before, after):
	'''偵測channel的member變化'''
	try:
		if after.channel!=None and tmp_dict[str(member.id)] == 0:
			tmp_dict[str(member.id)] = time.time()
			v_channel, t_channel = await get_channel()
			print('I see you, {}.'.format(member.display_name))
			await t_channel.send('I see you, {}.'.format(member.display_name))

		elif after.channel==None and tmp_dict[str(member.id)] != 0:
			get_point = int(time.time() - tmp_dict[str(member.id)])
			online_dict[str(member.id)] += get_point
			v_channel, t_channel = await get_channel()
			print('Bye Bye, {}~, 時數累加 {:.0f}小時 {}分鐘'.format(
				member.display_name, get_point/60//60, get_point//60%60))
			await t_channel.send('Bye Bye, {}~, 時數累加 {:.0f}小時 {}分鐘'.format(
				member.display_name, get_point/60//60, get_point//60%60))
			with open('RC_info.txt', 'w') as f:
				f.write(json.dumps(online_dict))
			tmp_dict[str(member.id)] = 0
	except KeyError:
		pass

@bot.command()
async def timer(ctx):
	"""print出貢獻值"""
	msg = '累計貢獻值：\n\n'
	guild_ = bot.get_guild(560861172648378389)
	for key, val in online_dict.items():
		user = guild_.get_member(int(key)).display_name
		days, hours, mins = int(val/60/60/24), int(val/60/60%24), int(val/60%60)
		msg += '{:^10}\t\t{}天 {}小時 {}分\n'.format(user, days, hours, mins)
	#print(msg)
	await ctx.send(msg)

@bot.command()
async def rc(ctx):
	"""舊RC資訊"""
	with open('RC_info_2.txt', 'r') as f:
		info = f.readlines()[:-1]
		msg = ''
		for i in info:
			msg += i
		await ctx.send(msg)

bot.run(token)