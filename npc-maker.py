"""
Scraper for NPC (non-player-character) ideas from DMTools.

Generates a list of generic NPCs from D&D from the NPC idea generator
found at DMTools.
"""

from collections import OrderedDict
import requests
import bs4  # Beautiful Soup


def make_npc_list(count:int=30, filename:str='npc_list.txt'):
    """
    Creates a list of NPCs by scraping from the DM Tools website.

    Imperative core that brings together the functional style subsections.

    Args:
        - count (30) = 30: A count NPCs for the generated list.
        - filename (str) = 'npc_list.txt': The filename to output the result at

    Returns:
        - None

    Side Effects:
        - Generates a file of NPCs
    s
    """
    results = list()
    while len(results) < count:
        html = get_npcs()
        for npc in html:
            data = clean_npc_data(npc)
            if data is not None:
                results.append(data)

    with open(filename, 'w') as file:
        for npc in results[:count]:
            file.writelines(f'# : {results.index(npc) + 1}\n')
            for key, value in npc.items():
                file.writelines(f'{key} : {value}\n')
            file.writelines('DM Notes: ' + '_'*80)
            file.writelines('\n' * 2)


def get_npcs():
    """Load the DMTools NPC idea page and scrape the NPCs into a list."""
    page = requests.get('http://www.dmtools.org/gens.php?nav=idea')
    page.raise_for_status()  # Asserts the page loaded
    soup = bs4.BeautifulSoup(page.text, "lxml")
    return list(soup.find_all('div', class_='grid_4'))

def clean_npc_data(npc_html):
    """
    Take the NPC data from DMTools and cleans it up into a dict.

    They ~usually~ use an html structure of "<b>heading</b>value".
    They're not very consistent with it though, so this function is a
    wee bit ugly.
    """
    npc = ordered_dict_from_tag(html=npc_html, tag='b')
    subheadings = ordered_dict_from_tag(html=npc_html, tag='i')

    unjoined_text = get_html_text(npc_html)
    text_list = join_list_items(list_=unjoined_text,symbol='/')

    npc = feed_list_into_dict(mylist=text_list, mydict=npc)

    if npc['Name'] is None:
        # There's some website brouhaha with weird name structures on some NPCs - toss those
        return None
    else:
        npc['Name'] = f"{npc['Name'][0]}; {' '.join(npc['Name'][1:])}"
        npc['Physical'] = dict(feed_list_into_dict(mylist=npc['Physical'],mydict=subheadings))
        return npc


def ordered_dict_from_tag(html, tag):
    """Create an ordered dict from the specified tag."""
    keys = [heading.text for heading in html.find_all(tag)]
    odict = OrderedDict.fromkeys(keys)
    return odict


def get_html_text(html):
    """
    Create a list of the tag texts, strip them, then filter the empties.
    """
    texts = html.find_all(text=True)
    texts = [text.strip() for text in texts]
    return list(filter(lambda text: text != '', texts))


def join_list_items(list_, symbol='/'):
    """
    Join list items when the symbol is found at certain parts of the element.

    Examples:
        >>> join_list_items(['a','/','b'], '/')
        ['a/b']
        >>> join_list_items(['d/','e'], '/')
        ['d/e']
        >>> join_list_items(['f','/g'], '/')
        ['f/g']
    """
    for i, item in enumerate(list_):
        if item == '/':
            list_[i - 1:i + 2] = [''.join(list_[i - 1:i + 2])]
        elif item.endswith('/'):
            list_[i:i+2] = [''.join(list_[i:i+2])]
        elif item.startswith('/'):
            list_[i-1:i+1] = [''.join(list_[i-1:i+1])]
    return list_


def feed_list_into_dict(mylist, mydict, start_key=None):
    """
    Take a list with embedded dict keys and streams them into the
    dict values.

    Examples:
        >>> d = OrderedDict([(1 , []), (2, []), (3, [])])
        >>> l = [1, 'A', 'B', 2, 'C', 3, 'D']
        >>> feed_list_into_dict(l, d)
        OrderedDict([(1, ['A', 'B']), (2, 'C'), (3, 'D')])

    """
    key = start_key

    for value in list(mylist):
        if value in mydict:
            key = value
        elif key is not None:
            if mydict[key] is None:
                mydict[key] = []
            mydict[key] += [value]

    for key in mydict.keys():
        try:
            if len(mydict[key]) == 1:
                mydict[key] = mydict[key][0]
        except Exception:
            continue

    return mydict

