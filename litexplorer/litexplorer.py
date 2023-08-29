
from Bio import Entrez
import pandas as pd
from .models import docdb
#import graph_tool.all as gt
def check_id(id):
  if not isinstance(id, str):
    print("ID is not a string: ", type(id))
    return ""
  if len(id) <= 4:
    print("Too short ID: " , id )
    return ""

  if id[0:3] == "PMC" :
    id = id[3:]
  return id
"""
def get_alt_ids(id, db = 'pmc'):

    id = check_id(id)
    if db == 'pmc':
      link = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pmc&id=' + id
      with open(wget.download(link)) as xmlFile:
        try:
          dataDict = xmltodict.parse(xmlFile.read())
          pmid = dataDict.get('eLinkResult').get('LinkSet').get('LinkSetDb')[0].get('Link').get('Id')
          return pmid
        except:
          return None


    return None

"""
#For context of link builder see  this link https://www.ncbi.nlm.nih.gov/pmc/tools/cites-citedby/
#This function takes a PMC Id and searches Pubmed Central (PMC) for all articles it cited
def get_parents(id, db = 'pmc'):
  link_list = []
  id = check_id(id)
  try:
    links = Entrez.elink(dbfrom=db, id=id, linkname="pmc_pmc_cites")

    record = Entrez.read(links)
  #print(record)

    records = record[0][u'LinkSetDb'][0][u'Link']
  except:
    print("couldn't get parents for pmcid:", id)
    return [None]
  for link in records:
    link_list.append("PMC" + link[u'Id'])

  return link_list

#For context of link builder see  this link https://www.ncbi.nlm.nih.gov/pmc/tools/cites-citedby/
#This function takes a PMC Id and searches Pubmed Central (PMC) for all articles that cited the given PMC Id
def get_children(id, db = "pmc"):
  link_list = []
  id = check_id(id)
  try:
    links = Entrez.elink(dbfrom='pubmed', id=id, linkname="pmc_pmc_citedby")
    record = Entrez.read(links)


    records = record[0][u'LinkSetDb'][0][u'Link']
  except:
    print("couldn't get children for for pmcid:", id)
    return [None]
  for link in records:
    link_list.append("PMC" + link[u'Id'])

  return link_list
def get_similiar(id, n = 20):
  link_list = []
  id = check_id(id)
  links = Entrez.elink(dbfrom="pmc", db= "pmc", id=id, cmd="neighbor_score")
  record = Entrez.read(links)
  #print(record)
  try:
    records = record[0][u'LinkSetDb'][0][u'Link']
    for link, limit in zip(records, range(n)):
      link_list.append({"PMC" + link[u'Id']: link[u'Id'].values() })
  except Exception as e:
    print(e)
    print("couldn't get similiar for pmcid:", id)
    return [None]
  return link_list
def get_medline(id, db = 'pmc'):
  try:
    if db == 'pmc':
      handle = Entrez.efetch(db=db, id=id, retmode='text', rettype='medline')
      record = handle.read()


    if len(record) == 0:
      return None
    lsOfStr = [""]
    for i in record.splitlines():
      if len(i) > 0:
        if i[0]!=" ":
          lsOfStr.append(i)
        else:
         lsOfStr[len(lsOfStr) - 1] += " " + i.strip()
    pmcid, pmid, title, abstract = None, None, None, None

    authors = []
    for i in lsOfStr:
      #print (i)
      if len(i) > 4:
        if i[0:3] == "PMC":
          pmcid = i.split('-', 1)[1].strip()
          #print(pmcid)
        elif i[0:4] == "PMID":
          pmid = i.split('-', 1)[1].strip()
          #print(pmid)
        elif i[0:2] == "TI":
          title = i.split('-', 1)[1].strip()
          #print(title)
        elif i[0:2] == "AB":
          abstract = i.split('-', 1)[1].strip()
          #print(abstract)
        elif i[0:3] == "FAU":
          authors.append(i.split('-', 1)[1].strip())
          #print(authors)
    return [pmcid, pmid, title, abstract, authors]
  except:
    print("Couldn't get medline for id=", id)
    return [None,None,None,None,None]
"""
def build_cite_graph(citeDf):
  citeDf
  edgeLs = []
  ids = citeDf.PMCID.values
  parents = citeDf.Parents.values
  children = citeDf.Children.values

  g = gt.Graph()
  for i in range(len(ids)):
    for parent in parents[i]:
      if (parent != None):
          edgeLs  += [[parent, ids[i]]]
    for child in children[i]:
        if (child != None):
          edgeLs  += [[ids[i], child]]

  g = gt.Graph()

  node_id = g.add_edge_list(edgeLs, hashed=True)
  vTitle = g.new_vp("string")
  vAbstract = g.new_vp("string")
  vAuthors = g.new_vp("string")
  for node in range(g.num_vertices()):
    try:
      vTitle[node] = citeDf.at[node_id[node], "Title"]
      vAbstract[node] = citeDf.at[node_id[node], "Abstract"]
      vAuthors[node] = citeDf.at[node_id[node], "Authors"]
    except Exception as e:
      pass

  g.vertex_properties['PMCID'] = node_id
  g.vertex_properties['Title'] = vTitle
  g.vertex_properties['Abstract'] = vAbstract
  g.vertex_properties['Authors'] = vAuthors
  return g


#Takes CiteDataFrame, Returns Directional Vertex Graph of Citations

"""
def build_cite_df(citeDf,degrees):
  for i in range(degrees):

    parentIds = citeDf[citeDf.Degree == i].Parents.values[0]
    #print(parentIds)
    childrenIds = citeDf[citeDf.Degree == i].Children.values[0]
    #print(childrenIds)

    lstOfIds = parentIds+childrenIds

    #print(i)
    #print(lstOfIds)
    if len(lstOfIds) > 0:

      for j in lstOfIds:
        if j != None:
          #print(j)
          if j not in citeDf['PMCID']:
              medline = get_medline(j)
              if medline[0] != None:
                citeDf.at[j, 'PMCID'] = medline[0]
                citeDf.at[j, 'isValidId'] = True
                citeDf.at[j, 'PMID'] = medline[1]
                citeDf.at[j, 'Title'] =medline[2]
                citeDf.at[j, 'Abstract'] =medline[3]
                citeDf.at[j, 'Authors'] =medline[4]
                citeDf.at[j, 'Degree']  = i+1
                if (citeDf.at[j,'isValidId']) and (i < degrees-1):
                  citeDf.at[j, 'Parents'] = get_parents(j)
                  citeDf.at[j, 'Children'] = get_children(j)

                else:
                  citeDf.at[j, 'Parents'] = [None]
                  citeDf.at[j, 'Children'] = [None]

                if citeDf.at[j, 'Parents'][0] != None:
                  citeDf.at[j, 'NumParents'] = len(citeDf.at[j, 'Parents'])
                else:
                  citeDf.at[j, 'NumParents'] = 0
                if citeDf.at[j, 'Children'][0] != None:
                  citeDf.at[j, 'NumChildren'] = len(citeDf.at[j, 'Children'])
                else:
                  citeDf.at[j, 'NumChildren'] = 0


              else:
                citeDf.at[j,'isValidId'] = False

  return citeDf[citeDf.isValidId]

def start(root):
    degrees = 2
    Entrez.email = "joe.hardin369@gmail.com"
    rootDf = pd.DataFrame(columns=["PMCID",  # Primary Key/ Index Pubmed Central
                                   "PMID",  # Pubmed
                                   "isValidId",  # Boolean.  Did we find any record of this on Pubmed
                                   "Title",  # If we did, string value indicating title.  If not found None or NaN
                                   "Abstract",  # string value indicating fetched Abstract.  If not found None or NaN
                                   "Authors",  # List of Strings of Authors
                                   "Degree",
                                   # Degrees from root.  Root is 0, its parents and children are 1, theirs are 2 if they aren't 1, etc.
                                   "Parents",  # Articles this specific article cited in PMC database
                                   "NumParents",  # Number of Parents
                                   "Children",
                                   # Articles this specific article was cited by in later articles on PMC database
                                   "NumChildren"  # Number of children
                                   ])
    # rootDf.set_index('PMCID', inplace = True)
    docdb.objects.all().delete()
    medline = get_medline(root)
    rootDf.at[root, 'PMCID'] = medline[0]

    if (medline[0] is None) or (medline[0].lower() != root.lower() ):
        x = docdb(pmcid = root, isValidId= False )
        x.save()
        return
    if medline[0] is not None:  # and medline[0].lower() == root.lower() :

        rootDf.at[root, 'isValidId'] = True
        rootDf.at[root, 'PMID'] = medline[1]
        rootDf.at[root, 'Title'] = medline[2]
        rootDf.at[root, 'Abstract'] = medline[3]
        rootDf.at[root, 'Authors'] = medline[4]
        rootDf.at[root, 'Degree'] = 0
        parents = get_parents(root)
        children = get_children(root)
        if parents[0] is not None:
            parentlen = len(parents)
        else:
            parentlen = 0
        if children[0] is not None:
            childrenlen = len(children)
        else:
            childrenlen = 0

        x = docdb(pmcid=medline[0],
                  pmid=medline[1],
                  isValidId=True,
                  title = medline[2],
                  abstract = medline[3],
                  author = medline[4],
                  degree = 0,
                  parents= parents,
                  children= children,
                  numparents= parentlen,
                  numchildren= childrenlen
        )
        x.save()
        print(docdb.objects.all().values())




