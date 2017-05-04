# This Python file uses the following encoding: utf-8
from flask import render_template, request, Blueprint, session, redirect, url_for, json
import random
import re
from app.controler.power_API import get_business_json
from public_function import get_first_letter
import time


class cMediaOverview:

	@staticmethod
	def mediaOverviewJson(username,filternode):
		jsons = json.loads(get_business_json("media_1.json", username))["body"]  # 字符串传化为json 对象 dict
		args = filternode
		jsons = json.dumps(jsons,ensure_ascii=False)
		jsons = jsons.replace(" ","")

		resultjson=[]
		word=r'({[^}]*[^}]*})'
		jsons=",".join(re.findall(word,jsons))

		for x in xrange(0,len(args)):
		  if args[x][0]=="tjtype":
			tjtype=args[x][1]
		  if args[x][0]=="channel_name"  or args[x][0]=="agent" or args[x][0]=="staff" :
			if args[x][1]!="":
			  word=r'({[^}]*"'+args[x][0]+'":"'+args[x][1].replace(',','"[^}]*}|{[^}]*"'+args[x][0]+'":"')+'"[^}]*})'
	  
			  jsons=",".join(re.findall(word,jsons))
		   
			else:
			  word=r'({[^}]*[^}]*})'
			  jsons=",".join(re.findall(word,jsons))


		jsons=jsons.replace('"r1":""','"r1":0')
		jsons=jsons.replace('"r29":""','"r29":0')
		jsons=jsons.replace('"r6":""','"r6":0')
		jsons=jsons.replace('"cumulative_flow":""','"cumulative_flow":0')
		jsons=jsons.replace('"cumulative_money":""','"cumulative_money":0')
		jsons=jsons.replace('"spend":""','"spend":0')
		jsons=json.loads("["+jsons+"]")#加上[]  就可以返回了
		new_json=[]
		date_temp=[]

		jsons.sort(key=lambda jsons:jsons.get("date_time",0))

		for x in xrange(1,len(jsons)):
			if jsons[x]["date_time"] == jsons[x-1]["date_time"]:  

				jsons[x]["ad_click"]=int(round(float(jsons[x]["ad_click"])))+int(round(float(jsons[x-1]["ad_click"])))
				jsons[x]["ad_action"]=int(round(float(jsons[x]["ad_action"])))+int(round(float(jsons[x-1]["ad_action"])))
				jsons[x]["double_new"]=int(round(float(jsons[x]["double_new"])))+int(round(float(jsons[x-1]["double_new"])))
				jsons[x]["back_user"]=int(round(float(jsons[x]["back_user"])))+int(round(float(jsons[x-1]["back_user"])))
				jsons[x]["ad_action_new"]=int(round(float(jsons[x]["ad_action_new"])))+int(round(float(jsons[x-1]["ad_action_new"])))
				jsons[x]["ad_account_new"]=int(round(float(jsons[x]["ad_account_new"])))+int(round(float(jsons[x-1]["ad_account_new"])))
				jsons[x]["paid_account"]=int(round(float(jsons[x]["paid_account"])))+int(round(float(jsons[x-1]["paid_account"])))
				jsons[x]["spend"]=int(round(float(jsons[x]["spend"])))+int(round(float(jsons[x-1]["spend"])))
				jsons[x]["cumulative_flow"]=int(round(float(jsons[x]["cumulative_flow"])))+int(round(float(jsons[x-1]["cumulative_flow"])))
				jsons[x]["cumulative_money"]=int(round(float(jsons[x]["cumulative_money"])))+int(round(float(jsons[x-1]["cumulative_money"])))
				jsons[x]["r1"]=int(round(float(jsons[x]["r1"])))+int(round(float(jsons[x-1]["r1"])))
				jsons[x]["r6"]=int(round(float(jsons[x]["r6"])))+int(round(float(jsons[x-1]["r6"])))
				jsons[x]["r29"]=int(round(float(jsons[x]["r29"])))+int(round(float(jsons[x-1]["r29"])))
				jsons[x]["ad_role_31"]=int(round(float(jsons[x]["ad_role_31"])))+int(round(float(jsons[x-1]["ad_role_31"])))
				jsons[x]["ad_AU_5"]=int(round(float(jsons[x]["ad_AU_5"])))+int(round(float(jsons[x-1]["ad_AU_5"])))
				jsons[x-1]=""
			else:
				jsons[x]["ad_click"]=int(round(float(jsons[x]["ad_click"])))
				jsons[x]["ad_action"]=int(round(float(jsons[x]["ad_action"])))
				jsons[x]["double_new"]=int(round(float(jsons[x]["double_new"])))
				jsons[x]["back_user"]=int(round(float(jsons[x]["back_user"])))
				jsons[x]["ad_action_new"]=int(round(float(jsons[x]["ad_action_new"])))
				jsons[x]["ad_account_new"]=int(round(float(jsons[x]["ad_account_new"])))
				jsons[x]["paid_account"]=int(round(float(jsons[x]["paid_account"])))
				jsons[x]["spend"]=int(round(float(jsons[x]["spend"])))
				jsons[x]["cumulative_flow"]=int(round(float(jsons[x]["cumulative_flow"])))
				jsons[x]["cumulative_money"]=int(round(float(jsons[x]["cumulative_money"])))
				jsons[x]["r1"]=int(round(float(jsons[x]["r1"])))
				jsons[x]["r6"]=int(round(float(jsons[x]["r6"])))
				jsons[x]["r29"]=int(round(float(jsons[x]["r29"])))
				jsons[x]["ad_role_31"]=int(round(float(jsons[x]["ad_role_31"])))
				jsons[x]["ad_AU_5"]=int(round(float(jsons[x]["ad_AU_5"])))

		for item in jsons[:]: # 复制一个json list 出来，凡是刚才赋值为“”的都标记为删除，remove后 的jsons 就是结果了
			if item == "":
				jsons.remove(item)



		for x in xrange(0,len(jsons)):

				jsons[x]["fufeilv"]=float(float(jsons[x]["paid_account"])/float(jsons[x]["ad_account_new"])*100) if float(jsons[x]["ad_account_new"])!= 0 else 0
				jsons[x]["ROI"]=float(float(jsons[x]["cumulative_money"])/float(jsons[x]["spend"])*100) if float(jsons[x]["spend"])!= 0 else 0
				jsons[x]["CPA"]=float(float(jsons[x]["spend"])/float(jsons[x]["ad_action_new"])) if float(jsons[x]["ad_account_new"])!= 0 else 0
				#print(jsons[x]["paid_account"],jsons[x]["ad_account_new"],jsons[x]["paid_account"]/jsons[x]["ad_account_new"])
		jsons=json.dumps(jsons)
		jsons = jsons.replace(" ","") 
		return jsons 

		# # 处理channel请求
		# channel_name = request.args.get('channel_name')
		# jsons_filter_channel_names = []
		# if channel_name != "":
		# 	channel_names = channel_name.split(",")
		# 	for i in range(len(jsons)):
		# 		if jsons[i]["channel_name"] in channel_names:
		# 			jsons_filter_channel_names.append(jsons[i])
		# else:
		# 	jsons_filter_channel_names = jsons

		# # 处理agent请求
		# agent = request.args.get('agent')
		# jsons_filter_agents = []
		# if agent != "":
		# 	agents = agent.split(",")
		# 	for i in range(len(jsons_filter_channel_names)):
		# 		if jsons_filter_channel_names[i]["agent"] in agents:
		# 			jsons_filter_agents.append(jsons_filter_channel_names[i])
		# else:
		# 	jsons_filter_agents = jsons_filter_channel_names

		# # 处理staff请求
		# staff = request.args.get('staff')
		# jsons_filter_staffs = []
		# if staff != "":
		# 	staffs = staff.split(",")
		# 	for i in range(len(jsons_filter_agents)):
		# 		if jsons_filter_agents[i]["staff"] in staffs:
		# 			jsons_filter_staffs.append(jsons_filter_agents[i])
		# else:
		# 	jsons_filter_staffs = jsons_filter_agents

		# # 按照日期 group by 筛选出有的日期
		# newjson = []
		# for ii in range(len(jsons_filter_staffs)):
		# 	flag = 1
		# 	for jj in range(len(newjson)):
		# 		if newjson != []:
		# 			if jsons_filter_staffs[ii]["date_time"] == newjson[jj]["date_time"]:
		# 				flag = 0
		# 				break
		# 		else:
		# 			flag = 1
		# 	if flag:
		# 		newjson.append({"date_time": jsons_filter_staffs[ii]["date_time"]})

		# # 拼凑json串
		# for ii in range(len(newjson)):
		# 	newjson[ii]["channel_name"] = "groupBy"  # 渠道
		# 	newjson[ii]["agent"] = "groupBy"  # 代理
		# 	newjson[ii]["staff"] = "groupBy"  # 负责人
		# 	newjson[ii]["ad_click"] = 0.0  # 点击设备
		# 	newjson[ii]["ad_action"] = 0.0  # 激活设备
		# 	newjson[ii]["ad_action_new"] = 0.0  # 新增设备
		# 	newjson[ii]["ad_account_new"] = 0.0  # 新增总账号
		# 	newjson[ii]["double_new"] = 0.0  # 纯新增账号
		# 	newjson[ii]["back_user"] = 0.0  # 回流账号
		# 	newjson[ii]["paid_account"] = 0.0  # 付费账号
		# 	newjson[ii]["spend"] = 0.0  # 折后花费
		# 	newjson[ii]["cumulative_flow"] = 0.0  # 累计流水
		# 	newjson[ii]["dis"] = 0.0  # 分成比例
		# 	newjson[ii]["cumulative_moeny"] = 0.0  # 累计净收入

		# # 讲数据累加带对应日期
		# for jj in jsons_filter_staffs:
		# 	for ii in range(len(newjson)):
		# 		if jj["date_time"] == newjson[ii]["date_time"]:
		# 			newjson[ii]["ad_click"] = newjson[ii]["ad_click"] + int(jj["ad_click"])  # 点击设备
		# 			newjson[ii]["ad_action"] = newjson[ii]["ad_action"] + int(jj["ad_action"])  # 激活设备
		# 			newjson[ii]["ad_action_new"] = newjson[ii]["ad_action_new"] + int(jj["ad_action_new"])  # 新增设备
		# 			newjson[ii]["ad_account_new"] = newjson[ii]["ad_account_new"] + int(jj["ad_account_new"])  # 新增总账号
		# 			newjson[ii]["double_new"] = newjson[ii]["double_new"] + int(jj["double_new"])  # 纯新增账号
		# 			newjson[ii]["back_user"] = newjson[ii]["back_user"] + int(jj["back_user"])  # 回流账号
		# 			newjson[ii]["paid_account"] = newjson[ii]["paid_account"] + int(jj["paid_account"])  # 付费账号
		# 			newjson[ii]["spend"] = newjson[ii]["spend"] + float(jj["spend"])  # 折后花费
		# 			newjson[ii]["cumulative_flow"] = newjson[ii]["cumulative_flow"] + float(
		# 				jj["cumulative_flow"])  # 累计流水
		# 			newjson[ii]["dis"] = newjson[ii]["dis"] + float(jj["dis"])  # 分成比例
		# 			newjson[ii]["cumulative_moeny"] = newjson[ii]["cumulative_moeny"] + float(
		# 				jj["cumulative_moeny"])  # 累计净收入

		# # 计算 fufeilv CPA ROI
		# for ii in range(len(newjson)):
		# 	if float(newjson[ii]["ad_account_new"]) != 0:
		# 		newjson[ii]["fufeilv"] = newjson[ii]["paid_account"] / float(newjson[ii]["ad_account_new"])  # fufeilv
		# 		newjson[ii]["CPA"] = newjson[ii]["spend"] / float(newjson[ii]["ad_account_new"])  # CPA

		# 		newjson[ii]["fufeilv"] = round(newjson[ii]["fufeilv"], 2)
		# 		newjson[ii]["CPA"] = round(newjson[ii]["CPA"], 2)

		# 	else:
		# 		newjson[ii]["fufeilv"] = '0'
		# 		newjson[ii]["CPA"] = '0'

		# 	if float(newjson[ii]["spend"]) != 0:
		# 		newjson[ii]["ROI"] = newjson[ii]["cumulative_moeny"] / float(newjson[ii]["spend"])  # ROI
		# 		newjson[ii]["ROI"] = round(newjson[ii]["ROI"] * 100, 2)
		# 	else:
		# 		newjson[ii]["ROI"] = '0'

		# 	# 将float 保留2位小数
		# 	newjson[ii]["spend"] = round(newjson[ii]["spend"], 2)
		# 	newjson[ii]["cumulative_flow"] = round(newjson[ii]["cumulative_flow"], 2)
		# 	newjson[ii]["dis"] = round(newjson[ii]["dis"], 2)
		# 	newjson[ii]["cumulative_moeny"] = round(newjson[ii]["cumulative_moeny"], 2)

		# return json.dumps(newjson)  # 将dict 转化成 字符串
