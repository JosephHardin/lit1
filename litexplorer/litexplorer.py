
from Bio import Entrez
from .models import docdb, citedb, iddb
from time import time
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
def get_parents(degree, db = 'pmc'):
    roots = iddb.objects.all().filter(degree=degree)
    if len(roots) < 1:
        return
    ids = []
    for i in roots:
        ids.append(check_id(getattr(i, "pmcid")))
    print(ids)
    links = Entrez.elink(dbfrom=db, id=ids, linkname="pmc_pmc_cites")

    records = Entrez.read(links)

    if len(records) > 0:
        print("In Records")
        print(records)
        for record, child in zip(records, roots):
            if len(record[u'LinkSetDb']) > 0:
                for link in record[u'LinkSetDb'][0][u'Link']:
                    print(link)
                    try:
                        childId = "PMC" + link[u'Id']
                        if iddb.objects.filter(pmcid=childId).exists():
                            parent = iddb.objects.get(pmcid=childId)
                        else:
                            newid = iddb(pmcid=childId, degree=degree + 1)
                            newid.save()
                            parent = iddb.objects.get(pmcid=childId)

                        x = citedb(child=child, parent=parent)
                        x.save()
                    except Exception as e:
                        print("Couldn't get children for PMC", getattr(child, "pmcid"))
                        print(e)
    return

#For context of link builder see  this link https://www.ncbi.nlm.nih.gov/pmc/tools/cites-citedby/
#This function takes a PMC Id and searches Pubmed Central (PMC) for all articles that cited the given PMC Id
def get_children(degree, db = 'pmc'):
    roots = iddb.objects.all().filter(degree=degree)
    if len(roots) < 1:
        return
    ids = []
    for i in roots:
        ids.append(check_id(getattr(i, "pmcid")))
    print(ids)
    links = Entrez.elink(dbfrom=db, id=ids, linkname="pmc_pmc_citedby")

    records = Entrez.read(links)

    if len(records) > 0:
        print("In Records")
        print(records)
        for record, parent in zip(records, roots):
            if len(record[u'LinkSetDb']) > 0:
                for link in record[u'LinkSetDb'][0][u'Link']:
                    print(link)
                    try:
                        childId = "PMC" + link[u'Id']
                        if iddb.objects.filter(pmcid=childId).exists():
                            child = iddb.objects.get(pmcid=childId)
                        else:
                            newid = iddb(pmcid=childId, degree=degree+1)
                            newid.save()
                            child = iddb.objects.get(pmcid=childId)

                        x = citedb(child=child, parent=parent)
                        x.save()
                    except Exception as e:
                        print("Couldn't get children for PMC", getattr(parent, "pmcid"))
                        print(e)
    return
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
  st = time()
  print("Starting medline")
  try:
    if db == 'pmc':
      handle = Entrez.efetch(db=db, id=id, retmode='text', rettype='medline')
      record = handle.read()

    print("Time to fetch record", time() - st)
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
    print("Time to parse", time() - st)
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
def build_citedb(degrees):
    start = time()
    for i in range(degrees):
        print("Now working on degree", i)
        idset = {}
        for e in docdb.objects.all().filter(degree=i):
            end = time()
            print("Start of loop 1", end-start)
            parentIds = citedb.objects.all().filter(parents = e.pmcid)
            childrenIds = e.children.replace("'","").strip("][").split(",")
            lstOfIds = parentIds + childrenIds
            #print(lstOfIds)
            if len(lstOfIds) > 0:
                for j in lstOfIds:
                    j = j.strip()
                    if not docdb.objects.filter(pmcid=j).exists():
                        idset.add(j.strip())
                #print(j)
        print(idset)

        medline = get_medline(j)
        end = time()
        print("Just got medline", end-start)
        #if medline[0] != None:
        if i < degrees-1:
          parents = get_parents(j)
          children = get_children(j)

        else:
          parents= [None]
          children= [None]

        if parents[0] is not None:
          numParents = len(parents)
        else:
          numParents = 0
        if children[0] is not None:
          numChildren = len(children)
        else:
          numChildren = 0
        swrite = time()
        try:
            x = docdb(pmcid=medline[0],
                pmid=medline[1],
                isValidId=True,
                title=medline[2],
                abstract=medline[3],
                author=medline[4],
                degree=i+1,
                parents=parents,
                children=children,
                numparents=numParents,
                numchildren=numChildren
                )
            x.save()
            ewrite = time()
            print("It took this long to write to the database", ewrite-swrite)
        except Exception as k:
            print(medline)
            print(k)


    print("done")
    return



def start(root):
    degrees = 0
    Entrez.email = "joe.hardin369@gmail.com"

    deletedb()
    medline = get_medline(root)

    if (medline[0] is None) or (medline[0].lower() != root.lower()):
        iddb(pmcid=root, isValidId=False, degree= 0).save()
        return

    x = iddb(pmcid=medline[0], isValidId=True, degree=0)
    x.save()
    y = docdb(x,
              title=medline[2],
              abstract=medline[3],
              author=medline[4],
             )
    y.save()
    x = iddb(pmcid=medline[0], isValidId=True, degree=0)
    x.save()


    get_children(0)
    get_parents(0)
    print(iddb.objects.all().values())
    print(docdb.objects.all().values())
    print(citedb.objects.all().values())
    #print(citedb.objects.all())



    #print(docdb.objects.all().values())
    #build_citedb(degrees)



def deletedb():
    docdb.objects.all().delete()
    iddb.objects.all().delete()
    citedb.objects.all().delete()