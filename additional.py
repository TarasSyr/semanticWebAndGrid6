from flask import Flask, render_template, jsonify
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, XSD
import plotly.graph_objs as go
from igraph import Graph as iGraph

app = Flask(__name__)

# Створення RDF-графа
g = Graph()
ex = Namespace("http://example.org/")

# Додавання даних про друковані плати
pcb1 = URIRef(ex["pcb/1"])
pcb2 = URIRef(ex["pcb/2"])
pcb3 = URIRef(ex["pcb/3"])
circuit1 = URIRef(ex["circuit/1"])
circuit2 = URIRef(ex["circuit/2"])

g.add((pcb1, RDF.type, ex.PCB))
g.add((pcb1, RDFS.label, Literal("PCB 1")))
g.add((pcb1, ex.layers, Literal(4, datatype=XSD.integer)))
g.add((pcb1, ex.usedInCircuit, circuit1))

g.add((pcb2, RDF.type, ex.PCB))
g.add((pcb2, RDFS.label, Literal("PCB 2")))
g.add((pcb2, ex.layers, Literal(2, datatype=XSD.integer)))
g.add((pcb2, ex.usedInCircuit, circuit2))

g.add((pcb3, RDF.type, ex.PCB))
g.add((pcb3, RDFS.label, Literal("PCB 3")))
g.add((pcb3, ex.layers, Literal(6, datatype=XSD.integer)))
g.add((pcb3, ex.usedInCircuit, circuit1))

g.add((circuit1, RDF.type, ex.Circuit))
g.add((circuit1, RDFS.label, Literal("Circuit 1")))

g.add((circuit2, RDF.type, ex.Circuit))
g.add((circuit2, RDFS.label, Literal("Circuit 2")))


# Функція для виконання SPARQL-запиту
def query_data():
    query = """
        PREFIX ex: <http://example.org/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?pcb ?name ?layers ?circuit
        WHERE {
            ?pcb a ex:PCB .
            ?pcb rdfs:label ?name .
            ?pcb ex:layers ?layers .
            ?pcb ex:usedInCircuit ?circuit .
            FILTER (?layers > 2)
        }
    """
    results = g.query(query)
    return [
        {
            "pcb": str(row.pcb),
            "name": str(row.name),
            "layers": int(row.layers),
            "circuit": str(row.circuit),
        }
        for row in results
    ]


# Роут для веб-сторінки
@app.route("/")
def index():
    data = query_data()

    # Дані для графіка Plotly
    fig = go.Figure()
    for item in data:
        fig.add_trace(
            go.Bar(
                x=[item["name"]],
                y=[item["layers"]],
                name=f'Used in {item["circuit"].split("/")[-1]}',
            )
        )
    plot_div = fig.to_html(full_html=False)

    return render_template("index.html", plot_div=plot_div, data=data)


# Роут для графа iGraph
@app.route("/graph")
def graph():
    ig = iGraph(directed=True)
    nodes = set()
    edges = []

    data = query_data()
    for item in data:
        pcb = item["name"]
        circuit = item["circuit"].split("/")[-1]
        nodes.add(pcb)
        nodes.add(circuit)
        edges.append((pcb, circuit))

    ig.add_vertices(list(nodes))
    ig.add_edges(edges)

    layout = ig.layout("kk")
    visual_style = {
        "vertex_label": ig.vs["name"],
        "vertex_size": 20,
        "edge_arrow_size": 0.5,
    }
    return jsonify(
        {
            "nodes": list(nodes),
            "edges": edges,
        }
    )

# Запуск Flask
if __name__ == "__main__":
    app.run(debug=True)
