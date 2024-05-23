import React, { useState, useEffect } from 'react';
import './App.css';
import Card from 'react-bootstrap/Card';

function DualSearch() {
  const [series, setSeries] = useState([]);
  const [searchType, setSearchType] = useState('serieYcanal');
  const [searchValue1, setSearchValue1] = useState('');
  const [searchValue2, setSearchValue2] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchValue1 && searchValue2) {
        fetchData(searchType, searchValue1, searchValue2);
      } else {
        setSeries([]); // Limpiar las tarjetas si no hay valor de búsqueda
      }
    }, 500); // Tiempo de espera antes de disparar la búsqueda (debouncing)

    return () => clearTimeout(delayDebounceFn);
  }, [searchType, searchValue1, searchValue2]);

  const fetchData = async (type, value1, value2) => {
    setLoading(true);
    setSeries([]); // Limpiar las tarjetas antes de iniciar una nueva búsqueda

    try {
      let url = `http://localhost:8000/series/?tipo=${type}&valor=${value1}&valor2=${value2}`;
      const response = await fetch(url);
      const data = await response.json();

      if (Array.isArray(data)) {
        setSeries(data);
      }
    } catch (error) {
      console.error('Error fetching series:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchTypeChange = (event) => {
    setSearchType(event.target.value);
    setSearchValue1(''); // Limpiar los valores de búsqueda al cambiar el tipo de búsqueda
    setSearchValue2('');
  };

  const handleSearchValue1Change = (event) => {
    setSearchValue1(event.target.value);
  };

  const handleSearchValue2Change = (event) => {
    setSearchValue2(event.target.value);
  };

  return (
    <div>
      <br />
      <Encabezado />
      <br />
      <Opciones
        searchType={searchType}
        searchValue1={searchValue1}
        searchValue2={searchValue2}
        onSearchTypeChange={handleSearchTypeChange}
        onSearchValue1Change={handleSearchValue1Change}
        onSearchValue2Change={handleSearchValue2Change}
      />
      <br />
      {loading ? <p>Cargando...</p> : null}
      <CardContainer series={series} />
    </div>
  );
}

const CardContainer = ({ series }) => {
  return (
    <div className="card-container">
      {series.length > 0 ? (
        series.map((serie) => <CardL key={serie.imagen} serie={serie} />)
      ) : (
        <p></p>
      )}
    </div>
  );
};

function Encabezado() {
  return (
    <div>
      <br />
      <div className="row" style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-start' }}>
        <div className="col-md-5" style={{ textAlign: 'right' }}>
          <img
            src="https://www.animaker.es/blog/wp-content/uploads/2023/08/New_Courage-271x300.webp"
            alt="Courage the Cowardly Dog"
            style={{ maxWidth: '100px', height: 'auto', marginRight: '0px' }}
          />
        </div>
        <div className="col-md-7" style={{ textAlign: 'left' }}>
          <h1 className="titulo">
            ToonMania
          </h1>
        </div>
      </div>
    </div>
  );
}

function Opciones({ searchType, searchValue1, searchValue2, onSearchTypeChange, onSearchValue1Change, onSearchValue2Change }) {
  return (
    <div className="container">
      <div className="row">
        <p className="p"> Búsqueda por:</p>
        <div className="col-md-4">
          <select id="searchOptions" className="form-select select-custom" aria-label="Default select example" value={searchType} onChange={onSearchTypeChange}>
            <option value="serieYcanal">Serie y Canal</option>
            <option value="serieYaudiencia">Serie y Audiencia</option>
            <option value="TecnicaYNombre">Serie y Técnica</option>
          </select>
        </div>
        <div className="col-md-4">
          <div className="row">
            <div className="col-md-12">
              <input className="form-control me-5" type="search" placeholder="Serie" aria-label="Search" value={searchValue1} onChange={onSearchValue1Change} />
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="row">
            <div className="col-md-12">
              <input className="form-control me-5" type="search" placeholder="Canal/Audiencia/Técnica" aria-label="Search" value={searchValue2} onChange={onSearchValue2Change} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function CardL({ serie }) {
  return (
    <Card style={{ width: '15rem', height: '27rem', margin: '10px' }}>
      <Card.Img variant="top" src={serie.imagen} style={{ height: '9rem' }} />
      <Card.Body>
        <Card.Title style={{ fontSize: '0.9rem' }}>
          {serie.NombreSerie}
        </Card.Title>
        <Card.Text style={{ fontSize: '0.8rem' }}>
          {serie.calificacionGoogle && <>Calificación Google: {serie.calificacionGoogle}<br /></>}
          {serie.calificacionIBM && <>Calificación IBM: {serie.calificacionIBM}<br /></>}
          {serie.numeroEpisodios && <>Episodios: {serie.numeroEpisodios}<br /></>}
          {serie.Descripcion && <>Descripción: {serie.Descripcion}<br /></>}
          {serie.NombreCanal && <>Canal: {serie.NombreCanal}<br /></>}
          {serie.NombreAudiencia && <>Audiencia: {serie.NombreAudiencia}<br /></>}
          {serie.Tecnicas && <>Técnicas: {serie.Tecnicas}<br /></>}
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default DualSearch;
