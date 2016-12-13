import networkx as nx
from ._internal import *
from .graphs import islink, isnode

def pick_labels(g, strategy):
    """Return the lables for a graph. 

    Strategies --
    * nodes: Label all verticies that represent graph nodes
    * links: Label all verticies that reprsent links
    * auto: Label nodes if there are any.  Label links otherwise
    """


    if strategy == "auto":
        links = [v for v in g.vertices() if islink(v,g)]
        nodes = [v for v in g.vertices() if isnode(v,g)]

        if len(links) > 0 and len(nodes) > 0 : 
            strategy = "nodes"
        elif len(links) > 0: 
            strategy = "links"
        else:
            strategy = "nodes"

    if strategy == "all":
        return {v: v for v in g.vertices()}
    
    if strategy == "nodes":
        return {v: v if not islink(v,g) else ""
                for v in g.vertices()}
    
    if strategy == "links": 
        return {v: v if not isnode(v,g) else ""
                for v in g.vertices()}

def draw(src, pos=None, ax=None, *, delta=None, iterations=2, label='auto', **layout_args):
    "Layout and draw a graph."

    layout_args["iterations"] = iterations 
    g = src if (not isinstance(src, FlangeTree)) else src()

    if pos is None:
        pos=nx.spectral_layout(g)
        pos=nx.spring_layout(g, pos=pos, **layout_args)

    def color(vertex):
        if isnode(vertex, g): return "r"
        if islink(vertex, g): return "b"
        return "w"

    types = nx.get_node_attributes(g, "_type")
    colors = [color(v) for v in g.vertices()] 

    labels = pick_labels(g, label)
    sizes = [300 if not islink(v, g) else 100
             for v in g.vertices()]

    nx.draw(g, pos=pos, ax=ax, node_size=sizes, node_color=colors)
    nx.draw_networkx_labels(g, labels=labels, pos=pos, ax=ax)


def show(flanglet, graph, *, size=(8,10)):
    "Draw a sequence of graphs to reprsent prcoessing" 

    before = graph().copy()
    foci = flanglet.focus(before.copy())
    after = flanglet(before.copy())

    pos = nx.spring_layout(before)
    
    fig = plt.gcf()
    fig.set_figheight(size[0])
    fig.set_figwidth(size[1])
    
    cols = max(len(foci), 6)
    rows = 4
    ax_before = plt.subplot2grid((rows, cols), (0,0), colspan=cols//2, rowspan=3)
    ax_after = plt.subplot2grid((rows, cols), (0,cols//2), colspan=cols//2, rowspan=3)
        
    nx.draw(before, pos=pos, ax=ax_before)
    nx.draw_networkx_labels(before, pos=pos, ax=ax_before)

    for (i, sub) in enumerate(foci):
        ax_select = plt.subplot2grid((rows, cols), (3, i))
        nx.draw(sub, pos=pos, ax=ax_select)
        nx.draw_networkx_labels(sub, pos=pos, ax=ax_select)

    nx.draw(after, pos=pos, ax=ax_after)
    nx.draw_networkx_labels(after, pos=pos, ax=ax_after)
    
    return fig
