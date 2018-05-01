from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_colwidth', -1)

def get_article_elements( url ):
    soup = BeautifulSoup( urllib.request.urlopen( url ), "html.parser")

    title = soup.find("meta",  property="og:title")

    #site_name = soup.find("meta",  property="og:site_name")
    #if site_name == []:
     #   site_name = soup.find( )

     
def ibm_query_to_html( df,ibm_string):
    # Remove unnecessary index.
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Combine title and link into href.
    def href_format(row):
        href = '<a href="{0}" target="_blank">{1}</a>' 
        return href.format(row['URL'], row['Title'])
    df['Article'] = df.apply(href_format, axis=1)

    # Drop Precision.
    df['Relevance'] = df['Relevance'].apply(lambda x: '{}'.format(round(float(x))))
    
    # Remove title and link.
    df.drop(columns=['Title', 'URL'], inplace=True)

    #df['Relevance'] = '{:.1f}'.format(float(df['Relevance']))
    df_html_output =  ''.join(df.to_html(escape=False,
                              columns=[ 'Article', 'Source','Sentiment', 'Relevance'],
                              index=False))
    #df_html_output = df_html_output.replace('<t>','<th style = "background-color: red">')
    return df_html_output
    
    """
    # Turn df to html to single string.
    return ''.join(df.to_html(escape=False,
                              columns=['Sentiment', 'Article', 'Source', 'Relevance'],
                              index=False, justify="center"))
    """
