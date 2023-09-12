
from Bio import Entrez
from .models import docdb, citedb, iddb
from time import time

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
    st = time()
    roots = iddb.objects.all().filter(degree=degree)
    if len(roots) < 1:
        return
    ids = []
    for i in roots:
        ids.append(check_id(getattr(i, "pmcid")))
    # print(ids)
    links = Entrez.elink(dbfrom=db, id=ids, linkname="pmc_pmc_cites")

    records = Entrez.read(links)
    print("Time it takes to fetch children records", time() - st)
    st = time()
    newIds = []
    if len(records) == 0:
        print("No child records found")
        return
    # print("In Records")
    # print(records)
    clist = []
    for record, child in zip(records, roots):
        if len(record[u'LinkSetDb']) > 0:


            for link in record[u'LinkSetDb'][0][u'Link']:
                # print(link)
                try:
                    newIds.append(iddb(pmcid="PMC" + link[u'Id'], degree=degree + 1))
                    clist.append(child)
                except Exception as e:
                    print("Couldn't get children for PMC", getattr(child, "pmcid"))
                    print(e)

    # print(datas)
    plist = iddb.objects.bulk_create(newIds, ignore_conflicts=True)
    # example = iddb.objects.filter(pmcid=set(plist))
    print("Parent list ", len(plist), "  ", plist[0])
    print("Child list ", len(clist), "  ", clist[0])

    print("Time it takes to add parent records to iddb", time() - st)
    x = citedb()
    for parent, child in zip(plist, clist):
        try:
            x = citedb(parent=parent, child=child)
            x.save()
        except:
            pass

    print("Time it takes to add parent records to citedb", time() - st)
    return

#For context of link builder see  this link https://www.ncbi.nlm.nih.gov/pmc/tools/cites-citedby/
#This function takes a PMC Id and searches Pubmed Central (PMC) for all articles that cited the given PMC Id
def get_children(degree, db = 'pmc'):
    #st = time()
    roots = iddb.objects.all().filter(degree=degree)
    if len(roots) < 1:
        return
    ids = []
    for i in roots:
        ids.append(check_id(getattr(i, "pmcid")))
    #print(ids)
    links = Entrez.elink(dbfrom=db, id=ids, linkname="pmc_pmc_citedby")

    records = Entrez.read(links)
    #print("Time it takes to fetch children records", time() - st)
    #st = time()
    newIds = []
    if len(records) == 0:
        print("No child records found")
        return
    #print("In Records")
    #print(records)
    plist = []
    clist = []
    for record, parent in zip(records, roots):
        if len(record[u'LinkSetDb']) > 0:

            parentid = parent.pmcid
            for link in record[u'LinkSetDb'][0][u'Link']:
                #print(link)
                try:
                    newIds.append(iddb(pmcid="PMC" + link[u'Id'], degree= degree+1))
                    plist.append(parent)
                    clist.append("PMC" + link[u'Id'])
                except Exception as e:
                    print("Couldn't get children for PMC", getattr(parent, "pmcid"))
                    print(e)

    #print(datas)
    clist = iddb.objects.bulk_create(newIds, ignore_conflicts= True)
    #example = iddb.objects.filter(pmcid=set(plist))


    #print("Time it takes to add children records to iddb", time() - st)
    x = citedb()
    for parent, child in zip(plist,clist):
        try:
            x = citedb(parent = parent, child= child)
            x.save()
        except:
            pass

    #print("Time it takes to add children records to citedb", time() - st)
    return

def get_medline(db = 'pmc'):
    st = time()
    print("Starting medline")
    id = list(iddb.objects.values_list('pmcid', flat=True))

    for i in range(len(id)):
        id[i] = check_id(id[i])
    if db == 'pmc':
      handle = Entrez.efetch(db=db, id=id, retmode='text', rettype='medline')

      records = str(handle.read()).split('\n\n')
      #print(records)

    else:
        return

    medlist = []
    #print("Time to fetch record", time() - st)
    for record, id in zip(records, iddb.objects.all()):
        st = time()
        if len(record) == 0:
            print("Couldn't get medline for ", id)
            continue
        lsOfStr = [""]
        authors = []
        pmcid, title, abstract = None, None, None
        for i in record.splitlines():
            if len(i) > 0:
                if i[0] != " ":
                    lsOfStr.append(i)
                else:
                    lsOfStr[len(lsOfStr) - 1] += " " + i.strip()
        for i in lsOfStr:
            # print (i)
            if len(i) > 4:
                if i[0:3] == "PMC":
                    pmcid = i.split('-', 1)[1].strip()
                    #print("Id fetched is ", pmcid, " id I thought it should be is ", id, "And it evaluates as", pmcid == id.pmcid)

                elif i[0:2] == "TI":
                    title = i.split('-', 1)[1].strip()
                    # print(title)
                elif i[0:2] == "AB":
                    abstract = i.split('-', 1)[1].strip()
                    # print(abstract)
                elif i[0:3] == "FAU":
                    authors.append(i.split('-', 1)[1].strip())
                    # print(authors)


        if pmcid == id.pmcid:
            id.isValidId = True
            id.save()
            x = docdb(pmcid= id, title= title, abstract=abstract, author=authors)
            x.save()

        authors = []
        title = ""
        abstract = ""


        #print("Time to parse", time() - st)
       #medlist.append([id, title, abstract, authors])
    #print(medlist)
    return
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



def start(root):
    degrees = 1
    Entrez.email = "joe.hardin369@gmail.com"

    deletedb()

    iddb(pmcid=root, degree=0).save()
    st = time()
    for d in range(degrees):
        get_children(d)
        print("got children for ", d, " in ", time()-st)
        st = time()
        get_parents(d)
        print("got parents for ", d, " in ", time() - st)
        st = time()

    get_medline()
    iddb.objects.filter(isValidId=False).delete()
    numRel = len(iddb.objects.all())
    if numRel == 0:
        return [False]
    else:
        rootrec = docdb.objects.get(pmcid=root)
        return [True, rootrec.title, str(numRel)]





def deletedb():
    docdb.objects.all().delete()
    iddb.objects.all().delete()
    citedb.objects.all().delete()