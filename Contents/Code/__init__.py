NAME = 'Anna Kim Photography'
RSS_FEED = 'http://www.annakimphotography.com/blog/feed/'
RSS_NS = {'content': 'http://purl.org/rss/1.0/modules/content/'}

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME
	HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
@handler('/photos/annakimphotography', NAME)
def MainMenu():

	oc = ObjectContainer()

	xml = XML.ElementFromURL(RSS_FEED)

	for item in xml.xpath('//item'):

		content = item.xpath('./content:encoded/text()', namespaces=RSS_NS)[0]
		html = HTML.ElementFromString(content)
		thumb = html.xpath('//img[contains(@src, "/uploads/")]/@src')

		if len(thumb) < 1:
			continue

		url = item.xpath('./link/text()')[0]
		title = item.xpath('./title/text()')[0]
		summary = item.xpath('./description/text()')[0]
		originally_available_at = Datetime.ParseDate(item.xpath('./pubDate')[0].text)

		oc.add(PhotoAlbumObject(
			url = url,
			title = String.DecodeHTMLEntities(title),
			summary = String.DecodeHTMLEntities(summary),
			originally_available_at = originally_available_at,
			thumb = Resource.ContentsOfURLWithFallback(url=thumb[0])
		))

	return oc
