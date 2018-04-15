
def construct_tweet_link(company_handle, positive=False, hashtags = ['supplychain','transparency','modernslavery','forcedlabor','informedpurchases'], text="Share supply chain", website = "slaveryincluded.org"):

    base = "https://platform.twitter.com/widgets/tweet_button.html?size=l&"

    url_string = "url=https%3A%2F%2F" + website

    company_construct = "&via=" + company_handle
    part_00 = "&related=twitterapi%2Ctwitter&text="

    text = text.replace(" ", "%20")
    
    tag_string = "&hashtags="
    tag_string = tag_string + '%2C'.join(hashtags)


    full_string = base  + url_string+ company_construct + part_00 + text + tag_string 
    return str(full_string)
