from sreality_crawler import Crawler

def test_filterExistingLinks():
    newLinks = ["l1", "l2", "l3", "l4"]
    existingLinks = ["l3", "l4", "l5"]
    expected = ["l1", "l2"]

    actual = Crawler(None, None)._filterExistingLinks(newLinks, existingLinks)

    if len(actual) != len(expected):
        raise Exception("Wrong number of items returned")
    
    for e in expected:
        if not(e in actual):
            raise Exception("Expected item %s not returned" % e)

def test():
    test_filterExistingLinks()

test()