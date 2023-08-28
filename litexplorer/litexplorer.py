


def trythis(id):
    print("ID is:", id)

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


def start(root):
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
    medline = get_medline(root)
    rootDf.at[root, 'PMCID'] = medline[0]

    if medline[0] != None:  # and medline[0].lower() == root.lower() :

        rootDf.at[root, 'isValidId'] = True
        rootDf.at[root, 'PMID'] = medline[1]
        rootDf.at[root, 'Title'] = medline[2]
        rootDf.at[root, 'Abstract'] = medline[3]
        rootDf.at[root, 'Authors'] = medline[4]
        rootDf.at[root, 'Degree'] = 0
        rootDf.at[root, 'Parents'] = get_parents(root)
        rootDf.at[root, 'Children'] = get_children(root)
        if rootDf.at[root, 'Parents'][0] != None:
            rootDf.at[root, 'NumParents'] = len(rootDf.at[root, 'Parents'])
        else:
            rootDf.at[root, 'NumParents'] = 0
        if rootDf.at[root, 'Children'][0] != None:
            rootDf.at[root, 'NumChildren'] = len(rootDf.at[root, 'Children'])
        else:
            rootDf.at[root, 'NumChildren'] = 0



    else:
        rootDf.at[root, 'isValidId'] = False
