import pandas as pd
from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF, RDFS, BNode
import rltk
import json
import re
import math

ingredient = pd.read_json('./output/ingredients.jl', lines=True)

with open('./output/compounds.jl') as fp:
  compound = [json.loads(line) for line in fp.read().split('\n') if line!='']

compound_dict = {str(int(line['chem_id'])): line for line in compound}

compound = pd.read_json('./output/compounds.jl', lines=True)


# chemclass = {'natural rubber': ['latex'], 
#              'fragrance': ['Amyl cinnamal', 'Amylcinnamyl alcohol', 'Anisyl alcohol', 'Benzyl alcohol', 'Benzyl benzoate',
#                            'Benzyl cinnamate', 'Benzyl salicylate', 'Cinnamyl alcohol', 'Cinnamaldehyde', 'Citral',
#                            'Citronellol', 'Coumarin', 'Eugenol', 'Farnesol', 'Geraniol', 'Hexyl cinnamaladehyde',
#                            'Hydroxycitronellal', 'Hydroxyisohexyl 3-cyclohexene carboxaldehyde (HICC), (also known as Lyral)',
#                            'Isoeugenol', 'Lilial', 'd-Limonene', 'Linalool', 'Methyl 2-octynoate', 'g-Methylionone', 'Oak moss extract', 'Tree moss extract'], 
#              'preservative': ['Methylisothiazolinone', 'Methylchloroisothiazolinone', 'Bronopol', 'Diazolidinyl urea', 'DMDM hydantoin', 'Imidazolidinyl urea', 'Sodium hydroxymethylglycinate'], 
#              'alcoholic': ['']
#              'dyes': ['p-phenylenediamine', 'Coal-tar'], 
#              'metal': ['Gold', 'Nickel'], 
#              'vitaminC': ['vitamin c'], 
#              'glycolic': ['glycolic acid'],
#              'lactic': ['lactic acid'], 
#              'mandelic': ['mandelic acid'], 
#              'tartaric': ['tartartic acid'], 
#              'malic': ['malic acid'], 
#              'citric': ['citric acid'],
#              'salicylic': ['salicylic acid'], 
#              'retinol': ['retinol', 'vitamin a'], 
#              'niacinamide': ['niacinamide'], 
#              'benzoic': ['benzoic acid']}


# buildingggg GRAPH

foaf = Namespace('http://xmlns.com/foaf/0.1/')
schema = Namespace('http://schema.org/')
owl = Namespace('http://www.w3.org/2002/07/owl#')
myns = Namespace('http://inf558.org/chemcosmetic/')

kgraph = Graph()
kgraph.bind('foaf', foaf)
kgraph.bind('schema', schema)
kgraph.bind('myns', myns)

# define CLASS to graph
# compound class
comp = URIRef(myns['Compound'])
kgraph.add((comp, RDF.type, schema['Class']))
kgraph.add((comp, owl['sameAs'], XSD.string))
kgraph.add((comp, myns['formula'], XSD.string))
kgraph.add((comp, myns['synonym'], XSD.string))
kgraph.add((comp, myns['groupOf'], myns['ChemGroup']))
kgraph.add((comp, myns['hasAttribute'], myns['Safety']))
kgraph.add((comp, myns['hasFunction'], myns['Function']))
kgraph.add((comp, myns['acne'], XSD.integer))
kgraph.add((comp, myns['irritant'], XSD.integer))
kgraph.add((comp, myns['safety'], XSD.integer))

# safety class
ssafety = URIRef(myns['Safety'])
kgraph.add((ssafety, RDF.type, schema['Class']))
kgraph.add((ssafety, RDFS.label, Literal('Safety')))

# chemical group class
group = URIRef(myns['ChemGroup'])
kgraph.add((group, RDF.type, schema['Class']))
kgraph.add((group, RDFS.label, Literal('Chemical Group')))

# function class
func = URIRef(myns['Function'])
kgraph.add((func, RDF.type, schema['Class']))
kgraph.add((func, RDFS.label, Literal('Function')))

# define PROPERTY to graph
# formula property
formula = URIRef(myns['formula'])
kgraph.add((formula, RDF.type, schema['Property']))
kgraph.add((formula, RDFS.label, Literal('formula')))
kgraph.add((formula, schema['domainIncludes'], myns['Compound']))
kgraph.add((formula, schema['rangeIncludes'], XSD.string))

# synonym property
syn = URIRef(myns['synonym'])
kgraph.add((syn, RDF.type, schema['Property']))
kgraph.add((syn, RDFS.label, Literal('synonym')))
kgraph.add((syn, schema['domainIncludes'], myns['Compound']))
kgraph.add((syn, schema['rangeIncludes'], XSD.string))

# groupOf property
groupof = URIRef(myns['groupOf'])
kgraph.add((groupof, RDF.type, schema['Property']))
kgraph.add((groupof, RDFS.label, Literal('is group of')))
kgraph.add((groupof, schema['domainIncludes'], myns['Compound']))
kgraph.add((groupof, schema['rangeIncludes'], myns['ChemGroup']))

# hasAttribute property
hasattr = URIRef(myns['hasAttribute'])
kgraph.add((hasattr, RDF.type, schema['Property']))
kgraph.add((hasattr, RDFS.label, Literal('has attribute')))
kgraph.add((hasattr, schema['domainIncludes'], myns['Compound']))
kgraph.add((hasattr, schema['rangeIncludes'], myns['Safety']))

# hasFunction property
hasfun = URIRef(myns['hasFunction'])
kgraph.add((hasfun, RDF.type, schema['Property']))
kgraph.add((hasfun, RDFS.label, Literal('has function')))
kgraph.add((hasfun, schema['domainIncludes'], myns['Compound']))
kgraph.add((hasfun, schema['rangeIncludes'], myns['Function']))

# acne
acne = URIRef(myns['acne'])
kgraph.add((acne, RDF.type, schema['Property']))
kgraph.add((acne, RDFS.label, Literal('acne')))
kgraph.add((acne, schema['domainIncludes'], myns['Compound']))
kgraph.add((acne, schema['rangeIncludes'], XSD.integer))

# irritant
irritant = URIRef(myns['irritant'])
kgraph.add((irritant, RDF.type, schema['Property']))
kgraph.add((irritant, RDFS.label, Literal('irritant')))
kgraph.add((irritant, schema['domainIncludes'], myns['Compound']))
kgraph.add((irritant, schema['rangeIncludes'], XSD.integer))

# safety
safety = URIRef(myns['safety'])
kgraph.add((safety, RDF.type, schema['Property']))
kgraph.add((safety, RDFS.label, Literal('safety')))
kgraph.add((safety, schema['domainIncludes'], myns['Compound']))
kgraph.add((safety, schema['rangeIncludes'], XSD.integer))

safety = URIRef(myns['conflictWith'])
kgraph.add((safety, RDF.type, schema['Property']))
kgraph.add((safety, RDFS.label, Literal('conflict with')))
kgraph.add((safety, schema['domainIncludes'], myns['ChemGroup']))
kgraph.add((safety, schema['rangeIncludes'], myns['ChemGroup']))

# build Chemical Group
chemclass = {'VitaminC': ['vitamin c'], 
             'Glycolic': ['glycolic acid'],
             'Lactic': ['lactic acid'], 
             'Mandelic': ['mandelic acid'], 
             'Tartaric': ['tartartic acid'], 
             'Malic': ['malic acid'], 
             'Citric': ['citric acid'],
             'Salicylic': ['salicylic acid'], 
             'Retinol': ['retinol', 'vitamin a', 'retinoic acid'], 
             'Niacinamide': ['niacinamide'], 
             'Benzoic': ['benzoic acid'],
             'Alcoholic':['ethyl alcohol','methanol','isopropyl alcohol','benzyl alcohol','alcohol denat']}

# 雙向/單向?

kgraph.add((myns['VitaminC'], myns['conflictWith'], myns['Lactic']))
kgraph.add((myns['VitaminC'], myns['conflictWith'], myns['Salicylic']))
kgraph.add((myns['VitaminC'], myns['conflictWith'], myns['Glycolic']))

kgraph.add((myns['Retinol'], myns['conflictWith'], myns['Lactic']))
kgraph.add((myns['Retinol'], myns['conflictWith'], myns['Salicylic']))
kgraph.add((myns['Retinol'], myns['conflictWith'], myns['Glycolic']))
kgraph.add((myns['Retinol'], myns['conflictWith'], myns['VitaminC']))

kgraph.add((myns['Glycolic'], myns['conflictWith'], myns['Salicylic']))
kgraph.add((myns['Niacinamide'], myns['conflictWith'], myns['VitaminC']))



for g in chemclass.keys():
    gURI = URIRef(myns[g])
    kgraph.add((gURI, RDF.type, myns['ChemGroup']))
    kgraph.add((gURI, RDFS['label'], Literal(g)))


# build Safety
safetySet = set()
for s in compound.safety:
    safetySet.update(s)

for s in safetySet:
    sURI = URIRef(myns[s.replace(' ', '')])
    kgraph.add((sURI, RDF.type, myns['Safety']))
    kgraph.add((sURI, RDFS['label'], Literal(s)))

# build Function
funcSet = set()
for i in ingredient.function:
    if i: funcSet.update(i)

for i in funcSet:
    iURI = URIRef(myns[i.replace(' ', '')])
    kgraph.add((iURI, RDF.type, myns['Function']))
    kgraph.add((iURI, RDFS['label'], Literal(i)))

# chemchem = ingredient[ingredient['chem_id'].notnull()]

# chemchem.drop_duplicates(subset ="chem_id", keep = 'first', inplace = True) 
# nonechem = ingredient[ingredient['chem_id'].isnull()]
# nonechem = nonechem[ingredient['name'] != 'or']
# nonechem = nonechem[ingredient['name'] != 'NATURAL FRAGRANCE']

# ingredient = pd.concat([chemchem, nonechem],ignore_index=True)

# def uriGenerator(string):
#     n = '_'.join([ s for s in re.split('[, ]', re.sub('[^0-9a-zA-Z]+', '_', string.lower())) if len(s) != 0])
#     return '_'.join([s for s in n.split('_') if len(s)!=0])

compSet = set()

for index, row in ingredient.iterrows():
    # uriname = uriGenerator(row['name'])
    uriname = 'chem' + row['ingredient_id']
    if uriname in compSet: 
        continue
    else:
        compSet.add(uriname)
        # this = URIRef(myns['CHEM_'+uriname])
        this = URIRef(myns[uriname])
        kgraph.add((this, RDF.type, myns['Compound']))
        kgraph.add((this, foaf['name'], Literal(row['name'].title())))
        
        if row['function']:
            for f in row['function']:
                kgraph.add((this, myns['hasFunction'], myns[f.replace(' ', '')]))
        
        if row['acne']:
            for a in row['acne']:
                kgraph.add((this, myns['acne'], Literal(a, datatype=XSD.integer)))
        
        if row['irritant']:
            for i in row['irritant']:
                kgraph.add((this, myns['irritant'], Literal(i, datatype=XSD.integer)))
            
        if row['safety']:
            for s in row['safety']:
                kgraph.add((this, myns['safety'], Literal(s, datatype=XSD.integer)))
        
        # if row['chem_id']>0:
        if not math.isnan(row['chem_id']):
            chemid = str(int(row['chem_id']))
            kgraph.add((this, owl['sameAs'], Literal(compound_dict[chemid]['chem_url'])))
            kgraph.add((this, myns['formula'], Literal(compound_dict[chemid]['formula'])))

            for i in compound_dict[chemid]['safety']:
                kgraph.add((this, myns['hasAttribute'], myns[i.replace(' ', '')]))
            
            for i in compound_dict[chemid]['synonyms']:
                kgraph.add((this, myns['synonym'], Literal(i)))
                for g, l in chemclass.items():
                    matching = [ ll for ll in l if ll.lower() in i.lower()]
                    # print(matching)
                    if len(matching) > 0:
                        kgraph.add((this, myns['groupOf'], myns[g]))        
        else:
            for g, l in chemclass.items():
                matching = [ ll for ll in l if ll.lower() in row['name'].lower()]
                if len(matching) > 0:
                    kgraph.add((this, myns['groupOf'], myns[g]))

kgraph.serialize('./output/RDF_compounds.ttl', format="turtle")

# idss = []
# for i in chemchem.chem_id:
#     if i not in compound_dict: idss.append(i)


# from selenium import webdriver
# from bs4 import BeautifulSoup
# import time
# compfile = open('compound.jl', 'a')

# driver = webdriver.Chrome('./chromedriver')

# for i in ids:
#     comp = 'https://pubchem.ncbi.nlm.nih.gov/compound/%s'%i
#     driver.get(comp)
#     compid = comp.split('/')[-1]
#     time.sleep(2.5)
#     response = BeautifulSoup(driver.page_source, 'html.parser') 
#     sysSet = set()
#     for r in response.select('section#Synonyms section'): 
#         sysSet.update(set([rr.text for rr in r.select('div.columns p')]))

#     rows = response.select('div.summary tr')
#     formula = ''
#     safety = []
#     for row in rows:
#         if row.select('th') and row.select('th')[0].text == 'Molecular Formula:':
#             formula = row.select('td a span')[0].text     
#         if row.select('th') and row.select('th')[0].text == 'Chemical Safety:':    
#             safety = [ s.get('data-caption') for s in row.select('td a p div')]    
#     compinfo = {'chem_id': compid, 'chem_url': comp, 'safety': safety, 'formula': formula, 'synonyms':list(sysSet)}            
#     compfile.write(json.dumps(compinfo) + '\n')
#     compfile.flush()


