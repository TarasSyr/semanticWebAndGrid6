from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD

g = Graph()

act = Namespace("http://example.org/")

actuator1 = URIRef(act["actuator/1"])
actuator2 = URIRef(act["actuator/2"])
actuator3 = URIRef(act["actuator/3"])
actuator4 = URIRef(act["actuator/4"])
electroActuator = URIRef(act["type/electro"])
pnevmoActuator = URIRef(act["type/pnevmo"])

g.add((actuator1, RDF.type, act.actuator))
g.add((actuator1, RDFS.label, Literal("Electrical actuator 1")))
g.add((actuator1, act.inputVoltage, Literal(5, datatype=XSD.integer)))
g.add((actuator1, act.type, electroActuator))

g.add((actuator2, RDF.type, act.actuator))
g.add((actuator2, RDFS.label, Literal("Pnevmatic actuator 1")))
g.add((actuator2, act.inputVoltage, Literal(5, datatype=XSD.integer)))
g.add((actuator2, act.type, pnevmoActuator))

g.add((actuator3, RDF.type, act.actuator))
g.add((actuator3, RDFS.label, Literal("Electrical actuator 2")))
g.add((actuator3, act.inputVoltage, Literal(2, datatype=XSD.integer)))
g.add((actuator3, act.type, electroActuator))

g.add((actuator4, RDF.type, act.actuator))
g.add((actuator4, RDFS.label, Literal("Pnevmatic actuator 2")))
g.add((actuator4, act.inputVoltage, Literal(2, datatype=XSD.integer)))
g.add((actuator4, act.type, pnevmoActuator))

g.add((electroActuator, RDF.type, act.type))
g.add((electroActuator, RDFS.label, Literal("Electrical actuator")))

g.add((pnevmoActuator, RDF.type, act.type))
g.add((pnevmoActuator, RDFS.label, Literal("Pnevmatic actuator")))

g.serialize("actuators_database.rdf", format="xml")

#print(g.serialize(format="turtle").encode("utf-8"))

query = """
    PREFIX ex: <http://example.org/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?actuator ?name ?inputVoltage ?type
    WHERE{
        ?actuator a ex:actuator .
        ?actuator rdfs:label ?name .
        ?actuator ex:inputVoltage ?inputVoltage .
        ?actuator ex:type ?type .
        FILTER (?inputVoltage >=5 )
    }
    """

results = g.query(query)

for row in results:
    print(f"Actuator: {row.actuator}, name: {row.name}, input voltage: {row.inputVoltage}, type: {row.type}")



