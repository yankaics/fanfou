#!/usr/bin/env python
#-*- coding=utf-8 -*-

import web
import hashlib, time, re
import urllib, urllib2
import message
import hanzi
import photo
from lxml import etree

render = web.template.render('templates/')
db     = web.database(dbn='mysql',user='root',pw='password',db='fanfou')

class wechatmsg:
    def GET(self):
        token = "fanfou"
        params = web.input()
        args = [token, params['timestamp'], params['nonce']]
        args.sort()
        if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
            if params.has_key('echostr'):
                return params['echostr']

    def POST(self):
        str_xml = web.data() 
        xml     = etree.fromstring(str_xml)
        msgType = xml.find("MsgType").text
        fromUser= xml.find("FromUserName").text
        toUser  = xml.find("ToUserName").text
        
        if msgType=='event':
            event = xml.find("Event").text
            if   event == 'subscribe'  :
                #count = db.select('fanfou' ,what="count(id)") 
                #count = count[0].count
                #db.insert('timeline', weixin=fromUser ,num=count)
                return render.weixin(fromUser,toUser,int(time.time()),hanzi.hello)
            elif event == 'unsubscribe':
                pass
                
        elif msgType=='text' :
            content  = xml.find("Content").text
            message.save(content,1)
            return render.weixin(fromUser,toUser,int(time.time()),hanzi.txtok)
            
        elif msgType=='image':
            pic_url  = xml.find("PicUrl").text
            msg_id   = xml.find("MsgId").text
            info     = photo.save(msg_id, pic_url)
            if info == 1:
                return render.weixin(fromUser,toUser,int(time.time()),hanzi.cnfse)
            
        else:
            return render.weixin(fromUser,toUser,int(time.time()),hanzi.cnfse)
