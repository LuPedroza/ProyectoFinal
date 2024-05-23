import React, { useState, useEffect } from 'react';
import './App.css';
import Card from 'react-bootstrap/Card';

function IndividualSearch() {
  const [series, setSeries] = useState([]);
  const [searchType, setSearchType] = useState('serie');
  const [searchValue, setSearchValue] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchValue) {
        fetchData(searchType, searchValue);
      } else {
        setSeries([]); // Limpiar las tarjetas si no hay valor de búsqueda
      }
    }, 500); // Tiempo de espera antes de disparar la búsqueda (debouncing)

    return () => clearTimeout(delayDebounceFn);
  }, [searchType, searchValue]);

  const fetchData = async (type, value) => {
    setLoading(true);
    setSeries([]); // Limpiar las tarjetas antes de iniciar una nueva búsqueda

    try {
      let url = `http://localhost:8000/series/?tipo=${type}&valor=${value}`;
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
    setSearchValue(''); // Limpiar el valor de búsqueda al cambiar el tipo de búsqueda
  };

  const handleSearchValueChange = (event) => {
    setSearchValue(event.target.value);
  };

  return (
    <div>
      <br />
      <Encabezado />
      <br />
      <Opciones
        searchType={searchType}
        searchValue={searchValue}
        onSearchTypeChange={handleSearchTypeChange}
        onSearchValueChange={handleSearchValueChange}
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

function Opciones({ searchType, searchValue, onSearchTypeChange, onSearchValueChange }) {
  return (
    <div className="container">
      <div className="row">
        <p className="p"> Búsqueda por:</p>
        <div className="col-md-6">
          <select id="searchOptions" className="form-select select-custom" aria-label="Default select example" value={searchType} onChange={onSearchTypeChange}>
            <option value="serie">serie</option>
            <option value="tecnica">técnica</option>
            <option value="audiencia">audiencia</option>
            <option value="canal">canal</option>
            <option value="compania">compañía</option>
          </select>
        </div>
        <div className="col-md-6">
          <div className="row">
            <div className="col-md-12">
              <input className="form-control me-5" type="search" placeholder="Buscar" aria-label="Search" value={searchValue} onChange={onSearchValueChange} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function CardL({ serie, searchType }) {
  return (
    <Card style={{ width: '15rem', height: '27rem', margin: '10px' }}>
      <Card.Img variant="top" src={serie.imagen} style={{ height: '9rem' }} />
      <Card.Body>
        <Card.Title style={{ fontSize: '0.9rem' }}>
          {serie.NombreSerie}
        </Card.Title>
        <Card.Text style={{ fontSize: '0.8rem' }}>
          {serie.calificacionGoogle && <>Calificación Google: {serie.calificacionGoogle} <br /></>}
          {serie.calificacionIBM && <>Calificación IBM: {serie.calificacionIBM} <br /></>}
          {serie.numeroEpisodios && <>Número de Episodios: {serie.numeroEpisodios} <br /></>}
          {serie.Descripcion && <>Descripción: {serie.Descripcion} <br /></>}
          {serie.NombreCanal && <>Nombre del Canal: {serie.NombreCanal} <br /></>}
          {serie.NombreAudiencia && <>Nombre de la Audiencia: {serie.NombreAudiencia} <br /></>}
          {serie.Tecnicas && <>Técnicas: {serie.Tecnicas}</>}
          {searchType === 'compania' && <>Compañía: {serie.NombreCompania}</>}
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default IndividualSearch;