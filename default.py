#!/usr/bin/python
import urllib, sys, os
import xbmcaddon, xbmcplugin, xbmcgui,logging
import updatesetting, sync
from xbmc import translatePath, executebuiltin, getInfoLabel

addonID = "plugin.video.anonymous.wall"
Addon = xbmcaddon.Addon(addonID)
AddonName = Addon.getAddonInfo("name")
pluginhandle = int(sys.argv[1])

def ChangeFile(file,search,replace):

	changeFile = unicode(translatePath(file), 'utf-8')

	f = open(changeFile,'r')
	filedata = f.read()
	f.close()
	newdata = filedata.replace(search,replace)
	f = open(changeFile,'w')
	f.write(newdata)
	f.close()

def getParams(arg):
	param=[]
	paramstring=arg
	if len(paramstring)>=2:
		params=arg
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:    
				param[splitparams[0]]=splitparams[1]
							
	return param

def getParam(name,params):
	try:
		return urllib.unquote_plus(params[name])
	except:
		pass

def PlayUrl(url,name,imdb):
	print "******* Anonymous.Media.Wall ART label:{0} t:{1}".format(xbmc.getInfoLabel("ListItem.Label"),xbmc.getInfoLabel("ListItem.Art(thumb)"))
	listitem = xbmcgui.ListItem(path=url,label=xbmc.getInfoLabel("ListItem.Label"), thumbnailImage=xbmc.getInfoLabel("ListItem.Art(thumb)"))
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	listitem.setProperty('IMDBNumber', imdb)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

# Change Player Limits
Player_Ver = 0
try:
	Player_Addon = xbmcaddon.Addon("plugin.video.salts")
	Player_Ver = Player_Addon.getAddonInfo('version')
except:	pass

if Player_Ver and Player_Ver<>Addon.getSetting("salts.version"):
	Addon.setSetting("salts.version",Player_Ver)
	changeFile = os.path.join(Player_Addon.getAddonInfo("path"),"salts_lib","salts_utils.py")
	ChangeFile(changeFile,"def is_salts():","def is_salts():\n    return True")

Player_Ver = 0
try:
	Player_Addon = xbmcaddon.Addon("plugin.video.exodus")
	Player_Ver = Player_Addon.getAddonInfo('version')
except:	pass


if Player_Ver and Player_Ver<>Addon.getSetting("exodus.version"):
	Addon.setSetting("exodus.version",Player_Ver)
	changeFile = os.path.join(Player_Addon.getAddonInfo("path"),"resources","lib","sources","en","library.py")
	ChangeFile(changeFile,"r = [i for i in r if not i['file'].encode('utf-8').endswith('.strm')][0]","")
	changeFile = os.path.join(Player_Addon.getAddonInfo("path"),"resources","lib","modules","player.py")
	ChangeFile(changeFile,"item.setInfo(type='Video', infoLabels = meta)","item.setInfo(type='Video', infoLabels = meta)\n            item.setProperty('IMDBNumber', imdb)")
	
wall=None
action=None
if len(sys.argv) >= 2:   
	params = getParams(sys.argv[2])
	wall=getParam("wall", params)
	action=getParam("action", params)
	
streamAddonMV = Addon.getSetting("StreamMovies")
streamAddonTV = Addon.getSetting("StreamTV")

if wall is None:
	Addon.openSettings()
	updatesetting.main()
elif (wall == "update"):
	sync.main()
elif (action == "player"):
	imdb = getParam("imdb",params)
	print "*** {0}: Wall.Player {1} {2}".format(AddonName,wall,imdb)
	
	streamAddonMV = "Quasar"
	streamAddonTV = "Quasar"
	
if (wall == "movies"):
	imdb = getParam("imdb",params)
	trakt = getParam("trakt",params)
	year = getParam("year",params)
	name = getParam("name",params)
	title = getParam("title",params)
	url = getParam("url",params)
	slug = getParam("slug",params)

	directPlay = Addon.getSetting("DirectPlay")

	if (streamAddonMV=="Metalliq"):
		stream ='plugin://plugin.video.metalliq/movies/play/imdb/{0}/library'.format(imdb)
	if (streamAddonMV=="Genesis"):
		stream ='plugin://plugin.video.genesisreborn/?action=play&imdb={0}&meta={1}&year={2}&title={3}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","originaltitle": "%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,title),safe=''),year,title.replace(' ','%20'))
	if (streamAddonMV=="Elysium"):
		stream ='plugin://plugin.video.elysium/?action=play&imdb={0}&meta={1}&year={2}&title={3}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","originaltitle": "%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,title),safe=''),year,title.replace(' ','%20'))
	if (streamAddonMV=="Exodus"):
		stream ='plugin://plugin.video.exodus/?action=play&imdb={0}&meta={1}&year={2}&title={3}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","originaltitle": "%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,title),safe=''),year,title.replace(' ','%20'))
	if (streamAddonMV=="Specto"):
		stream ='plugin://plugin.video.specto/?action=play&imdb={0}&meta={1}&year={2}&title={3}&name={4}&tmdb=0'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","originaltitle": "%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,title),safe=''),year,title.replace(' ','%20'),name.replace(' ','%20'))
	if (streamAddonMV=="Pulsar"):
		if (directPlay=="false"):
			stream ="plugin://plugin.video.pulsar/movie/{0}/play".format(imdb)
		else:
			stream ="plugin://plugin.video.pulsar/movie/{0}/links".format(imdb)
	if (streamAddonMV=="Quasar"):
		if (directPlay=="false"):
			stream ="plugin://plugin.video.quasar/movie/{0}/play".format(imdb)
		else:
			stream ="plugin://plugin.video.quasar/movie/{0}/links".format(imdb)
	if (streamAddonMV=="SALTS"):
		stream ="plugin://plugin.video.salts/?trakt_id={0}&dialog=True&mode=get_sources&video_type=Movie&title={1}&year={2}&slug={3}".format(trakt,title.replace(' ','+'),year,slug)
	PlayUrl(stream,name,imdb)
	print "*** {0}: Wall.Play: Movie({1} - {2}) {3} {4}:{5}".format(AddonName,imdb,title,streamAddonMV,name,stream)
	try:
		stats = '/movie/{0}/{1}'.format(name.replace("+", " "),streamAddonMV)
		url = "http://wall.ghost-rider.ml/stats.php?"+stats
		response = urllib.urlopen(url)
	except:	pass	

if (wall == "tv"):
	date = getParam("date",params)
	episode = getParam("episode",params)
	trakt = getParam("trakt",params)
	genre = getParam("genre",params)
	imdb = getParam("imdb",params)
	name = getParam("name",params)
	season = getParam("season",params)
	show = getParam("show",params)
	title = getParam("title",params)
	tvdb = getParam("tvdb",params)
	tmdb = getParam("tmdb",params)
	year = getParam("year",params)
	year = getParam("year",params)
	slug = getParam("slug",params)
	
	directPlay = Addon.getSetting("DirectPlay")

	if (streamAddonTV=="Metalliq"):
		stream ='plugin://plugin.video.metalliq/tv/play/{0}/{1}/{2}/library'.format(tvdb,season,episode)
	if (streamAddonTV=="Genesis"):
		stream ='plugin://plugin.video.genesisreborn/?action=play&imdb={0}&meta={1}&year={2}&title={3}&season={4}&episode={5}&tvshowtitle={6}&tvdb={7}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","imdb":"%s","tvshowtitle": "%s","tvdb":"%s","year":"%s","season":"%s","episode":"%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,imdb,title,tvdb,year,season,episode),safe=''),year,title.replace(' ','%20'),season,episode,title,tvdb)
	if (streamAddonTV=="Exodus"):
		stream ='plugin://plugin.video.exodus/?action=play&imdb={0}&meta={1}&year={2}&title={3}&season={4}&episode={5}&tvshowtitle={6}&tvdb={7}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","imdb":"%s","tvshowtitle": "%s","tvdb":"%s","year":"%s","season":"%s","episode":"%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,imdb,title,tvdb,year,season,episode),safe=''),year,title.replace(' ','%20'),season,episode,title,tvdb)
	if (streamAddonTV=="Elysium"):
		stream ='plugin://plugin.video.elysium/?action=play&imdb={0}&meta={1}&year={2}&title={3}&season={4}&episode={5}&tvshowtitle={6}&tvdb={7}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","imdb":"%s","tvshowtitle": "%s","tvdb":"%s","year":"%s","season":"%s","episode":"%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,imdb,title,tvdb,year,season,episode),safe=''),year,title.replace(' ','%20'),season,episode,title,tvdb)
	if (streamAddonTV=="Specto"):
		stream ='plugin://plugin.video.specto/?action=play&imdb={0}&meta={1}&year={2}&title={3}&season={4}&episode={5}&tvshowtitle={6}&tvdb={7}&name={8}'.format(imdb,urllib.quote('{"thumb":"%s","code": "%s","imdb":"%s","tvshowtitle": "%s","tvdb":"%s","year":"%s","season":"%s","episode":"%s"}' % (xbmc.getInfoLabel("ListItem.Art(thumb)"),imdb,imdb,title,tvdb,year,season,episode),safe=''),year,title.replace(' ','%20'),season,episode,title,tvdb,name.replace(' ','%20'))
	if (streamAddonTV=="Pulsar"):
		if (directPlay=="false"):
			stream ="plugin://plugin.video.pulsar/show/{0}/season/{1}/episode/{2}/play".format(tvdb,season,episode)
		else:
			stream ="plugin://plugin.video.pulsar/show/{0}/season/{1}/episode/{2}/links".format(tvdb,season,episode)
	if (streamAddonTV=="Quasar"):
		if (directPlay=="false"):
			stream ="plugin://plugin.video.quasar/show/{0}/season/{1}/episode/{2}/play".format(tmdb,season,episode)
		else:
			stream ="plugin://plugin.video.quasar/show/{0}/season/{1}/episode/{2}/links".format(tmdb,season,episode)
	if (streamAddonTV=="SALTS"):
		stream ="plugin://plugin.video.salts/?ep_airdate=2012-05-14&episode={0}&dialog=True&title={1}&ep_title=NULL&season={2}&video_type=Episode&mode=get_sources&year={3}&trakt_id={4}".format(episode,title,season,year,trakt)
 
	PlayUrl(stream,name,imdb) 	
	print "*** {0}: Wall.Play: TV({1} - {2}) {3} {4}".format(AddonName,tvdb,name,streamAddonTV,stream)

	try:
		stats = '/tv/{0}/S{1}/E{2}/{3}'.format(show.replace("+", " "),str(season).zfill(2),str(episode).zfill(2),streamAddonTV)
		url = "http://wall.ghost-rider.ml/stats.php?"+stats
		response = urllib.urlopen(url)
	except:	pass