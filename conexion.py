import jpype
from rdflib import Literal, BNode, Namespace, Graph, URIRef
from rdflib.plugins.sparql import prepareQuery

# Cargar librerías de Apache Jena
jvmPath = jpype.getDefaultJVMPath()
jena_path = r"C:\Users\yelan\Desktop\apache-jena-fuseki-5.0.0\fuseki-server.jar"
jpype.startJVM(jvmPath, "-Djava.class.path=%s" % jena_path)

# Cargar ontología RDF
g = Graph()
g.parse(r"C:\Users\yelan\Desktop\Gestión del conocimiento\Ontologia\SeriesAnimadas.rdf", format="xml")

# Definir prefijos para la consulta SPARQL
series= Namespace("http://www.semanticweb.org/yelan/ontologies/2024/2/seriesAnimadas#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
xsd= Namespace("http://www.w3.org/2001/XMLSchema#")

def convertir_a_json_nombre(resultados):
    series_list = []
    for result in resultados:
        serie_dict = {
            'NombreSerie': str(result.NombreSerie),
            'calificacionGoogle': str(result.calificacionGoogle),
            'calificacionIBM': str(result.calificacionIBM),
            'numeroEpisodios': str(result.numeroEpisodios),
            'Descripcion': str(result.Descripcion),
            'imagen': str(result.imagen),
            'NombreCanal': str(result.NombreCanal),
            'NombreAudiencia': str(result.NombreAudiencia),
            'Tecnicas': str(result.Tecnicas),
        }
        series_list.append(serie_dict)
    
    return series_list

def convertir_a_json_sinCanal(resultados):
    series_list = []
    for result in resultados:
        serie_dict = {
            'NombreSerie': str(result.NombreSerie),
            'calificacionGoogle': str(result.calificacionGoogle),
            'calificacionIBM': str(result.calificacionIBM),
            'numeroEpisodios': str(result.numeroEpisodios),
            'Descripcion': str(result.Descripcion),
            'imagen': str(result.imagen),
            'NombreAudiencia': str(result.NombreAudiencia),
            'Tecnicas': str(result.Tecnicas),
        }
        series_list.append(serie_dict)
    
    return series_list

def convertir_a_json_sin_sinTecnica(resultados):
    series_list = []
    for result in resultados:
        serie_dict = {
            'NombreSerie': str(result.NombreSerie),
            'calificacionGoogle': str(result.calificacionGoogle),
            'calificacionIBM': str(result.calificacionIBM),
            'numeroEpisodios': str(result.numeroEpisodios),
            'Descripcion': str(result.Descripcion),
            'imagen': str(result.imagen),
            'NombreCanal': str(result.NombreCanal),
            'NombreAudiencia': str(result.NombreAudiencia),
        }
        series_list.append(serie_dict)
    
    return series_list

def convertir_a_json_compania(resultados):
    series_list = []
    for result in resultados:
        serie_dict = {
            'NombreCompania': str(result.NombreCompania),
            'NombreSerie': str(result.NombreSerie),
            'calificacionGoogle': str(result.calificacionGoogle),
            'calificacionIBM': str(result.calificacionIBM),
            'numeroEpisodios': str(result.numeroEpisodios),
            'Descripcion': str(result.Descripcion),
            'imagen': str(result.imagen),
        }
        series_list.append(serie_dict)
    
    return series_list

def seriePorCanal(canal):
    consulta_sparql = f"""
    SELECT DISTINCT ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia 
    WHERE {{
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        ?audiencia series:NombreAudiencia ?NombreAudiencia.
        ?canal rdf:type series:Canal.
        ?canal series:Transmite ?serie.
        ?canal series:NombreCanal ?NombreCanal.
        FILTER (regex(?NombreCanal, "{canal}", "i"))
    }}
    GROUP BY ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
    return convertir_a_json_sin_sinTecnica(results)


def seriePorTecnica(tec):
    consulta_sparql = f"""
    SELECT DISTINCT ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreAudiencia (GROUP_CONCAT(?NombreTecnica; separator=", ") AS ?Tecnicas) 
    WHERE {{
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        ?audiencia series:NombreAudiencia ?NombreAudiencia.
        ?serie series:Utiliza ?Tecnica.
        ?Tecnica series:NombreTecnica ?NombreTecnica.
        FILTER (regex(?NombreTecnica, "{tec}", "i"))
    }}
    GROUP BY ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen  ?NombreAudiencia
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
    return convertir_a_json_sinCanal(results)



def seriePorAudiencia(audien):
    consulta_sparql = f"""
    SELECT DISTINCT ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia 
    WHERE {{
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        ?audiencia series:NombreAudiencia ?NombreAudiencia.
        ?canal rdf:type series:Canal.
        ?canal series:Transmite ?serie.
        ?canal series:NombreCanal ?NombreCanal.
        FILTER (regex(?NombreAudiencia, "{audien}", "i"))
    }}
    GROUP BY ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
    return convertir_a_json_sin_sinTecnica(results)


def TodasSeries():
    consulta_sparql = """
    SELECT DISTINCT ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia (GROUP_CONCAT(?NombreTecnica; separator=", ") AS ?Tecnicas) 
    WHERE {{
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        ?audiencia series:NombreAudiencia ?NombreAudiencia.
        ?serie series:Utiliza ?Tecnica.
        ?Tecnica series:NombreTecnica ?NombreTecnica.
        ?canal rdf:type series:Canal.
        ?canal series:Transmite ?serie.
        ?canal series:NombreCanal ?NombreCanal.
    }}
    GROUP BY ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
    return convertir_a_json_nombre(results)



def seriesPorNombre(serie):
    consulta_sparql = f"""
    SELECT DISTINCT ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia (GROUP_CONCAT(?NombreTecnica; separator=", ") AS ?Tecnicas) 
    WHERE {{
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        ?audiencia series:NombreAudiencia ?NombreAudiencia.
        ?serie series:Utiliza ?Tecnica.
        ?Tecnica series:NombreTecnica ?NombreTecnica.
        ?canal rdf:type series:Canal.
        ?canal series:Transmite ?serie.
        ?canal series:NombreCanal ?NombreCanal.
        FILTER (regex(?NombreSerie, "{serie}", "i"))
    }}
    GROUP BY ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
    return convertir_a_json_nombre(results)

def seriesPorNombreYcanal(serie,canal):
    consulta_sparql = f"""
    SELECT DISTINCT ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia (GROUP_CONCAT(?NombreTecnica; separator=", ") AS ?Tecnicas) 
    WHERE {{
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        ?audiencia series:NombreAudiencia ?NombreAudiencia.
        ?serie series:Utiliza ?Tecnica.
        ?Tecnica series:NombreTecnica ?NombreTecnica.
        ?canal rdf:type series:Canal.
        ?canal series:Transmite ?serie.
        ?canal series:NombreCanal ?NombreCanal.
        FILTER (regex(?NombreSerie, "{serie}", "i") && regex(?NombreCanal, "{canal}", "i"))
    }}
    GROUP BY ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
    return convertir_a_json_nombre(results)

def seriesPorNombreYaudiencia(serie,audi):
    consulta_sparql = f"""
    SELECT DISTINCT ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia (GROUP_CONCAT(?NombreTecnica; separator=", ") AS ?Tecnicas) 
    WHERE {{
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        ?audiencia series:NombreAudiencia ?NombreAudiencia.
        ?serie series:Utiliza ?Tecnica.
        ?Tecnica series:NombreTecnica ?NombreTecnica.
        ?canal rdf:type series:Canal.
        ?canal series:Transmite ?serie.
        ?canal series:NombreCanal ?NombreCanal.
        FILTER (regex(?NombreSerie, "{serie}", "i") && regex(?NombreAudiencia, "{audi}", "i"))
    }}
    GROUP BY ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreCanal ?NombreAudiencia
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
    return convertir_a_json_nombre(results)

def seriesPorCompania(comp):
    consulta_sparql = f"""
    
    SELECT DISTINCT ?NombreCompania ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen 
    WHERE {{
        ?compania rdf:type series:Compania.
        ?compania series:Produce ?serie.  
        ?compania series:NombreCompania ?NombreCompania.
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        FILTER (regex(?NombreSerie, "{comp}", "i"))
    }}
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
 
    return convertir_a_json_compania(results)



def seriePorTecnicayNombre(serie,tec):
    consulta_sparql = f"""
    SELECT DISTINCT ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen ?NombreAudiencia (GROUP_CONCAT(?NombreTecnica; separator=", ") AS ?Tecnicas) 
    WHERE {{
        ?serie rdf:type series:Serie.
        ?serie series:NombreSerie ?NombreSerie.
        ?serie series:CalificacionesGoogle ?calificacionGoogle.
        ?serie series:CalificacionesIBM ?calificacionIBM.
        ?serie series:numeroEpisodios ?numeroEpisodios.
        ?serie series:Descripcion ?Descripcion.
        ?serie series:DirigdoA ?audiencia.
        ?audiencia series:imagen ?imagen.
        ?audiencia series:NombreAudiencia ?NombreAudiencia.
        ?serie series:Utiliza ?Tecnica.
        ?Tecnica series:NombreTecnica ?NombreTecnica.
        FILTER (regex(?NombreSerie, "{serie}", "i") && regex(?NombreTecnica, "{tec}", "i"))
    }}
    GROUP BY ?NombreSerie ?calificacionGoogle ?calificacionIBM ?numeroEpisodios ?Descripcion ?imagen  ?NombreAudiencia
    """

    query = prepareQuery(consulta_sparql, initNs={"rdf": rdf, "xsd": xsd, "series": series})
    results = g.query(query)
    return convertir_a_json_sinCanal(results)
