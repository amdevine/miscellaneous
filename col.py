import sys, getopt, requests

def parseInput(argv):
    name = False
    rank = False
    fuzzy = False
    children = False
    try:
        opts, args = getopt.getopt(argv, "cfhn:r:", ["children", "fuzzy", "help", "name=", "rank="])
    except getopt.GetoptError:
        print('\nIncorrect arguments.\nUsage: col.py --name <scientific name> [--rank <taxonomic rank> --fuzzy --children --children]\n')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('\nUsage: col.py --name <scientific name> [--rank <taxonomic rank> --fuzzy --children]\n')
            sys.exit()
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-r", "--rank"):
            rank = arg
        elif opt in ("-f", "--fuzzy"):
            fuzzy = True
        elif opt in ("-c", "--children"):
            children = True

    return (name, rank, fuzzy, children)


def checkError(data):
    if data['error_message'] != "":
        print('\n{e}\n'.format(e=data['error_message']))
        sys.exit()

def checkRank(rank):
    ranks = [
        'Kingdom',
        'Phylum',
        'Class',
        'Order',
        'Superfamily',
        'Family',
        'Genus',
        'Species',
        'Infraspecies'
    ]
    if rank not in ranks:
        print('\nUnknown rank.\nPlease use one of the following ranks: {r}\n'.format(r=", ".join(ranks)))
        sys.exit(2)

def formatTaxname(tname):
    tname = tname.lower()
    taxname = tname[0].upper() + tname[1:]
    return taxname


def queryCOLRank(tname, taxrank):
    taxrank = taxrank.title()
    taxname = formatTaxname(tname)
    checkRank(taxrank)
    url = 'http://www.catalogueoflife.org/col/webservice'
    params = {
        'name': taxname,
        'format': 'json',
        'response': 'full',
    }
    r = requests.get(url, params).json()
    checkError(r)
    noMatches = True
    for result in r['results']:
        try:
            if result['name'] == taxname and result['rank'] == taxrank:
                print("\nName: {n} (Rank: {r})".format(n=result['name'], r=result['rank']))
                try:
                    for c in result['classification']:
                        print("{r}: {n}".format(r=c['rank'], n=c['name']))
                except KeyError:
                    print("No classification provided.")
                noMatches = False
                # sys.exit()
        except KeyError:
            pass
    if noMatches:
        print("\nSearch successful, but no exact matches found at rank = {r}.".format(r=taxrank))
        queryCOLFuzzy(taxname)
    print()
    sys.exit()


def queryCOLNoRank(tname):
    taxname = formatTaxname(tname)
    url = 'http://www.catalogueoflife.org/col/webservice'
    params = {
        'name': taxname,
        'format': 'json',
        'response': 'full',
    }
    r = requests.get(url, params).json()
    checkError(r)
    noMatches = True
    for result in r['results']:
        try:
            if result['name'] == taxname:
                print("\nName: {n} (Rank: {r})".format(n=taxname, r=result['rank']))
                try:
                    for c in result['classification']:
                        print("{r}: {n}".format(r=c['rank'], n=c['name']))
                except KeyError:
                    print("No classification provided.")
                noMatches = False
        except KeyError:
            pass
    if noMatches:
        print("\nSearch successful, but no exact matches found.")
        queryCOLFuzzy(taxname)
    print()
    sys.exit()


def queryCOLFuzzy(tname):
    taxname = formatTaxname(tname)
    url = 'http://www.catalogueoflife.org/col/webservice'
    params = {
        'name': taxname,
        'format': 'json',
        'response': 'full',
    }
    r = requests.get(url, params).json()
    checkError(r)
    print('Displaying up to the first 10 results for name search \"{n}\":'.format(n=taxname))
    for result in r['results'][:10]:
        print("\nName: {n} (Rank: {r})".format(n=result['name'], r=result['rank']))
        try:
            for c in result['classification']:
                print("{r}: {n}".format(r=c['rank'], n=c['name']))
        except KeyError:
            print("No classification provided.")
    print()
    sys.exit()


def queryCOLChildren(tname, taxrank):
    taxrank = taxrank.title()
    checkRank(taxrank)
    taxname = formatTaxname(tname)
    url = 'http://www.catalogueoflife.org/col/webservice'
    params = {
        'name': taxname,
        'format': 'json',
        'response': 'full',
    }
    r = requests.get(url, params).json()
    checkError(r)
    for result in r['results']:
        if result['name'] == taxname and result['rank'] == taxrank:
            print("\nChildren of {n} ({r})".format(n=result['name'], r=result['rank']))
            try:
                for c in results['child_taxa']:
                    print()


if __name__ == '__main__':
    try:
        taxname, taxrank, fuzzy, children = parseInput(sys.argv[1:])
    except TypeError:
        print('\nMissing arguments.\nUsage: col.py --name <scientific name> [--rank <taxonomic rank> --fuzzy --children]\n')
        sys.exit(2)
    if not taxname:
        print("\nMissing options or arguments.\nUsage: col.py --name <scientific name> [--rank <taxonomic rank> --fuzzy --children]\n")
        sys.exit(2)
    elif fuzzy and children:
        print("\nCannot select both fuzzy matching and find children. Please run two separate searches.\n")
        sys.exit(2)
    elif children:
        queryCOLChildren(taxname, taxrank)
    elif fuzzy:
        print()
        queryCOLFuzzy(taxname)
    elif taxname and not taxrank:
        queryCOLNoRank(taxname)
    elif taxname and taxrank:
        queryCOLRank(taxname, taxrank)
    sys.exit()
