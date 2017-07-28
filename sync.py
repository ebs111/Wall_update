#!/usr/bin/python

import os, sys, urllib, json, re, shutil, glob, platform,time
import xbmcaddon, xbmcgui, xbmc, time, datetime, urllib2,logging
import json
	
def slugify(text):
    return re.sub(r'\W+', '-', text.lower())

def GetMovieSearchQuery():
	q = "&year_s="+Addon.getSetting("year_s")+"&year_e="+Addon.getSetting("year_e")
	q = q+"&rating="+Addon.getSetting("rating")
	if Addon.getSetting("subs") == "true":
		q = q+"&subs=1"

	if Addon.getSetting("limitMovies") > 0:
		q = q+"&limit="+Addon.getSetting("limitMovies")
	
	if Addon.getSetting("genre_0") == "true":
		q = q+"&genre=all"
	else:
		genre_q = ""
		genres = [12,14,16,18,27,28,35,36,37,53,80,99,878,9648,10402,10749,10751,10752,10769,10770]
		for genre in genres:
			if Addon.getSetting("genre_%d"%(genre)) == "true":
				genre_q = genre_q+"%d,"%(genre)
		q = q+"&genre="+genre_q
	return q

def UpdateMovies(libraryFolderMovies):
	q = GetMovieSearchQuery()
	url = "https://ia801509.us.archive.org/19/items/all_data_20170727/all_data.json"
	try:
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		LOG.append("Wall.Sync: Movie API {0}".format(q.decode("utf-8")))
	except:
		data = ""
		LOG.append("Wall.Sync: ERROR Movie API {0}".format(q.decode("utf-8")))
		pass

	folders = []
	# Add new Movies
	try:
		LOG.append("Wall.Sync: Movie Folder Exist:{0} # {1} {2}".format(os.path.isdir(xbmc.translatePath(libraryFolderMovies)),sum([len(files) for r, d, files in os.walk(xbmc.translatePath(libraryFolderMovies))]),xbmc.translatePath(libraryFolderMovies).decode("utf-8")))
	except:
		LOG.append("Wall.Sync: ERROR Movie Folder {0} {1}".format(os.path.isdir(xbmc.translatePath(libraryFolderMovies)),xbmc.translatePath(libraryFolderMovies).decode("utf-8")))
		pass
	x=0
	for movie in data:
		if x>int(Addon.getSetting("limitMovies")):
		 break

		if int(movie['year'])>=int(Addon.getSetting("year_s")) and int(movie['year'])<=int(Addon.getSetting("year_e")) and x<int(Addon.getSetting("limitMovies")):
		 x=x+1
		 movie_name = movie['title'][:63]+" ("+movie['year']+")"
		 folders.append(movie_name)
		 MovieFolder = xbmc.translatePath(os.path.join(libraryFolderMovies, movie_name)).decode("utf-8")
		 if not os.path.exists(MovieFolder):
			LOG.append("Wall.Sync: ADD Movie {0}".format(movie_name.decode("utf-8")))
			os.makedirs(MovieFolder)

			NFOFile = xbmc.translatePath(os.path.join(MovieFolder, movie_name+".nfo")).decode("utf-8")
			f = open(NFOFile, 'w')
			f.write("http://www.imdb.com/title/"+movie['imdb']+"/")
			f.close()
			
			  
			    
			
			StrFile = xbmc.translatePath(os.path.join(MovieFolder, movie_name+".strm")).decode("utf-8")
			Str = {'imdb':movie['imdb'],'trakt':movie['trakt'],'year':movie['year'],'name':movie_name,'title':movie['title'].decode("utf-8"),'slug':slugify(movie['title'])+"+"+movie['year'],'url':"http://www.imdb.com/title/"+movie['imdb']+"/"}
			f = open(StrFile, 'w')
			f.write("plugin://plugin.video.ghostrider.wall/?wall=movies&"+urllib.urlencode(Str))
			f.close()
			
			try:
				MovieDate = int(movie['date'])
				os.utime(MovieFolder,(MovieDate,MovieDate))
				os.utime(StrFile,(MovieDate,MovieDate))
				os.utime(NFOFile,(MovieDate,MovieDate))
			except:
				LOG.append("......... Wall.Sync: ERROR Set Movie Date {0}".format(StrFile.decode("utf-8")))
				pass
	
	# Add remove Movies by filter
	if Addon.getSetting("RemoveFiles") == "true":
		CleanDBnFiles(folders,libraryFolderMovies,2)

def GetTVSearchQuery():
	q = "&year_s="+Addon.getSetting("year_s_tv")+"&year_e="+Addon.getSetting("year_e_tv")
	q = q+"&rating="+Addon.getSetting("rating_tv")
	
	if Addon.getSetting("limitTv") > 0:
		q = q+"&limit="+Addon.getSetting("limitTv")

	if Addon.getSetting("genre_0_tv") == "true":
		q = q+"&genre=all"
	else:
		genre_q = ""
		for genre in range(1, 28):
			if Addon.getSetting("genre_%d_tv"%(genre)) == "true":
				genre_q = genre_q+"%d,"%(genre)
		q = q+"&genre="+genre_q
	return q

def UpdateTV(libraryFolderTV):
	# Get TV Info
	q = GetTVSearchQuery()
	url = "https://ia801501.us.archive.org/26/items/all_data_series/all_data_series.json"
	try:
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		LOG.append("Wall.Sync: TV API {0}".format(q.decode("utf-8")))
	except:
		data = ""
		LOG.append("Wall.Sync: ERROR TV API {0}".format(q.decode("utf-8")))
		pass

	folders = []
	try:
		LOG.append("Wall.Sync: TV Folder Exist:{0} # {1} {2}".format(os.path.isdir(xbmc.translatePath(libraryFolderTV)),sum([len(files) for r, d, files in os.walk(xbmc.translatePath(libraryFolderTV))]),xbmc.translatePath(libraryFolderTV).decode("utf-8")))
	except:
		LOG.append("Wall.Sync: ERROR TV Folder {0} {1}".format(os.path.isdir(xbmc.translatePath(libraryFolderTV)),xbmc.translatePath(libraryFolderTV).decode("utf-8")))
		pass
	# Add new TV Shows
	y=0
	
	for tv in data:
	


		
		if y>int(Addon.getSetting("limitMovies")):
		 break

		if int(tv['year'])>=int(Addon.getSetting("year_s_tv")) and int(tv['year'])<=int(Addon.getSetting("year_e_tv")) and y<int(Addon.getSetting("limitTv")):
		 y=y+1
		 if tv['year'] in tv['title']:
			tv_name = tv['title']
			slug = slugify(tv_name)
		 else:
			tv_name = tv['title']+" ("+tv['year']+")"
			slug = slugify(tv['title'])+" ("+tv['year']+")"
		 folders.append(tv_name)
		 TVFolder = (xbmc.translatePath(os.path.join(libraryFolderTV, removeDisallowedFilenameChars(tv_name))).decode("utf-8"))
		 if not os.path.exists(TVFolder):
			
			try:
			  LOG.append("Wall.Sync: Create TV {0}".format(tv_name.encode('utf-8')))
			except:
			 pass
			os.makedirs(TVFolder)
			NFOFile = xbmc.translatePath(os.path.join(TVFolder, "tvshow.nfo")).decode("utf-8")
			f = open(NFOFile, 'w')
			f.write("http://thetvdb.com/index.php?tab=series&id="+tv['tvdb'])
			f.close()
		 season = tv['season']
		 lastupdate = tv['lastupdate']
		 for i in season.keys():
			if season[i]>0:
				SeasonFolder = xbmc.translatePath(os.path.join(libraryFolderTV, removeDisallowedFilenameChars(tv_name),'Season %02d'%int(i))).decode("utf-8")
				if not os.path.exists(SeasonFolder):
					try:
					  LOG.append("...... Wall.Sync: Create TV Session {0}".format(tv_name+' Season %02d'%int(i)))
					except:
					  pass
					os.makedirs(SeasonFolder)
				for x in range(1,(int(season[i])+1)):
					StrFile = xbmc.translatePath(os.path.join(libraryFolderTV, removeDisallowedFilenameChars(tv_name),'Season %02d'%int(i), removeDisallowedFilenameChars(tv['title'])+' S%02d'%int(i)+'E%02d'%int(x)+".strm")).decode("utf-8")
					if not os.path.exists(StrFile):
						LOG.append("......... Wall.Sync: Add TV Episode {0}".format('S%02d'%int(i)+'E%02d'%int(x)))
						Str = {'imdb':tv['imdb'],'tmdb':tv['tmdb'],'trakt':tv['trakt'],'year':tv['year'],'title':tv['title'],'slug':slug,'url':"http://www.imdb.com/title/"+tv['imdb']+"/",'episode':x,"season":i,"show":removeDisallowedFilenameChars(tv_name),"name":removeDisallowedFilenameChars(tv['title'])+' S%02d'%int(i)+'E%02d'%int(x),"tvdb":tv['tvdb']}
						
						f = open(StrFile, 'w')
						f.write("plugin://plugin.video.ghostrider.wall/?wall=tv&"+urllib.urlencode(encoded_dict(Str)))
						f.close()
						try:
						
						  os.utime(StrFile,(int(lastupdate[i]),int(lastupdate[i])))
						except:
						#	LOG.append("......... Wall.Sync: ERROR Set TV Episode Date {0}".format(StrFile.decode("utf-8")))
							pass

	# Add remove Movies by filter
	if Addon.getSetting("RemoveFiles") == "true":
		CleanDBnFiles(folders,libraryFolderTV,1)		
	
#def CheckRepo():
#	try:
#		repo = 'repository.GhostRider'
#		folder = xbmc.translatePath(os.path.join('special://home','addons',repo))
#		if not os.path.isdir(folder):
#			LOG.append("Wall.Sync: Adding GhostRider Repo")
#			os.makedirs(folder)
#			xml_file = xbmc.translatePath(os.path.join('special://home','addons',repo,'addon.xml'))
#			urllib.urlretrieve ("http://repo.thewiz.info/"+repo+"/addon.xml", xml_file)
#			icon_file = xbmc.translatePath(os.path.join('special://home','addons',repo,'icon.png'))
#			urllib.urlretrieve ("http://repo.thewiz.info/"+repo+"/icon.png", icon_file)
#	except: pass


def removeDisallowedFilenameChars(filename):
    import unicodedata,string

    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)
	
def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict
def json_query(query):
	xbmc_request = json.dumps(query)
	raw = xbmc.executeJSONRPC(xbmc_request)
	clean = unicode(raw, 'utf-8', errors='ignore')
	response = json.loads(clean)
	result = response.get('result', response)

	return result

def CleanDBnFiles(FoldersRemove,libraryFolder,type):

	# Check type movie or TV
	if type==1:
		method = "VideoLibrary.GetTVShows"
		array = 'tvshows'
		key = 'tvshowid'
		methodRemove = "VideoLibrary.RemoveTVShow"
	else:
		method = "VideoLibrary.GetMovies"
		array = 'movies'
		key = 'movieid'
		methodRemove = "VideoLibrary.RemoveMovie"
	
	# Remove from DB
	remove_data = json_query({"jsonrpc": "2.0","id": 1, "method": method,  "params": { "properties" : ['title', 'imdbnumber','file'] }})
	LOG.append("Wall.Sync: CleanDB {0} {1}".format(array,methodRemove))

	if array in remove_data and remove_data[array]:
		remove2_data = remove_data[array]
		for show in remove2_data:
			ff = os.path.basename(os.path.normpath(show['file']))
			ff2 = os.path.splitext(ff)[0]
			if not ff in FoldersRemove:
				if "plugin.video.ghostrider.wall" in show['file']:
					result = json_query({"jsonrpc": "2.0","id": 1, "method": methodRemove,  "params": { key : show[key] }})
					LOG.append("... Wall.Sync: Remove DB {0}".format(show['file']))
	
	# Remove folders
	filelist = glob.glob(xbmc.translatePath(os.path.join(libraryFolder,"*")))
	if filelist != []:
		for f in filelist:
			ff = os.path.basename(os.path.normpath(f))
			if not ff in FoldersRemove:
				try:
					shutil.rmtree(f)
					LOG.append("... Wall.Sync: Remove File/Folder {0}".format(f))
				except:
					pass

def upload_file(filepath):
	file_content = open(filepath, 'r').read()
	post_dict = {
		'data': file_content,
		'project': 'www',
		'language': 'text',
		'expire': 1209600,
	}
	post_data = json.dumps(post_dict)
	headers = {
		'User-Agent': '%s-%s' % (AddonName, AddonVersion),
		'Content-Type': 'application/json',
	}
	req = urllib2.Request('http://xbmclogs.com/api/json/create', post_data, headers)
	response = urllib2.urlopen(req).read()
	try:
		response_data = json.loads(response)
	except:
		response_data = None
	if response_data and response_data.get('result', {}).get('id'):
		paste_id = response_data['result']['id']
		print "***** Log Upload {0}".format(paste_id)
		return paste_id
	else:
		print "***** Error Log Upload {0}".format(repr(response))

def main():
	global AddonName,baseUrl,Addon,LOG,AddonVersion
	addonID = "plugin.video.ghostrider.wall"
	Addon = xbmcaddon.Addon(addonID)
	LOG = []
	AddonName = Addon.getAddonInfo("name")
	AddonPath = Addon.getAddonInfo("path")
	AddonVersion = Addon.getAddonInfo('version')

	cctime = datetime.datetime.now()
	LOG.append("*********************** {0} ***********************".format(cctime.strftime('%d/%m/%Y %H:%M:%S')))
	(system, node, release, version, machine, processor) = platform.uname()
	LOG.append("OS:{0} OS_VER:{1} OS_DIST:{2} User:{3}".format(system,release,version,node))
	LOG.append("Kodi:{0} KodiName:{1} Python:{2}".format(xbmc.getInfoLabel("System.BuildVersion"),xbmc.getInfoLabel('System.FriendlyName').replace('XBMC (','').replace(')',''),platform.python_version()))
	LOG.append("CPU_TYPE:{0} CPU:{1}".format(machine,processor))
	LOG.append("FREEHD: {0} TOTALHD: {1}".format(xbmc.getInfoLabel("System.FreeSpace"),xbmc.getInfoLabel("System.TotalSpace")))
	LOG.append("FREEMEM:{0} TOTALMEM:{1}".format(xbmc.getInfoLabel("System.FreeMemory"),xbmc.getInfoLabel("System.Memory(total)")))
	LOG.append("#### Addon Setting ####")
	LOG.append("GhostRider Media Wall Ver: {0} Syn.Time: {1}".format(AddonVersion,Addon.getSetting("StartDelay")))
	LOG.append("Movies: Status {0} Limit {1} Stream {2}".format(Addon.getSetting("useStreamMovies"),Addon.getSetting("limitMovies"),Addon.getSetting("StreamMovies")))
	LOG.append("TV:     Status {0} Limit {1} Stream {2}".format(Addon.getSetting("useStreamTV"),Addon.getSetting("limitTv"),Addon.getSetting("StreamTV")))
	#CheckRepo()
	
	libraryFolder = "special://userdata/addon_data/plugin.video.ghostrider.wall/library/"
	libraryFolderMovies = "special://userdata/addon_data/plugin.video.ghostrider.wall/library/movies/"
	libraryFolderTV = "special://userdata/addon_data/plugin.video.ghostrider.wall/library/tv/"

	if Addon.getSetting("useStreamMovies") == "true":
		UpdateMovies(libraryFolderMovies)

	if Addon.getSetting("useStreamTV") == "true":
		UpdateTV(libraryFolderTV)

	cctime2 = datetime.datetime.now()
	LOG.append("*********************** {0} {1}***********************".format(cctime2.strftime('%d/%m/%Y %H:%M:%S'),(cctime2-cctime)))
	# Dump Log
	logfilep = xbmc.translatePath(os.path.join("special://userdata/addon_data/plugin.video.ghostrider.wall/", "thewiz.wall.log")).decode("utf-8")
	logfile = open(logfilep, 'w')
	for line in LOG:
		logfile.write("\n"+line)
	logfile.close

	xbmc.executebuiltin('Notification({0}, GhostRider.Wall Updated, {1}, {2})'.format(AddonName, 5000,os.path.join( AddonPath ,"icon.png" )))

	if Addon.getSetting("UpdateVideo") == "true":
		while xbmc.getCondVisibility('Library.IsScanningVideo') == True:
			xbmc.sleep(10000)
		xbmc.executebuiltin('UpdateLibrary(video,{0})'.format(libraryFolderMovies))
		while xbmc.getCondVisibility('Library.IsScanningVideo') == True:
			xbmc.sleep(10000)
		xbmc.executebuiltin('UpdateLibrary(video,{0})'.format(libraryFolderTV))
#ebs#