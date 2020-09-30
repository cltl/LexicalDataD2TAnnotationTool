from rdflib import ConjunctiveGraph, Graph


def get_fe_uris_and_labels(premon_nt, frame_uri):
    # get roles
    roles_of_frames = """SELECT ?o WHERE {
        <%s> <http://premon.fbk.eu/ontology/core#semRole> ?o
    }"""
    the_query = roles_of_frames % frame_uri

    results = premon_nt.query(the_query)

    label_to_fe_uri = dict()
    for result in results:
        fe_uri = str(result.asdict()['o'])

        label = get_rdf_label(premon_nt, fe_uri)
        label_to_fe_uri[label] = fe_uri

    return label_to_fe_uri

def get_rdf_uri(premon_nt, frame_label):
    frame_query = """SELECT ?s WHERE {
        ?s rdf:type <http://premon.fbk.eu/ontology/fn#Frame> .
        ?s rdfs:label "%s" .
    }"""
    the_query = frame_query % frame_label
    results = [result
               for result in premon_nt.query(the_query)]

    assert len(results) == 1, f'query should only have one result: {the_query}\n{results}'

    for result in results:
        frame_rdf_uri = str(result.asdict()['s'])

    return frame_rdf_uri

def load_nquads_file(path_to_nquad_file):
    """
    load rdf file in nquads format

    :param str path_to_nquad_file: path to rdf file in nquad format


    :rtype: rdflib.graph.ConjunctiveGraph
    :return: nquad

    """
    g = ConjunctiveGraph()
    with open(path_to_nquad_file, "rb") as infile:
        g.parse(infile, format="nquads")
    return g

def convert_nquads_to_nt(g, output_path):
    """

    :param rdflib.graph.ConjunctiveGraph g: a nquad graph

    :rtype:
    :return:
    """
    g.serialize(destination=output_path, format='nt')

def load_nt_graph(nt_path):
    g = Graph()
    with open(nt_path, 'rb') as infile:
        g.parse(file=infile, format='nt')

    return g


def get_rdf_label(graph, uri):
    query = """SELECT ?o WHERE {
        <%s> rdfs:label ?o
    }"""
    the_query = query % uri

    results = graph.query(the_query)

    labels = set()
    for result in results:
        label = str(result.asdict()['o'])
        labels.add(label)

    assert len(labels) == 1, f'expected one label for {uri}, got {labels}'

    return labels.pop()

if __name__ == '__main__':
    # should exist after running install.sh
    path = 'res/premon/premon-2018a-fn17-noinf.tql'
    g = load_nquads_file(path_to_nquad_file=path)
    convert_nquads_to_nt(g, output_path='res/premon/premon-2018a-fn17-noinf.nt')