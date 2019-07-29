#coding=utf-8
import discord
from discord.ext import commands
import random
import time
from collections import OrderedDict
import json
import os

token = os.environ['token']
#channel_id = 602424106389864460 #test
text_channel_id = 560861172648378391 #ours
voice_channel_id = 560861172648378393 #ours
guild_id = 560861172648378389

description = '''
online bot用法：
onilne bot的前導符號為"!"，任何指令前面都須加上才能執行。\n

online bot的功能：
紀錄成員上線時間。只要成員上線後進入任意語音頻道，
online bot會偵測到並回應"I see you, xxx"，這時上線時間已開始累計，
並於下線時(離開此群組也算)結算時數\n

online bot提供之指令列表：\n
'''
bot = commands.Bot(command_prefix='!', description=description)

async def get_channel():
	'''取得voice和text channel物件'''
	v_channel = await bot.fetch_channel(voice_channel_id)
	t_channel = await bot.fetch_channel(text_channel_id)
	return v_channel, t_channel

async def dict_sorting(d):
	d = [(x, int(y)) for x, y in d.items()]
	d.sort(key=lambda s: s[1], reverse=True)
	global online_dict
	online_dict = OrderedDict()
	for name, val in d:
		online_dict[name] = val

@bot.event
async def on_ready():
	'''init'''
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('Read online data')
	with open('RC_info.txt', 'r') as f:
		user = json.loads(f.read())
		await dict_sorting(user)
	global tmp_dict
	tmp_dict = {x: 0 for x, y in user.items()}
	v_channel, t_channel = await get_channel()
	await t_channel.send('打ㄍㄟˊ賀\t挖來啊啦~')
	print('------')
	del user

@bot.event
async def on_voice_state_update(member, before, after):
	'''偵測channel的member變化'''
	try:
		if after.channel!=None and tmp_dict[str(member.id)] == 0:
			tmp_dict[str(member.id)] = time.time()
			v_channel, t_channel = await get_channel()
			print('I see you, {}.'.format(member.display_name))
			# await t_channel.send('I see you, {}.'.format(member.display_name))

		elif after.channel==None and tmp_dict[str(member.id)] != 0:
			get_point = int(time.time() - tmp_dict[str(member.id)])
			online_dict[str(member.id)] += get_point
			await dict_sorting(online_dict)
			v_channel, t_channel = await get_channel()
			print('Bye Bye, {}~, 時數累加 {:.0f}小時 {}分鐘'.format(
				member.display_name, get_point/60//60, get_point//60%60))
			# await t_channel.send('Bye Bye, {}~, 時數累加 {:.0f}小時 {}分鐘'.format(
			#	member.display_name, get_point/60//60, get_point//60%60))
			with open('RC_info.txt', 'w') as f:
				f.write(json.dumps(online_dict))
			tmp_dict[str(member.id)] = 0
	except KeyError:
		pass

@bot.command()
async def timer(ctx):
	"""查看目前成員貢獻值排名"""
	msg = '累計貢獻值：\n\n'
	guild_ = bot.get_guild(guild_id)
	for key, val in online_dict.items():
		user = guild_.get_member(int(key)).display_name
		days, hours, mins, hours_ = int(val/60/60/24), int(val/60/60%24), int(val/60%60), int(val/60/60)
		msg += '{:<10} {} ({}{}天 {}小時 {}分)\n'.format(user, '\t'*4, hours_, days, hours, mins)
	#print(msg)
	await ctx.send(msg)

@bot.command()
async def rc(ctx):
	"""查看舊RC群組資訊"""
	with open('RC_info_2.txt', 'r') as f:
		info = f.readlines()[:-1]
		msg = ''
		for i in info:
			msg += i
		await ctx.send(msg)

bot.run(token)