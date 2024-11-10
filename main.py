from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD

g=Graph()

ex = Namespace("http://example.org/")

transistor1=URIRef(ex["transistor/1"])
transistor2=URIRef(ex["transistor/2"])
transistor3=URIRef(ex["transistor/3"])
transistor4=URIRef(ex["transistor/4"])
bipolarTransistor=URIRef(ex["type/bipolar"])
fieldTransistor=URIRef(ex["type/field"])

g.add((transistor1, RDF.type, ex.transistor))
g.add((transistor1, RDFS.label, Literal("Bipolar junction transistor 1")))
g.add((transistor1, ex.maxCollectCurrent, Literal(5, datatype=XSD.integer)))
g.add((transistor1, ex.type, bipolarTransistor))

g.add((transistor2, RDF.type, ex.transistor))
g.add((transistor2, RDFS.label, Literal("Field effect transistor 1")))
g.add((transistor2, ex.maxCollectCurrent, Literal(10, datatype=XSD.integer)))
g.add((transistor2, ex.type, fieldTransistor))

g.add((transistor3, RDF.type, ex.transistor))
g.add((transistor3, RDFS.label, Literal("Bipolar junction transistor 2")))
g.add((transistor3, ex.maxCollectCurrent, Literal(15, datatype=XSD.integer)))
g.add((transistor3, ex.type, bipolarTransistor))

g.add((transistor4, RDF.type, ex.transistor))
g.add((transistor4, RDFS.label, Literal("Field effect transistor 2")))
g.add((transistor4, ex.maxCollectCurrent, Literal(12, datatype=XSD.integer)))
g.add((transistor4, ex.type, fieldTransistor))

g.add((bipolarTransistor, RDF.type, ex.type))
g.add((bipolarTransistor, RDFS.label, Literal("Bipolar junction transistor")))

g.add((fieldTransistor, RDF.type, ex.type))
g.add((fieldTransistor, RDFS.label, Literal("Field effect transistor")))

g.serialize("transistors_database.ttl", format="turtle")

#print(g.serialize(format="turtle").encode("utf-8"))

query="""
    PREFIX ex: <http://example.org/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?transistor ?name ?maxCollectCurrent ?type
    WHERE{
        ?transistor a ex:transistor .
        ?transistor rdfs:label ?name .
        ?transistor ex:maxCollectCurrent ?maxCollectCurrent .
        ?transistor ex:type ?type .
        FILTER (?maxCollectCurrent > 10)
    }
    """

results = g.query(query)

for row in results:
    print(f"Transistor: {row.transistor}, name: {row.name}, maximum collector current: {row.maxCollectCurrent}, type: {row.type}")



